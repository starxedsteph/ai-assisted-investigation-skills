---
name: bigquery-query
description: Prepares and runs explicitly approved, read-only BigQuery investigation queries after setup, with dry-run estimates and a positive server-enforced bytes-billed cap on every execution. Use for BigQuery SQL, query estimates, or retrieving approved observational inputs. Defaults to planning and dry runs; never treats setup or an investigation request as execution approval.
---

# BigQuery query

Default to a plan and dry run. Use [`bigquery-setup`](../bigquery-setup/SKILL.md)
for missing or changed access, project, location, pricing, sources, or limits;
never repair these by automatically enabling billing or raising caps.
Read `../campaign-identification/SKILL.md` and `../safe-data-ingestion/SKILL.md`
for investigation and evidence rules, not arbitrary browsing or outcome evaluation.

## Prepare one capped query

Read `.bigquery-investigation/profile.json` in the agreed workspace and reconfirm
the effective CLI identity, explicit project/location, source allowlist, and
positive ceiling. Only verified billing-disabled sandbox or ordinary on-demand
pricing is supported; unknown or capacity/edition modes block execution.

Inspect approved metadata without previewing rows. Write one read-only GoogleSQL
`SELECT` or `WITH ... SELECT`, with fully qualified approved sources, documented
observational columns (never `SELECT *`), partition bounds where possible, and
named value parameters. Review views and all underlying sources/functions.
No scripts, multiple statements, DDL/DML, procedures, user-defined or remote
functions, ML/AI, external/federated or cross-region queries, uploads, or permanent
destinations: these can escape the scan-charge model. Apply the shared protocol's
outcome exclusions to filtering, joins, seeds, and thresholds as well as output.

Keep SQL, profiles, plans, parameters, and raw results in the ignored
`.bigquery-investigation/` directory; never commit credentials or private values.
Do not interpolate record data into SQL, shell code, identifiers, or paths.
Resolve the bundled helper relative to this skill:

```bash
python3 <bigquery-query-skill-path>/scripts/query_plan.py \
  --profile .bigquery-investigation/profile.json \
  --sql-file .bigquery-investigation/query.sql \
  --source-table SOURCE_PROJECT.DATASET.TABLE \
  --maximum-bytes-billed APPROVED_PROFILE_CEILING_OR_LOWER \
  --parameter 'seed:STRING:VALUE'
```

Repeat `--source-table` for each reviewed source and `--parameter` for each named
scalar value; omit parameters when unnecessary. Unsupported identifiers or
parameter forms need a reviewed extension, not a bypass.
The helper validates local configuration and declared sources, not SQL semantics,
cloud policy, or user consent. It only produces capped argument lists and
fingerprints; it neither authenticates nor executes queries. Its bundled empty
`assets/empty.bigqueryrc` overrides personal CLI query defaults; keep it empty
and use the generated arguments unchanged.

## Dry-run and request approval

Run `dry_run_argv` first with reviewed SQL on stdin, using literal arguments or a
subprocess argument list, never `eval` or unchecked extra flags. Retain
`--dry_run=true`, `--use_cache=false`, and the positive `--maximum_bytes_billed`.
Dry runs do not incur query-processing charges or consume query slots.
Use the same SQL, parameters, project, and location for the proposed execution.

Stop on failed, missing, or unreliable estimates, including misleading zero-byte
estimates for row-policy-protected sources. Estimates may be upper bounds for
clustered tables. If over cap, narrow within authorized scope or report blocked;
never automatically raise limits.

Show purpose, inspectable SQL, sources, time window, project/location, estimated
bytes/GiB, exact cap, and result handling. For on-demand pricing, show estimated
scan cost and the scan-charge ceiling using `bytes / 2^40 * regional price per TiB`,
including rounding and the 10 MB minimum per referenced table and per query.
Stop if minimums exceed the cap or current pricing/currency cannot be verified.
See [cost controls](https://docs.cloud.google.com/bigquery/docs/best-practices-costs)
and [pricing](https://cloud.google.com/bigquery/pricing).

Do not subtract assumed unused free-tier usage or promise a cache hit makes a
query free. Sandbox quotas apply only to a verified billing-disabled sandbox.
`LIMIT`, `--max_rows`, timeouts, or cancellation are not scan caps; quotas are
approximate and budget alerts do not stop spending. A submission's scan ceiling
does not cover other account usage or guarantee an all-services invoice total.

Use the user-input mechanism, such as `ask_user`, to approve this one submission,
including its cap/cost ceiling. Offer execute, revise, or decline. Without an
explicit answer from the user, do not execute: setup, investigation requests, a profile,
another agent, or a generated approval file are not consent. This applies even
to sandbox, cached, or repeated queries; approval is not for a batch or schedule.

## Submit once and record

Immediately before submission, revalidate identity/environment and bind approval
to SQL/parameter fingerprints, profile, project/location, sources, cap, and result
handling. Load SQL once, recompute the plan, compare `plan_sha256` to the approved
plan, and pass that same in-memory text on stdin. Any change needs a new dry run
and approval.

Submit unchanged `execution_argv` once, retaining its positive server-enforced
`--maximum_bytes_billed` at or below the profile ceiling, even for a small estimate.
BigQuery rejects ordinary on-demand queries whose estimated billed bytes exceed
the cap without a charge. No automatic retries, limit increases, or uncapped
CLI/console/client-library, project, identity, or pricing-model fallbacks.

On timeout or ambiguous submission, inspect the existing job's metadata before
proceeding; if no job can be identified, report uncertainty rather than resubmit.
Authentication, quota, or billing failures stop execution. Cancellation does not
guarantee a refund.

Record job ID, project/location, query/parameter hashes, approved cap, estimate,
status/errors, actual bytes processed/billed, cache hit, and fetched/total rows.
Use known-job metadata such as `bq show --job=true`, not new SQL to inspect charges.
Keep raw results local, label truncation, and agree on retrieving more rows from
the same job rather than rerunning SQL. Pass observational results through safe
ingestion with provenance, coverage, missingness, and truncation before exposing
data-origin text. Return to the chosen method, not an automatic report or
enforcement evaluation.
