---
name: investigation-fake-reviews
description: Analyzes customer and user review datasets to detect artificial rating inflation, generic boilerplate text, velocity spikes, and unusual reviewer activity. Use when investigating suspected fake reviews, unverified rating clusters, or review manipulation. Automatically apply safe-data-ingestion whenever data is introduced for analysis; do not wait for a separate request.
---

# Investigation fake reviews

## Purpose

Investigate one platform using only its on-platform reviews, rating history,
and reviewer activity. Identify manipulation candidates,
not proven fraud or operator identity.

## Shared protocol

Before inspecting data or applying these techniques, read
`../campaign-identification/SKILL.md` and follow its shared collaborative workflow,
evidence boundary, and outcome-blinding rules. This skill supplies review
methods, not a separate investigation process. Apply the shared mandatory
data-ingestion gate to every input; open existing databases read-only.

## Inputs and prerequisites

Use observed review identities, target entities, ratings, bodies, timestamps,
and reviewer keys as available. Verification-ratio checks require a documented
purchase-verification field; cross-target reviewer checks require reviewer
identity. Map fields through the adapter in Analysis methodology.

Leave unavailable checks untested. Rating inflation and velocity comparisons
need observed baselines or comparable controls and known coverage, not just a
selected all-high-rating sample.

## Investigation methods

### Rating and velocity signals

- Use observed review ratings as inputs, not predicted manipulation scores.
- Compare rating distributions with the target entity's earlier distribution and
  activity-matched controls. Report counts, denominators, and missing ratings.
  Look for extreme positive concentration, bimodal low/high splits, and a lack
  of intermediate ratings. A polarized legitimate audience can produce these.
- Count arrivals in fixed time bins. Detect volume surges on normally
  low-activity targets, including the baseline rate, burst size, duration, and
  minimum support. Distinguish exported zeros from missing observation coverage.
- Check releases, publicity, seasonal demand, incentives disclosed by the
  platform, and export ordering only where exposed by the allowed input; leave
  unavailable explanations unresolved before attributing a spike to manipulation.
  An all-high-rating sample cannot establish population-level inflation.

### Text and content signals

- Flag vague boilerplate praise lacking specific attributes, actual usage, or
  concrete outcomes. Short text alone is insufficient: inspect safely escaped
  samples and compare with legitimate short reviews in the same language.
- Measure repeated keyword stuffing for search rank: unusually frequent target
  terms without substantive details. Repetition is a signal, not proof of intent.
- Normalize whitespace and case to find exact cross-target review body reuse.
  Keep originals as inert evidence. Separate export duplicates, common phrases,
  quotations, translations, and shared templates from distinctive copying.
- Measure text length outliers and template concentration. Account for ingestion
  escaping and quarantined text; do not count wrapper length as review length.

### Reviewer patterns

- Count distinct 5-star reviews per reviewer in short windows and across target
  entities. Report the window, unique review counts, and target count; repeated
  exports must not inflate activity.
- Compute unverified purchase ratios only where a documented purchase
  verification field exists. Divide unverified by known verification states and
  report unknown states separately. Absence of verification data is not evidence
  of an unverified purchase, and unverified does not mean fake.
- Compare account behavior with ordinary active consumers. High activity may
  reflect legitimate reviewing; require independent corroboration.

## Analysis methodology

1. Define an adapter from available fields to this abstract
   relation: `reviews(review_id, target_entity, reviewer_id, rating, review_body,
   timestamp, purchase_verified)`. Unavailable optional fields stay null.
   Validate numeric/date payloads before conversion, decode inert wrappers
   only for computation, and keep identifiers and rendered text escaped.
2. Deduplicate by source review identity; preserve distinct reviews by the same
   reviewer. Bind target values and thresholds, never interpolate record data.
3. Run these SQL templates on the validated adapter. Null-safe denominators
   avoid interpreting no observations as a zero rate.

Baseline rating distribution:

```sql
SELECT rating, COUNT(*) AS reviews,
       1.0 * COUNT(*) / NULLIF(
         (SELECT COUNT(*) FROM reviews
          WHERE target_entity = :target AND rating IS NOT NULL), 0
       ) AS known_rating_share
FROM reviews
WHERE target_entity = :target AND rating IS NOT NULL
GROUP BY rating ORDER BY rating;
```

Text length metrics and prespecified short-text outliers:

```sql
SELECT COUNT(review_body) AS known_bodies,
       MIN(LENGTH(review_body)) AS minimum_length,
       AVG(LENGTH(review_body)) AS mean_length,
       MAX(LENGTH(review_body)) AS maximum_length,
       SUM(CASE WHEN LENGTH(review_body) <= :short_length THEN 1 ELSE 0 END)
         AS short_bodies
FROM reviews WHERE target_entity = :target;
```

Daily arrival curve:

```sql
SELECT target_entity, CAST(timestamp AS DATE) AS day, COUNT(*) AS arrivals
FROM reviews WHERE timestamp IS NOT NULL
GROUP BY target_entity, CAST(timestamp AS DATE)
ORDER BY target_entity, day;
```

Use the database's documented date truncation equivalent if needed. Build a
complete calendar only within confirmed coverage, then compare daily counts with
the preceding 28-day mean and matched controls. A practical exploratory filter is
at least 5 arrivals, at least 5 times baseline, and baseline at most 1 per day;
these are tunable candidate thresholds, not universal fraud criteria. With a
dataframe, group by target and calendar day, reindex verified covered days, and
apply a shifted 28-day rolling mean. Report quartiles and upper/lower text length
outliers alongside raw counts; do not use length as a standalone classifier.

## Interpretation and limitations

Report rating, timing, text, and reviewer measurements separately from hypotheses
of manipulation. Apply the shared protocol's independent-signal and
benign-explanation checks before supporting campaign-level coordination.
On-platform patterns do not establish external recruitment, payment, common
ownership, or proven fraud. Missing staging evidence leaves those links untested.

Package recorded findings with `results-export` only when the human
requests an export; do not automatically produce a report or perform
enforcement evaluation.
