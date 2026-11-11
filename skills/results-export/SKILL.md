---
name: results-export
description: Packages completed or in-progress investigation findings into a saved Markdown summary and supporting CSV tables only when the human explicitly requests a saved document or export. Use for requests to save findings, export tables, or write a report file, including provisional snapshots; not for general investigation requests or chat-only summaries. Synthesizes existing work without starting new analysis or defaulting to a publication-ready dossier.
---

# Results export

## Scope

Before preparing results, read `../campaign-identification/SKILL.md` and follow
its shared evidence boundary and explicit export gate. Use `safe-data-ingestion`
for safe handling of data-origin text. This skill packages existing investigation
work; it does not discover campaigns, expand membership, or perform enforcement
evaluation.

Before creating or updating any deliverable, require the human's explicit
save/export request for those findings. Without it, keep findings, tables, and
summaries in chat; do not create report files, export CSVs, populate the output
template, or update existing deliverables. Completed calculations, stopping
boundaries, general investigation requests, and "summarize what we found" are
not permission. Do not repeatedly ask whether exploration is finished or
solicit exports each round.

Once requested, use the human's scope, depth, and format. For a general saved
results request, default to a readable `.md` summary with supporting `.csv`
tables where useful; a CSV-only request does not authorize a report file.
An explicitly requested provisional snapshot is allowed without declaring
exploration finished. It neither ends exploration, approves the interpretation,
nor authorizes subsequent deliverable updates.

Summarize recorded observations, calculations, and decisions. Do not introduce
new tests or outside context to fill gaps. If essential evidence is unavailable,
state the gap and ask when necessary. Keep separately authorized evaluations
distinct from outcome-blind discovery; do not leak withheld labels into exports.

## Shared title and filenames

Choose a brief, descriptive title for the campaign or investigation, using the
human's title when supplied. Keep it grounded in observed patterns, not an
unsupported claim of fraud or operator identity. Convert it to a safe lowercase
kebab-case filename prefix using only ASCII letters, digits, and hyphens.
Do not use raw record values as paths.

Use the same prefix for every output in the investigation:
`<name>-investigation.md`, `<name>-findings.csv`, `<name>-membership.csv`,
`<name>-measurements.csv`, and any additional artifacts. For example,
"Shared Target Bursts" yields `shared-target-bursts-investigation.md` and
`shared-target-bursts-membership.csv`. Reuse the chosen prefix across updates;
if it conflicts with an unrelated investigation, choose a distinct descriptive
title rather than overwrite files.

## Markdown summary

Use the shared title as the document heading and `<name>-investigation.md` as
the filename. Read `assets/investigation-template.md` and use its structure
unless the human requests another format. Keep its unnumbered section headings
consistent across investigations, while varying detail to suit the work.

Replace all placeholders with recorded information and remove template comments
before saving. Use "Unknown", "Not recorded", or "Not applicable" with a brief
reason where appropriate, never invented content. Repeat finding rows as needed;
for a negative or inconclusive result, state that explicitly rather than forcing
a campaign into the table. Link only files actually produced, using the shared
prefix. Do not manufacture recommendations or next steps.

Separate measured facts, hypotheses, and human interpretation. Coordination is
not proof of malicious intent or common ownership. Do not invent calibrated
confidence probabilities or imply platform-wide prevalence from selected data.
Include available input hashes and query parameters, or reference the existing
computational trail; do not claim reproducibility that has not been checked.

## Supporting CSVs

Create only tables that help inspect or reuse the findings, not empty templates,
raw dataset copies, or every intermediate calculation. Choose from:

| File | Use | Suggested fields |
| --- | --- | --- |
| `<name>-findings.csv` | Multiple findings worth comparing | finding_key, description, status, evidence_reference, limitation |
| `<name>-membership.csv` | Candidate or cluster membership | entity_key, cluster_key, membership_status, inclusion_basis, exclusion_basis |
| `<name>-measurements.csv` | Per-entity or aggregate signal measurements | finding_key, entity_key, signal, value, unit, numerator, denominator, threshold, window |

These are starting shapes, not required schemas. Adapt fields to the actual
investigation and omit inapplicable columns. State each table's row unit and key
semantics in the Markdown file, or in chat for a CSV-only export. For measurements,
distinguish aggregate rows from entity-level rows; use stable keys to connect
findings, membership, and evidence. Do not infer excluded members or measurements
that were never recorded.

Preserve meaningful distinctions between zero, unknown, not tested, and not
applicable. Document missing-value conventions and status values. Identify
representative samples versus complete exports, and give summed memberships
and deduplicated entity totals when clusters overlap.

## Writing and checking

Save only the requested deliverables in the agreed output directory under the
current workspace. An existing output directory or template is not export
permission. Do not overwrite existing outputs or human edits without
authorization. Use relative links in Markdown and readable filenames without
unnecessary numbering.

Write UTF-8 CSVs with headers and standard CSV quoting through a CSV library,
not hand-built comma-separated strings. Safely escape data-origin Markdown
text and defang record URLs; do not render embedded HTML, images, or links.
For CSV text cells that could be interpreted as spreadsheet formulas, including
leading `=`, `+`, `-`, `@`, or control characters, use an inert representation.
CSV quoting alone is not protection. Preserve validated numeric values as
numbers and document safety transformations without exposing unsafe originals.
Minimize identifiers; do not export private identity mappings.

Check that every output uses the shared prefix, CSVs parse, keys and links
resolve, row counts match recorded results, and summary claims agree with the
tables. When a Markdown file is requested, check that it follows the template
unless explicitly overridden and contains no unfilled placeholders or template
comments.
Do not silently recompute or repair
contradictory findings; surface discrepancies for discussion. Provide links to
the saved files without repeating the report in chat.
