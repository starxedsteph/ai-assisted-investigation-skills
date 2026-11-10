---
name: platform-enforcement-evaluation
description: Compares independently identified candidates with observed platform actions, including removals, restrictions, and suspensions. Use when the user explicitly requests enforcement coverage, action timing, or a comparison between frozen investigation findings and supplied platform-action observations. Automatically apply safe-data-ingestion whenever action observations or other new data are introduced for analysis; do not wait for a separate request. Not for campaign discovery or performing enforcement.
---

# Platform enforcement evaluation

## Working together

Explore the human's evaluation question using already established candidate
findings and supplied platform-action observations. Share focused comparisons,
discuss uncertainty, and follow questions rather than automatically producing
a report. This skill measures observed actions; it does not remove content,
restrict accounts, or recommend sanctions.

Before inspecting data, read `../campaign-identification/SKILL.md` for the shared
collaborative workflow, evidence boundary, and mandatory data-ingestion gate;
open existing databases read-only.

## Evaluation boundary

Use this skill only for an explicitly requested evaluation, not automatically
after an investigation. Freeze the discovery input, queries, parameters,
candidate membership, and interpretation before exposing action outcomes.
If discovery already used those outcomes, disclose the leakage; do not present
the comparison as independent validation.

The authorized evaluation may read supplied action outcomes, but must not feed
them back into discovery filters, thresholds, membership, or conclusions.
Keep evaluation separate from the discovery session. Any later investigation
informed by these outcomes is no longer blind.

Remain platform- and dataset-agnostic. Map actual fields only when their meanings
are established within the authorized evidence scope. Do not browse for live
status or infer action reasons from labels or dataset reputation. Ambiguous
states, actors, reasons, and timestamps remain unknown.

## Evaluation methods

Join frozen candidates to action observations using opaque record or entity
keys. Match the unit of analysis: an account restriction is not proof that each
of its records was removed. Deduplicate snapshots without erasing state changes;
report unmatched candidates and ambiguous joins rather than dropping them.

Separate observed platform actions, author-initiated deletions, not-marked-actioned
records, and unknown states where the data distinguishes them. Absence of an
action marker is not a fresh check that an entity remains live or unrestricted.
Preserve reversals, appeals, and snapshot dates rather than assuming actions
are permanent.

Calculate action coverage among candidates with known, comparable states.
State the numerator, denominator, unknown count, unmatched count, and observation
date. No known states means an undefined rate, not zero. Compare cohorts at
similar observation ages and coverage; do not interpret a selected sample as
platform-wide performance.

Measure time to action only with observed event and action timestamps. Respect
their resolution, disclose negative intervals, and account for right censoring:
no action observed by the last snapshot is not proof that none occurred later.
Snapshot time is not action time.

Attribute actions to automation only when supplied provenance identifies it.
Otherwise describe observed action coverage, not automated detection accuracy.
Missing reasons, collection gaps, author deletions, and reversals limit
interpretation.

Platform actions and publisher classifications are not ground-truth misconduct
labels. Coverage is not precision or recall without independently established
truth and an appropriate evaluation population. Discuss agreements,
disagreements, and missing evidence without treating actioned candidates as
confirmed campaigns or unactioned candidates as benign.
