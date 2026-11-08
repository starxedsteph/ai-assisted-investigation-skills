---
name: scaffold-investigation-skill
description: Creates or standardizes domain investigation method skills using this repository's shared format, protocol, template, and authoring checklist. Use whenever adding a new investigation technique, scaffolding an investigation-* skill, or bringing an existing domain investigation skill into the standard format. Not for conducting investigations or creating ingestion, results, or enforcement utility skills.
---

# Scaffold investigation skill

## Authoring scope

Create a domain method skill, not a new investigation workflow. Use the format
below and read `assets/SKILL-template.md` for the starting document. Resolve the
template path relative to this skill's directory.

Resolve `<skills-root>` to the destination's skill collection directory:
`skills/` in this repository, or the supported skill directory for an installed
collection. Read `<skills-root>/campaign-identification/SKILL.md` and
`<skills-root>/safe-data-ingestion/SKILL.md` before authoring. Read a neighboring domain skill
for comparable methods if useful. These are authoring references, not permission
to inspect datasets or outside research. Do not start an investigation, acquire
data, inspect raw rows, or infer dataset-specific facts while scaffolding.

Use this standard only for domain method skills. Keep shared protocol,
ingestion, results, and enforcement evaluation skills in their separate formats.
When changing an existing method skill, preserve its name, domain methods,
examples, cautions, and human edits; reorganize rather than replace its content.
Compare against the original after reorganizing. Keep triggers, measurements,
thresholds, queries, evidence rules, and workflow unchanged unless the user
explicitly requests a behavioral change. A format change is not permission to
add analytical requirements or alter how the investigation proceeds.

## Establish the domain

Identify the question the new method answers, its scope boundary, and the
observations required to answer it. Use the user's supplied requirements first.
Ask only for unresolved choices that materially affect the skill, such as
whether the method covers on-platform observations or authorized cross-venue
linkage. Do not invent field meanings, data availability, or supported
conclusions.

Choose `investigation-<domain>` as the lowercase kebab-case name and use the
same directory name. Use the template's `name` and `description` frontmatter
fields in that order. Write a one-line YAML description explaining what it does
and the requests that should trigger it; quote the string when YAML punctuation
requires it. Distinguish adjacent skills so the new description does not claim
every investigation task. Keep dependencies and prerequisites in the body.

Use one level-one title derived from the name: replace hyphens with spaces and
capitalize its first letter, for example `# Investigation example domain`.

## Build the skill

Create `<skills-root>/investigation-<domain>/SKILL.md` from the bundled template
and fill every `{{PLACEHOLDER}}`. Do not overwrite an existing skill without
authorization. Preserve the six level-two headings in their exact order and use
sentence-case, unnumbered method subheadings at level three or deeper:

| Heading | Content |
| --- | --- |
| Purpose | The question answered, scope, intended candidate findings, and boundaries with adjacent skills. |
| Shared protocol | The template's dependency paragraph, loading the campaign protocol before data inspection and using safe ingestion and read-only databases. |
| Inputs and prerequisites | Required and optional observations, established field meanings, coverage, precision, and checks left untestable when inputs are missing. |
| Investigation methods | Domain signal families with measurable definitions, support, comparisons or controls, benign alternatives, and caveats. |
| Analysis methodology | Schema adapters, deduplication, validated values, parameterized calculations, and practical SQL/dataframe steps or labeled pseudocode. |
| Interpretation and limitations | Supported versus exploratory conclusions, inference limits, unresolved explanations, and the results/export handoff without automatic reporting or enforcement evaluation. |

Do not leave sections empty; explain genuinely inapplicable requirements.
Replace method placeholders with as many useful signal families as needed,
rather than producing generic filler. Keep caveats close to the methods and
examples they qualify, even when the final section summarizes them.

Keep the Shared protocol section intact. The sibling protocol remains the
authority for collaboration, evidence boundaries, the explicit export gate,
blinding, corroboration, and expansion; the new skill supplies domain-specific
methods. Reference the shared rules rather than repeat them in each method.
Do not introduce alternative rules or a mandatory one-pass pipeline.

For each method, define its observation requirements, unit of analysis, window,
measurement, support/denominator, comparison or controls, and benign alternatives.
Explain what missing data or coarse timestamps prevent testing. Separate
candidate filters from corroborated coordination and avoid universal thresholds
or invented confidence probabilities.

Include a practical adapter and computational approach grounded in the supplied
schema, not a named dataset. Label SQL dialects where relevant; use bound
parameters and handle duplicates, missing values, invalid values, and timestamp
precision explicitly. Do not invent runnable examples that depend on unavailable
fields. Use explanatory pseudocode when no concrete execution environment is
specified.

Keep the core skill under 500 lines. Add bundled references, assets, or scripts
only when they serve the method, and link them from the skill with instructions
on when to read or use them. Do not duplicate the protocol or results template.
Check that sibling dependencies exist in the destination skills root. If they
are missing, report the dependency gap instead of claiming a standalone skill is
ready or copying in a different protocol.

## Check and deliver

Review the completed skill against this checklist:

- Confirm the name, directory, frontmatter, title, and six-section outline match
  the template; replace every placeholder and resolve resource links.
- Confirm each method has the observations, unit, window/precision,
  support/denominator, comparisons, and benign alternatives needed for its claims.
  Unknown is not zero, missing is not negative evidence, and annotations are not
  independent observations.
- Confirm adapters support the stated calculations, optional fields stay unknown,
  and examples use the appropriate SQL dialect or labeled pseudocode, bound
  parameters, and explicit duplicate and invalid-value handling.
- Confirm candidate filters are not proof of coordination, limitations constrain
  claims, and the shared workflow, evidence boundaries, and blinding rules remain
  intact. Do not invent calibrated confidence or operator attribution.
- When standardizing an existing skill, compare the original and revised content,
  including moved paragraphs and examples. Preserve its methods and workflow;
  new summaries must restate existing guidance, not add requirements.

Keep scaffolding, discovery, results packaging, and outcome evaluation distinct.
When changing the format, update this guidance, the template, and affected domain
skills together.

Update the destination's skill-authoring documentation when appropriate and
report the created or updated skill's path and scope concisely. Do not add an
investigation report, real findings, evaluation, or unrelated skill changes.
