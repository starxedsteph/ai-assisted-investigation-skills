---
name: investigation-{{DOMAIN}}
description: {{DESCRIPTION}}
---

# Investigation {{DOMAIN_TITLE}}

## Purpose

{{PURPOSE_AND_SCOPE}}

Keep the methodology platform- and dataset-agnostic. Define adapters and signals
from the supplied schema rather than assuming named datasets or field meanings.

## Shared protocol

Before inspecting data or applying these techniques, read
`../campaign-identification/SKILL.md` and follow its shared collaborative workflow,
evidence boundary, and outcome-blinding rules. This skill supplies domain
methods, not a separate investigation process. Apply the shared mandatory
data-ingestion gate whenever data is introduced for analysis; do not wait for a
separate request. Open existing databases read-only.

## Inputs and prerequisites

{{REQUIRED_AND_OPTIONAL_OBSERVATIONS}}

{{COVERAGE_PRECISION_AND_UNTESTABLE_CHECKS}}

## Investigation methods

### {{METHOD_HEADING}}

{{MEASUREMENT_UNIT_WINDOW_SUPPORT_AND_CONTROLS}}

{{BENIGN_ALTERNATIVES_AND_METHOD_LIMITATIONS}}

## Analysis methodology

{{ABSTRACT_SCHEMA_AND_FIELD_ADAPTER}}

{{DEDUPLICATION_VALIDATION_AND_PARAMETER_BINDING}}

{{PRACTICAL_CALCULATIONS_WITH_DIALECT_OR_PSEUDOCODE_LABEL}}

## Interpretation and limitations

{{DOMAIN_SPECIFIC_INFERENCE_LIMITS_AND_UNRESOLVED_EXPLANATIONS}}

Distinguish measured signals, candidate membership, and supported coordination
under the shared protocol. Package recorded findings with `investigation-results`
only when the human requests an export; do not automatically produce a report
or perform enforcement evaluation.
