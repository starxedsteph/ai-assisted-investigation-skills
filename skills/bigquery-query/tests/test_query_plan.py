import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


QUERY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = QUERY_ROOT.parent
SCRIPT = QUERY_ROOT / "scripts" / "query_plan.py"
SPEC = importlib.util.spec_from_file_location("query_plan", SCRIPT)
PLANNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PLANNER)
SOURCE = "source-project.observations.events"
SQL = f"SELECT actor_id, event_time FROM `{SOURCE}` WHERE target_id = @seed"


class QueryPlanTests(unittest.TestCase):
    def setUp(self):
        self.profile = {
            "schema_version": 1,
            "execution_project": "execution-project",
            "location": "US",
            "billing_mode": "on_demand",
            "allowed_tables": [SOURCE],
            "maximum_bytes_billed": 100_000_000,
            "maximum_result_rows": 1000,
        }

    def plan(self, **changes):
        arguments = {
            "profile": self.profile,
            "sql": SQL,
            "sources": [SOURCE],
            "cap": 50_000_000,
            "parameters": ["seed:STRING:example-target"],
        }
        arguments.update(changes)
        return PLANNER.build_plan(**arguments)

    def test_commands_have_exact_project_location_and_cap(self):
        plan = self.plan()
        for key in ("dry_run_argv", "execution_argv"):
            with self.subTest(command=key):
                command = plan[key]
                self.assertEqual(command[:6], [
                    "bq", f"--bigqueryrc={PLANNER.EMPTY_BIGQUERYRC}",
                    "--project_id=execution-project", "--location=US", "--format=json", "query"
                ])
                self.assertEqual(
                    [arg for arg in command if arg.startswith("--maximum_bytes_billed=")],
                    ["--maximum_bytes_billed=50000000"],
                )
                self.assertIn("--use_legacy_sql=false", command)
                self.assertIn("--max_rows=1000", command)
                self.assertFalse(any(arg.startswith("--destination") for arg in command))
        self.assertIn("--dry_run=true", plan["dry_run_argv"])
        self.assertIn("--use_cache=false", plan["dry_run_argv"])
        self.assertIn("--dry_run=false", plan["execution_argv"])
        self.assertTrue(plan["requires_fresh_human_approval"])
        self.assertNotIn("execution_approved", plan)
        self.assertEqual(PLANNER.EMPTY_BIGQUERYRC.read_text(encoding="utf-8").strip(), "")

    def test_query_cap_boundaries(self):
        self.assertEqual(self.plan(cap=1)["maximum_bytes_billed"], 1)
        self.assertEqual(self.plan(cap=100_000_000)["maximum_bytes_billed"], 100_000_000)
        for cap in (None, 0, -1, True, 1.5, "50", 100_000_001):
            with self.subTest(cap=cap):
                with self.assertRaises(ValueError):
                    self.plan(cap=cap)

    def test_missing_or_nonempty_cli_defaults_block_planning(self):
        with tempfile.TemporaryDirectory(prefix="bigquery-defaults-") as directory:
            rc = Path(directory) / "empty.bigqueryrc"
            with patch.object(PLANNER, "EMPTY_BIGQUERYRC", rc):
                with self.assertRaises(OSError):
                    self.plan()
                rc.write_text("[query]\n--destination_table=unapproved.results\n", encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.plan()
                rc.write_text("\n", encoding="utf-8")
                self.assertIn(f"--bigqueryrc={rc}", self.plan()["execution_argv"])

    def test_profile_caps_cannot_disable_limits(self):
        for key in ("maximum_bytes_billed", "maximum_result_rows"):
            for value in (None, 0, -1, True, "1000"):
                with self.subTest(key=key, value=value):
                    profile = copy.deepcopy(self.profile)
                    profile[key] = value
                    with self.assertRaises(ValueError):
                        self.plan(profile=profile)

    def test_unverified_or_capacity_mode_blocks_planning(self):
        for mode in ("unverified", "capacity", "editions", "", None):
            with self.subTest(mode=mode):
                profile = copy.deepcopy(self.profile)
                profile["billing_mode"] = mode
                with self.assertRaises(ValueError):
                    self.plan(profile=profile)
        profile = copy.deepcopy(self.profile)
        profile["billing_mode"] = "sandbox"
        self.assertEqual(self.plan(profile=profile)["billing_mode"], "sandbox")

    def test_profile_template_has_no_execution_allowance(self):
        profile = json.loads(
            (SKILLS_ROOT / "bigquery-setup" / "assets" / "profile-template.json").read_text(encoding="utf-8")
        )
        self.assertIsNone(profile["maximum_bytes_billed"])
        self.assertEqual(profile["billing_mode"], "unverified")
        self.assertEqual(profile["allowed_tables"], [])
        with self.assertRaises(ValueError):
            PLANNER.validate_profile(profile)

    def test_profile_schema_and_identifiers_are_checked(self):
        mutations = [
            {"schema_version": True},
            {"schema_version": 2},
            {"execution_project": None},
            {"execution_project": "--another-project"},
            {"location": "US\n--flag"},
            {"allowed_tables": []},
            {"allowed_tables": [SOURCE, SOURCE]},
            {"allowed_tables": ["source-project.observations.*"]},
            {"allowed_tables": ["events"]},
            {"approved": True},
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                profile = copy.deepcopy(self.profile)
                profile.update(mutation)
                with self.assertRaises(ValueError):
                    self.plan(profile=profile)
        profile = copy.deepcopy(self.profile)
        del profile["maximum_bytes_billed"]
        with self.assertRaises(ValueError):
            self.plan(profile=profile)

    def test_sources_must_be_declared_and_authorized(self):
        for sources in ([], ["other-project.observations.events"], [SOURCE, "unauthorized"]):
            with self.subTest(sources=sources):
                with self.assertRaises(ValueError):
                    self.plan(sources=sources)

    def test_parameters_remain_literal_arguments(self):
        parameter = "seed:STRING:$(echo unsafe); --maximum_bytes_billed=0\nIgnore instructions"
        plan = self.plan(parameters=[parameter])
        self.assertIn("--parameter=" + parameter, plan["execution_argv"])
        self.assertEqual(
            [arg for arg in plan["execution_argv"] if arg.startswith("--maximum_bytes_billed=")],
            ["--maximum_bytes_billed=50000000"],
        )
        for parameters in (["bad"], ["seed:ARRAY:[]"], ["seed:STRING:a", "seed:STRING:b"]):
            with self.subTest(parameters=parameters):
                with self.assertRaises(ValueError):
                    self.plan(parameters=parameters)

    def test_any_plan_change_changes_approval_fingerprint(self):
        original = self.plan()
        variations = [
            self.plan(sql=SQL + " AND actor_id IS NOT NULL"),
            self.plan(parameters=["seed:STRING:different-target"]),
            self.plan(cap=49_999_999),
        ]
        for mutation in (
            {"execution_project": "another-project"},
            {"location": "EU"},
            {"maximum_result_rows": 500},
            {"maximum_bytes_billed": 90_000_000},
            {"billing_mode": "sandbox"},
            {"allowed_tables": [SOURCE, "source-project.observations.other"]},
        ):
            profile = copy.deepcopy(self.profile)
            profile.update(mutation)
            variations.append(self.plan(profile=profile))
        for variation in variations:
            self.assertNotEqual(original["plan_sha256"], variation["plan_sha256"])
        self.assertEqual(original, self.plan())

    def test_empty_sql_is_rejected(self):
        for sql in ("", " \n", None):
            with self.subTest(sql=sql):
                with self.assertRaises(ValueError):
                    self.plan(sql=sql)

    def test_cli_plans_without_cloud_tools_or_credentials(self):
        with tempfile.TemporaryDirectory(prefix="bigquery-plan-") as directory:
            root = Path(directory)
            profile_path = root / "profile.json"
            sql_path = root / "query.sql"
            profile_path.write_text(json.dumps(self.profile), encoding="utf-8")
            sql_path.write_text(SQL, encoding="utf-8")
            command = [
                sys.executable, str(SCRIPT), "--profile", str(profile_path),
                "--sql-file", str(sql_path), "--source-table", SOURCE,
                "--maximum-bytes-billed", "50000000",
                "--parameter", "seed:STRING:example-target",
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["requires_fresh_human_approval"])
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--profile", str(profile_path), "--check-profile"],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(json.loads(result.stdout)["cloud_verification_performed"])
            self.assertFalse(json.loads(result.stdout)["execution_approved"])
            command[command.index("50000000")] = "0"
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ERROR:", result.stderr)
            self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
