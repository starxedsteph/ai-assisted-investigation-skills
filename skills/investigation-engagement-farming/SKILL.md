---
name: investigation-engagement-farming
description: Identifies coordinated engagement (stars, likes, upvotes, reviews) by analyzing interaction timing, shared target clusters, and account activity patterns. Use when investigating abnormal engagement spikes, sleeper accounts, or collusive endorsement rings. Automatically apply safe-data-ingestion whenever data is introduced for analysis; do not wait for a separate request.
---

# Investigation engagement farming

## Purpose

Investigate suspected engagement manipulation from a seed account or target.
Find repeatable timing, co-engagement, and account patterns; compare them with
ordinary activity. Report candidate groups and the evidence for each, not
unsupported claims about intent or operator identity.

Keep the methodology platform- and dataset-agnostic. Define adapters and signals
from the supplied schema; do not prescribe named datasets, platform-specific
fields, or publisher-specific filters.

## Shared protocol

Before inspecting data or applying these techniques, read
`../campaign-identification/SKILL.md` and follow its shared collaborative workflow,
evidence boundary, and outcome-blinding rules. This skill supplies engagement
methods, not a separate investigation process. Apply the shared mandatory
data-ingestion gate to every input; open existing databases read-only.

## Inputs and prerequisites

Use observed account-target interactions and event timestamps for timing and
overlap checks. Account creation, dormancy, and content comparisons require
actual account metadata and adequate observation history. Map fields through
the adapter in Analysis methodology; leave unavailable checks untested.

Aggregate counts support aggregate comparisons only. They cannot recover
shared account identities, within-account timing, or missing activity history.

## Investigation methods

### Timing signals

- Measure consecutive interaction times per account. Repeated fixed delta-t
  intervals can indicate robotic activity; report the period, tolerance, number
  of intervals, and matching fraction. Respect timestamp precision.
- Count arrivals per target in fixed time bins. Compare burst size and duration
  with the target's earlier activity and popularity-matched controls.
- Look for the same accounts engaging with multiple targets in the same short
  windows. Separate within-account periodicity from group-level synchronization.
- Check missing intervals and collection boundaries before calling an abrupt
  cutoff suspicious. Monthly counts cannot establish second-level timing.

### Co-engagement signals

Build an account-target graph from distinct endorsements. Find accounts sharing
several targets, and measure shared-target counts and Jaccard overlap:
intersection size divided by union size. State minimum support and the time
window before expanding from a seed.

Popular targets and shared interests create natural overlap. Compare with
controls matched on account activity and target popularity. Do not merge groups
through a popular bridge or assume transitive similarity establishes one ring.
A shared aggregate metric computed from allowed observations is at most a
candidate filter, not an identical account graph.

### Account indicators

- **Sleeper accounts:** Compare creation dates with a sudden return to activity
  after a long observed idle period. Old accounts alone are not suspicious;
  missing history does not establish dormancy.
- **Single-purpose accounts:** Compare endorsements with original content and
  other activity over the same observation window. Missing content data means
  unknown, not zero; legitimate readers may only endorse.
- **Clustered creation dates:** Measure account creation cohorts against normal
  signup rates. Check onboarding drives, migrations, and community events.

Require actual account metadata for these checks. First observed engagement is
not an account's creation date.

## Analysis methodology

Map available columns to the examples below.
Deduplicate export duplicates while preserving legitimate repeated reviews or
votes. Bind seed values as SQL parameters, never interpolate record contents.

For SQLite event data, use `interactions(account_id, target_id, event_time)` with
UTC timestamps that SQLite can parse. Report invalid timestamps separately.
Deduplicate by source event identity before using this table; do not collapse
different actions just because they share an account and timestamp. Preserve
simultaneous actions as zero-length intervals. Calculate within-account
inter-arrival times:

```sql
WITH times AS (
  SELECT account_id, unixepoch(event_time) AS t
  FROM interactions
  WHERE account_id IS NOT NULL AND unixepoch(event_time) IS NOT NULL
), deltas AS (
  SELECT account_id, t,
         t - LAG(t) OVER (PARTITION BY account_id ORDER BY t) AS delta_seconds
  FROM times
)
SELECT account_id, COUNT(*) AS intervals,
       AVG(CASE WHEN ABS(delta_seconds - :period) <= :tolerance
                THEN 1.0 ELSE 0.0 END) AS matching_fraction
FROM deltas
WHERE delta_seconds IS NOT NULL
GROUP BY account_id
HAVING COUNT(*) >= :minimum_intervals;
```

Count monthly arrivals for a seed target:

```sql
SELECT strftime('%Y-%m', event_time) AS month, COUNT(*) AS arrivals
FROM interactions
WHERE target_id = :seed AND unixepoch(event_time) IS NOT NULL
GROUP BY month
ORDER BY month;
```

Find target overlap with the seed, then inspect shared accounts and their event
times to check synchronization:

```sql
WITH edges AS (
  SELECT DISTINCT account_id, target_id FROM interactions
  WHERE account_id IS NOT NULL AND target_id IS NOT NULL
), sizes AS (
  SELECT target_id, COUNT(*) AS accounts FROM edges GROUP BY target_id
), overlap AS (
  SELECT other.target_id, COUNT(*) AS shared_accounts
  FROM edges AS seed
  JOIN edges AS other ON seed.account_id = other.account_id
  WHERE seed.target_id = :seed AND other.target_id <> :seed
  GROUP BY other.target_id
)
SELECT o.target_id, o.shared_accounts,
       1.0 * o.shared_accounts /
       (s.accounts + seed_size.accounts - o.shared_accounts) AS jaccard
FROM overlap AS o
JOIN sizes AS s ON s.target_id = o.target_id
JOIN sizes AS seed_size ON seed_size.target_id = :seed
WHERE o.shared_accounts >= :minimum_shared
ORDER BY jaccard DESC, o.target_id;
```

With Pandas, parse timestamps using `pd.to_datetime(..., utc=True,
errors="raise")`, sort by account and time, and use
`groupby("account_id")["event_time"].diff()` for deltas. Use distinct
account-target pairs for overlap, not raw duplicate rows.

For aggregate-only data, sum recorded monthly counts instead of counting rows.
Validate numeric text before conversion; SQLite `CAST` can silently turn
malformed strings into zero. In safely ingested data, validate the
`<untrusted_record>` wrapper and parse only numeric/date payloads. Keep
identifiers escaped and wrapped.

For aggregate tables, list the full metric-matched group separately from any
narrower same-period group. Equal
fractions do not prove equal engagement counts, shared accounts, or a single
campaign. Do not treat absent period rows as observed zero activity.

## Interpretation and limitations

Natural viral growth may involve varied account ages and a gradual, sometimes
power-law-like decay after publicity. Synthetic campaigns may show homogeneous
cohorts, repeated schedules, or abrupt starts and stops. Neither shape is proof:
announcements can synchronize real users, while campaigns can imitate decay.

Check publicity, scheduled automation, community events, sampling, and timezone
effects within the shared evidence boundary. Without account-level data,
within-account cadence and shared-account explanations remain untested.

Distinguish measured signals, candidate membership, and supported coordination
under the shared protocol. Package recorded findings with `investigation-results`
only when the human requests an export; do not automatically produce a report
or perform enforcement evaluation.
