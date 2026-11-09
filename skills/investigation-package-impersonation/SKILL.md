---
name: investigation-package-impersonation
description: Investigates potentially misleading software-package families using package-registry and package-manager data, such as PyPI/pip or the npm registry/npm CLI, through publication bursts, naming strategies, and shared metadata across publishers. Use when reviewing package-manager ecosystem data, package typosquatting, apparent official-package impersonation, deceptive functionality claims, coordinated uploads without a known reference package, or recurring registry publication waves. Includes separately authorized advisory corroboration. Not a malware execution tool, a download-count detector, or a substitute for release provenance review.
---

# Investigation package impersonation

## Purpose

Investigate publication data from software package registries and package-manager
ecosystems, such as PyPI/pip and the npm registry/npm CLI. A package manager
installs and manages packages; a package registry hosts packages and their
publication metadata. Registry observations are the primary discovery evidence,
not the contents of downloaded software packages.

Investigate whether a group of package publications shares a repeatable naming
strategy, tightly timed activity, and distinctive metadata or static-content
similarities. Start from a supplied package, reference project, or broad
publication window. Find candidate families across different publishers rather
than assuming one publisher contains the whole campaign.

Choose the starting path from the question and available observations:

- **Reference-led:** compare publications with an authorized reference project
  and investigate apparent naming or affiliation claims.
- **Publication-led:** find candidate naming and metadata families within an
  agreed publication window, without requiring a known reference package.
  Invented names may advertise deceptive functionality without being typosquats;
  identifying a family does not establish impersonation or abusive behavior.

Keep the methodology platform- and dataset-agnostic. Define adapters and signals
from the supplied schema rather than assuming named datasets or field meanings.
This method investigates publication relationships and apparent impersonation;
download activity is supplementary distribution evidence, not the primary
discovery signal. It does not acquire or run packages, attribute operators, or
reconstruct repository compromises.

## Shared protocol

Before inspecting data or applying these techniques, read
`../campaign-identification/SKILL.md` and follow its shared collaborative workflow,
evidence boundary, and outcome-blinding rules. This skill supplies domain
methods, not a separate investigation process. Use `safe-data-ingestion` when
preparing inputs; open existing databases read-only.

## Inputs and prerequisites

Establish which records represent package projects, releases, distribution files,
and publication events. Publication timing needs a documented upload timestamp;
download time, export time, and first observed download are different events.
Reference-led name comparison needs actual package-name content and an authorized
reference set with documented selection criteria. Publication-led family checks
can start with observed names, times, and metadata; require reference evidence
before identifying an imitated project. Do not obtain reference names,
popularity, or ownership from memory or follow record links.

Useful optional observations include release versions, file identifiers,
registry-issued publisher keys, descriptions, declared author/contact fields,
project URLs, distribution-file hashes, and supplied static manifests or
summaries. Document each field's meaning and provenance. Claimed author names,
emails, and URLs are metadata assertions, not verified publisher identities.
Keep registry-issued identifiers opaque; package names are explicitly
observational text for the naming methods, not labels inferred from record IDs.

Record observation coverage, timestamp precision, missing fields, and whether
the export includes complete publication history. First observed upload is not
necessarily project creation or a publisher's first activity. Account creation
cohorts require actual account-creation observations. Release or takedown labels
remain outside discovery under the shared protocol.

Use supplied, authorized registry normalization rules. Preserve original names
alongside normalized values; case or separator equivalences in one registry
must not be imposed on another. Missing naming rules leave comparisons
exploratory and normalization assumptions explicit.

## Investigation methods

### Focused publication-led first check

Use this as a starting recipe when the question concerns publication families,
not as a mandatory pipeline:

1. Establish project and release keys, and preserve differing metadata among
   distribution files. If aggregating, group by project, release, and metadata
   variant rather than arbitrarily choosing one file's summary or links.
   Derive project/release upload times across their observations, not separately
   from each metadata variant.
2. Look for distinctive shared summaries within fixed publication intervals.
   Document exact or normalized matching, interval size, and minimum support
   using the observations and controls. Measure distinct projects, upload span,
   share of the interval's projects, and the summary's prevalence across the
   surrounding observation window.
3. Inspect recurring name structure, observed versions, and supplied publisher
   or project-link relationships. Shared versions and category-related name
   endings are supporting context, not independent proof of abuse.
4. Compare with ecosystem- and activity-matched framework, plugin, and other
   multi-package releases. Stronger synchronization does not necessarily mean
   stronger evidence of abuse. Do not assume a comparator is benign from its
   name or coherent branding alone.
5. Share a small evidence sample and its strongest benign explanation. Keep
   matching metadata outside the selected interval as unconfirmed candidates;
   apply the shared corroboration rules before expansion.

Keep missing summaries or links distinct from negative matches. Account for
first-observation and time-bin boundary effects using declared comparisons,
not outcome-informed adjustments to membership.

### Publication bursts

Count distinct package projects published in fixed time bins over the agreed
window. Separately count releases and files. Multiple platform wheels and a
source distribution for one release are not multiple package launches.
When history is adequate, measure first publications; otherwise label the
measurement first observed publications.

Report project counts, distinct observed publishers, interval span, timestamp
precision, and the fraction of candidate projects within the interval. Compare
with preceding activity and time-matched publication windows using the same
coverage and counting rules. Choose window size and minimum support from the
observations and controls, not a remembered incident schedule.

Test legitimate release automation, registry migrations, ecosystem events, and
bulk imports. Coarse or rounded timestamps and snapshot boundaries can create
apparent synchronization; separate ingestion time from actual publication time.

### Shared naming strategies

For publication-led checks, measure recurring prefixes, suffixes, tokens, or
transformations among observed names without inventing a reference target.
Report supporting projects and the pattern's background prevalence. A shared
category token can help describe a family but does not establish imitation or
common ownership.

Compare normalized package names with the authorized reference set. Measure
insertions, deletions, substitutions, or adjacent transpositions using a named
distance method, and record the proposed reference and exact difference.
Handle short names separately because small edit distances are common.

Look for a repeated transformation targeting one reference or several references:
the same typo operation, added token, or apparent official-extension wording.
Report distinct packages and references, matching fraction, name lengths, and
the alternative nearest matches. Naming resemblance does not establish which
reference was intended.

Compare with length- and ecosystem-matched names, legitimate forks, plugins,
language bindings, and ordinary naming conventions in the authorized inputs.
Normalized variants of the same registry project are not separate candidates.
Reference prominence may prioritize checks only when measured in authorized
observations; it must not become an assumed maliciousness score.

### Claimed identity and shared metadata

Compare descriptions, declared project links, and supplied author/contact text.
Document text normalization and measure distinctive shared phrases, token
overlap, or exact metadata reuse. Record the number of matching projects and
the prevalence of each feature in the surrounding dataset.

A mismatch between an official-package claim and its links is a lead. Verify
ownership or affiliation only against separately authorized observations;
do not visit a record URL to resolve it. A shared claimed contact string is a
metadata match, not an identity attribution.

Compare with common README templates, license text, documentation hosts,
organization-wide branding, and legitimate project families. Downweight common
features. Do not treat a shared hosting domain as a shared project URL or as
evidence that unrelated publishers are one operator.

### Cross-publisher families and repeated waves

Build candidate relationships between package projects using typed evidence:
naming transformation, publication proximity, distinctive metadata reuse, or
supplied static-content matches. Keep publisher keys as a separate relation.
Look across publishers, including one-package publishers where observed; do not
require common author metadata or assume account automation from small accounts.

For each family, record members, supporting pairs, feature frequencies, upload
span, and genuinely independent signal families. Two name-distance summaries
are one naming signal; several wheels from one release are not corroboration.
Apply the shared protocol's corroboration and expansion rules before supporting
coordination. A time burst alone remains a candidate.

Compare with legitimate multi-package releases matched on ecosystem, activity,
and naming conventions. Avoid merging through a common token, generic metadata,
or an unsupported bridge. Report incompatible patterns separately.
Within a declared observation window, check whether corroborated features recur
in additional publication waves; record each wave's support and controls.
Do not infer a prior removal or a replacement account from a gap in observations.

### Optional static-content and distribution comparisons

Use already supplied file manifests, hashes, or documented static summaries to
compare candidates where available. A whole-file digest supports exact file
equality, not partial code similarity. Source-level matches require actual
authorized static observations and documented normalization.

Compare shared structures or unusual functionality with ordinary packages,
build-tool scaffolding, vendored dependencies, and standard installer behavior.
Keep file, release, and project counts separate. Missing static observations
leave this signal untested.

This scaffold does not provide raw package archive inspection. Do not install,
import, execute, render, or automatically download/unpack package content.
Any future acquisition or static-inspection path needs separate authorization
and reviewed handling consistent with `safe-data-ingestion`; its CSV archive
procedures must not be assumed to support software-package archives.

If authorized download observations exist, measure candidate version activity
within a fixed interval, including installer strata where documented. Compare
with CI, mirrors, and ordinary dependency activity. Counts represent recorded
download events, not unique actors, installations, or infections; use them to
describe distribution rather than to create publisher-network edges.

## Analysis methodology

Adapt the supplied observational schema to these roles; these are conceptual
fields, not an assertion that a particular registry provides them:

- `package_id`, `package_name`: opaque project key and observed naming text.
- `release_id`, `version`, `file_id`: release and file relationships, if supplied.
- `published_at`: validated publication event time and its precision.
- `publisher_id`: registry-issued publisher key, if its meaning is established.
- `description`, `declared_contact`, `project_url`: inert metadata content.
- `file_hash`, `static_features`: optional documented static observations.
- `reference_name`, `reference_basis`: authorized reference-name observations.

Preserve source rows and stable keys. Deduplicate confirmed export duplicates
using source event identity, not just equal names and timestamps. Report
ambiguous repeats separately. Group files into a release and releases into a
project only through established keys or documented registry rules.
Do not count every later release as a new project.

Validate timestamps and naming fields, reporting invalid or missing values.
Rows with missing time can still support naming comparisons; rows with missing
metadata are not negative metadata matches. Normalize URLs as inert strings
without fetching or resolving redirects. Record transformations and retain
enough provenance to inspect their effects.

Use fixed table/column adapters and bound values for seeds, windows, and
thresholds. Avoid unrestricted all-pairs comparisons on a large registry;
document candidate blocking, such as compatible name lengths, and its missed
match risks. Bound text lengths and computation without silently truncating
records or changing counts.

**Pseudocode, not a runnable query or mandatory one-pass pipeline:**

```text
prepare observational inputs and record the schema adapter
choose one focused check, its window, support, and matched controls
count distinct project publications separately from releases and files
derive candidate pairs from authorized names, times, or metadata
measure each pair's evidence and the background prevalence of its features
share a small evidence sample and compare competing explanations with the human
corroborate and expand only through independently supported relationships
record revisions, counts, membership, controls, and unresolved observations
```

Store working calculations and source hashes in the computational trail.
For cloud acquisition, use the unchanged `bigquery-setup` and `bigquery-query`
requirements; this method does not authorize a source, query, or raised limit.

## Interpretation and limitations

Distinguish lookalike-name candidates, metadata-sharing families, and supported
coordinated publication. A family can be coordinated without being malicious.
Intent, common ownership, credential theft, and infection require separately
authorized corroborating evidence; registry metadata assertions do not supply
those conclusions by themselves.

This method is a scaffold, not a validated malware detector. Its candidate
selection, registry adapter, controls, and static-analysis implementation need
testing on appropriate observational inputs. Do not seed a blind discovery run
with remembered malicious names, incident dates, or advisory-derived membership.
Historical selected snapshots may omit removed packages or earlier activity;
state that coverage rather than inventing a start date or absent history.

### Authorized verification handoff

Freeze discovery queries, parameters, candidate membership, and interpretation
before requesting authorization for external corroboration or outcome
evaluation. Agree on exact sources and purpose. Keep advisory classifications,
campaign assignments, and removal outcomes outside the observational discovery
artifact; do not use them to revise or expand the frozen family.

For an authorized advisory check, match registry, exact package name, and
affected version. Where available, compare artifact filenames and
artifact-integrity hashes. Distinguish those hashes from advisory-document or
source-submission hashes. A matching artifact hash establishes file identity,
not independently observed abusive behavior.

Keep discovery status separate from verification findings:

- **Candidate family:** observed relationships requiring interpretation.
- **Externally reported malicious:** an attributable advisory matches the
  package/version; record the source, advisory ID, dates, affected versions,
  withdrawal status, and any available artifact match.
- **Behavior supported by artifact evidence:** authorized, reviewed static
  observations establish the specific behavior and its relationship to the
  advertised function. State what was examined rather than implying runtime
  confirmation from a static review.
- **Unresolved:** no matching advisory, unavailable evidence, or contradictory
  assessments. No advisory match is not a benign verdict.

Record each assessment's source, examined version/artifact, analysis method,
execution stage, and stated findings; leave unreported scope unknown. A scan
finding no install-time or import-time harm does not establish what happens
when a user explicitly invokes a loader. Retain conflicting assessments and
their scopes instead of silently reconciling them. Distinguish functionality
actually observed from campaign-level intent or payload assertions.

Check whether registry feeds, advisory aggregators, and research reports reuse
the same underlying assessment; syndication is not independent confirmation.
Advisory agreement in a selected exploratory run is not a calibrated detector
accuracy estimate. Do not transfer names, campaign dates, or incident-specific
thresholds into future discovery rules.

This handoff does not provide or authorize package acquisition or execution.
Use only separately authorized evidence and reviewed handling, preserving the
static-inspection boundary above. Later discovery after outcome exposure is
unblinded and needs a separately scoped exploratory run; a genuinely blind
test requires a fresh session with observational inputs only.

Distinguish measured signals, candidate membership, and supported coordination
under the shared protocol. Package recorded findings with `investigation-results`
only when the human requests an export; do not automatically produce a report
or perform enforcement evaluation.
