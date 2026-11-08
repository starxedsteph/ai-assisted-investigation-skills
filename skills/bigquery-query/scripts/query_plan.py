#!/usr/bin/env python3
"""Prepare capped BigQuery CLI commands without authenticating or running them."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


PROFILE_KEYS = {
    "schema_version",
    "execution_project",
    "location",
    "billing_mode",
    "allowed_tables",
    "maximum_bytes_billed",
    "maximum_result_rows",
}
PROJECT = re.compile(r"[a-z][a-z0-9-]{4,28}[a-z0-9]")
TABLE = re.compile(r"[a-z][a-z0-9-]{4,28}[a-z0-9]\.[A-Za-z0-9_]+\.[A-Za-z0-9_-]+")
PARAMETER = re.compile(
    r"([A-Za-z_][A-Za-z0-9_]*):"
    r"(STRING|INT64|FLOAT64|NUMERIC|BIGNUMERIC|BOOL|DATE|DATETIME|TIME|TIMESTAMP|BYTES):"
    r"(.*)",
    re.DOTALL,
)
EMPTY_BIGQUERYRC = Path(__file__).resolve().parents[1] / "assets" / "empty.bigqueryrc"


def positive_integer(value, label):
    if type(value) is not int or value <= 0:
        raise ValueError(f"{label} must be a positive integer; unset or zero blocks execution.")
    return value


def validate_profile(profile):
    if not isinstance(profile, dict) or set(profile) != PROFILE_KEYS:
        raise ValueError("Profile must contain exactly the documented profile-template fields.")
    if type(profile["schema_version"]) is not int or profile["schema_version"] != 1:
        raise ValueError("Unsupported profile schema_version.")
    project = profile["execution_project"]
    if not isinstance(project, str) or not PROJECT.fullmatch(project):
        raise ValueError("Confirm an explicit execution project ID in the profile.")
    location = profile["location"]
    if not isinstance(location, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", location):
        raise ValueError("Confirm an explicit dataset location in the profile.")
    if profile["billing_mode"] not in ("sandbox", "on_demand"):
        raise ValueError("Verify sandbox or on_demand pricing; unverified and capacity modes are blocked.")
    tables = profile["allowed_tables"]
    if not isinstance(tables, list) or not tables:
        raise ValueError("Authorize a nonempty exact source-table allowlist.")
    if any(not isinstance(table, str) or not TABLE.fullmatch(table) for table in tables):
        raise ValueError("Use fully qualified conventional ASCII table IDs, without wildcards.")
    if len(set(tables)) != len(tables):
        raise ValueError("Source-table allowlist contains duplicates.")
    positive_integer(profile["maximum_bytes_billed"], "Profile maximum_bytes_billed")
    positive_integer(profile["maximum_result_rows"], "Profile maximum_result_rows")
    return profile


def fingerprint(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def build_plan(profile, sql, sources, cap, parameters=()):
    validate_profile(profile)
    if EMPTY_BIGQUERYRC.read_text(encoding="utf-8").strip():
        raise ValueError("Bundled empty.bigqueryrc must remain empty; do not inherit query defaults.")
    positive_integer(cap, "Query maximum_bytes_billed")
    if cap > profile["maximum_bytes_billed"]:
        raise ValueError("Query cap exceeds the profile ceiling; a separately approved setup change is required.")
    if not isinstance(sql, str) or not sql.strip():
        raise ValueError("Supply nonempty reviewed SQL.")
    if not sources:
        raise ValueError("Declare the exact source tables reviewed for this query.")
    if any(not isinstance(source, str) or source not in profile["allowed_tables"] for source in sources):
        raise ValueError("Query declares a source outside the approved table allowlist.")
    names = set()
    for parameter in parameters:
        match = PARAMETER.fullmatch(parameter) if isinstance(parameter, str) else None
        if match is None:
            raise ValueError("Parameters must use named scalar NAME:TYPE:VALUE syntax.")
        if match[1] in names:
            raise ValueError(f"Duplicate parameter name: {match[1]}")
        names.add(match[1])
    parameters = sorted(parameters)
    base = [
        "bq",
        f"--bigqueryrc={EMPTY_BIGQUERYRC}",
        f'--project_id={profile["execution_project"]}',
        f'--location={profile["location"]}',
        "--format=json",
        "query",
        "--use_legacy_sql=false",
        f"--maximum_bytes_billed={cap}",
        f'--max_rows={profile["maximum_result_rows"]}',
        *(f"--parameter={parameter}" for parameter in parameters),
    ]
    plan = {
        "schema_version": 1,
        "execution_project": profile["execution_project"],
        "location": profile["location"],
        "billing_mode": profile["billing_mode"],
        "source_tables": sorted(set(sources)),
        "maximum_bytes_billed": cap,
        "maximum_result_rows": profile["maximum_result_rows"],
        "query_sha256": hashlib.sha256(sql.encode("utf-8")).hexdigest(),
        "parameters_sha256": fingerprint(parameters),
        "profile_sha256": fingerprint(profile),
        "requires_fresh_human_approval": True,
        "sql_input": "stdin",
        "dry_run_argv": base + ["--dry_run=true", "--use_cache=false"],
        "execution_argv": base + ["--dry_run=false", "--use_cache=true"],
    }
    plan["plan_sha256"] = fingerprint(plan)
    return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--check-profile", action="store_true", help="Validate local settings only")
    parser.add_argument("--sql-file", type=Path)
    parser.add_argument("--source-table", action="append", default=[])
    parser.add_argument("--maximum-bytes-billed", type=int)
    parser.add_argument("--parameter", action="append", default=[])
    args = parser.parse_args()
    try:
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
        validate_profile(profile)
        if args.check_profile:
            if args.sql_file or args.source_table or args.maximum_bytes_billed is not None or args.parameter:
                raise ValueError("--check-profile cannot be combined with query options.")
            result = {
                "configuration_valid": True,
                "cloud_verification_performed": False,
                "execution_approved": False,
            }
        else:
            if args.sql_file is None:
                raise ValueError("Supply --sql-file or use --check-profile.")
            sql = args.sql_file.read_text(encoding="utf-8")
            result = build_plan(
                profile, sql, args.source_table, args.maximum_bytes_billed, args.parameter
            )
    except (OSError, UnicodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
