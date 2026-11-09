# AI investigation skills

Agent Skills for human-guided, evidence-based investigations in public data.
They help an AI agent prepare untrusted inputs,
measure patterns, test competing explanations, and export evidence with clear
limitations. They are investigation guidance, not an autonomous abuse detector,
a malware scanner, or a system for taking enforcement actions.

The collection currently includes engagement manipulation, fake-review, and
package-publication family methods and can be extended to other investigation domains. Methods are
platform- and dataset-agnostic; conclusions depend on the available evidence.
Suspicious patterns are leads, not proof of wrongdoing.

## Choose a skill

| Skill | What it is for | What to supply or expect |
| --- | --- | --- |
| [`campaign-identification`](skills/campaign-identification/SKILL.md) | Shared investigation workflow: focused questions, timing, interaction graphs, content comparisons, controls, and corroboration. | A question or seed and safely prepared observational data. Produces iterative findings for discussion, not an automatic final report. |
| [`safe-data-ingestion`](skills/safe-data-ingestion/SKILL.md) | Defensive acquisition and preparation of untrusted CSVs or databases, including outcome-blind inputs and inert text handling. | Supplied files or an explicitly authorized download source. Requires schema checks, bounded parsing, sanitation, and a provenance audit. |
| [`investigation-engagement-farming`](skills/investigation-engagement-farming/SKILL.md) | Investigating stars, likes, upvotes, or similar endorsements through bursts, repeated timing, shared targets, and account patterns. | Account-target events and timestamps where available. Account-age and dormancy checks require actual metadata and observation history. |
| [`investigation-fake-reviews`](skills/investigation-fake-reviews/SKILL.md) | Investigating on-platform rating concentration, arrival surges, repeated review text, and reviewer activity. | Review identities, targets, ratings, bodies, dates, and reviewer keys where available. Purchase-verification checks require a documented field. |
| [`investigation-package-impersonation`](skills/investigation-package-impersonation/SKILL.md) | Investigating reference-led impersonation or publication-led families in software package-registry and package-manager data, such as PyPI/pip or the npm registry/npm CLI, through naming patterns, upload timing, and distinctive shared metadata across publishers. | Method scaffold using project/release relationships, publication timestamps, metadata, and registry naming rules. A reference set is needed to identify imitation, not to start family discovery. Separately authorized verification matches advisories and artifact identities while preserving conflicting assessments; this is not a validated malware detector or package-execution tool. |
| [`investigation-results`](skills/investigation-results/SKILL.md) | Explicitly requested saving or exporting of existing work, including provisional findings. | Recorded findings and an agreed output directory. Produces requested Markdown/CSV deliverables with a shared filename prefix; chat-only summaries stay in chat. |
| [`platform-enforcement-evaluation`](skills/platform-enforcement-evaluation/SKILL.md) | Separately comparing frozen candidates with supplied removals, restrictions, or suspensions. | An explicit evaluation request, frozen discovery results, and action observations. Does not perform enforcement or infer why an action occurred. |
| [`bigquery-setup`](skills/bigquery-setup/SKILL.md) | Choosing or creating a project with permission, finding its ID, choosing sandbox or optional billing with spending safeguards, and preparing CLI access, approved sources, a local profile, and conservative query limits. | Conversational, staged setup with human decisions about project, billing, location, sources, pricing, and caps. Does not enable billing automatically or run a test query; budget alerts are not hard spending limits. |
| [`bigquery-query`](skills/bigquery-query/SKILL.md) | Planning, estimating, and submitting explicitly approved read-only BigQuery queries. | A configured profile and reviewed SQL. Requires a dry run, a positive server-enforced byte cap, and fresh human approval for each submission. |
| [`scaffold-investigation-skill`](skills/scaffold-investigation-skill/SKILL.md) | Creating or standardizing another domain method using the shared protocol and template. | A domain question, scope, and required observations. Authors a skill; does not investigate a dataset. |

## Install and load

All source skill bundles live under [`skills/`](skills/), with each entry point
at `skills/<skill-name>/SKILL.md`. This is the repository's distribution layout,
not a promise that an agent automatically indexes a plain `skills/` directory.
Use an agent that supports the [Agent Skills format](https://agentskills.io/)
and local file access.

Copy the **contents of `skills/`** into a supported location, so the resulting
path is `<supported-location>/<skill-name>/SKILL.md`, not
`<supported-location>/skills/<skill-name>/SKILL.md`:

| Agent | Project location in the repository being investigated | Personal location on the local machine |
| --- | --- | --- |
| GitHub Copilot CLI | `.github/skills/`, `.claude/skills/`, or `.agents/skills/` | `~/.copilot/skills/` or `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |

For example, from this checkout, after reviewing the skills and checking that
the destination has no conflicting skill folders:

```bash
mkdir -p /path/to/target-project/.github/skills
cp -R skills/. /path/to/target-project/.github/skills/
```

Install the complete collection together to preserve sibling dependencies such
as `../campaign-identification/SKILL.md`. If installing a subset, also install
every referenced sibling skill into the same location. Keep bundled assets,
scripts, and tests, not just `SKILL.md`. The repository has no package build step;
when distributing a skill folder or archive, preserve its internal structure
and supply its sibling dependencies separately in that same skills location.

For Copilot CLI, start a new session or use `/skills reload`, then
`/skills info investigation-engagement-farming` to confirm the loaded location.
To use this checkout without copying, use `/skills add` to configure the
absolute path to this checkout's `skills/` directory as an additional location,
then reload and check the skills. See the
[Copilot CLI setup guide](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills).

The GitHub Copilot app makes configured repository and CLI skills available;
manage them through **Customize > Skills**, as described in the
[app setup guide](https://docs.github.com/en/copilot/how-tos/github-copilot-app/customize-github-copilot-app).
For Claude Code, start a session in the target project and invoke
`/investigation-engagement-farming`; see
[Claude Code skill locations](https://code.claude.com/docs/en/skills#choose-where-skills-load).
Local personal skills are not automatically available to remote or cloud
agents. Follow the setup guide for that execution surface.

Consumers of the previous root-level layout must update source paths to
`skills/<skill-name>/`. No duplicate root-level bundles or compatibility aliases
are provided.

Ask your agent to use a skill by name, or let it select one from your request.
These are instructions and helpers, not a standalone application; the agent
needs appropriate analysis tools, such as Python or SQLite. Consult its
documentation for installation details and tool permissions.

## Use the investigation workflow

1. **Define the question.** Supply your files or authorize a specific source, and
   agree on the scope. Browsing, enrichment, and cloud spending need separate
   permission.
2. **Prepare the data.** Use `safe-data-ingestion` to create safe observational
   inputs without labels or outcomes. For blind discovery, give a fresh session
   only those prepared inputs; previously seen results cannot be unseen.
3. **Investigate together.** Start with a focused check, discuss the evidence and
   limitations, and refine the next question. Keep findings, tables, and summaries
   in chat; necessary scoped working artifacts can still support analysis.
   Compare alternative explanations rather than treating a suspicious pattern
   as proof.
4. **Save findings when needed.** Explicitly request saved files or an export;
   "summarize what we found" alone does not authorize files or deliverable updates.
   Provisional snapshots are allowed without ending exploration. Keep provisional
   candidates and unresolved questions explicit.
5. **Evaluate separately, if requested.** Freeze discovery before comparing it
   with supplied labels or platform actions. Those outcomes are not ground truth.

### Example requests

With safely prepared observational data:

> Use investigation-engagement-farming to check whether target `target-a` shares
> accounts with other targets during this burst. Show a first comparison and its
> limits before expanding.

> Use investigation-fake-reviews to check repeated text across products and
> same-day reviewer activity in this CSV.

> Use investigation-package-impersonation to find candidate families in this
> publication metadata. Compare shared summaries and upload timing with ordinary
> multi-package releases; keep advisory verification separate from discovery.

To save existing work:

> Use investigation-results to save our current findings under `outputs/` as
> "Shared Target Bursts", with a Markdown summary and useful supporting CSVs.

## Data used in development trials

Development trials used two public research sources:

| Source | Sample | Checks exercised |
| --- | --- | --- |
| [StarScout](https://github.com/hehao98/StarScout), `data/240701/` exports | 12,141 repository rows and 43,818 monthly-star rows. | Safe ingestion, aggregate engagement comparisons, and candidate filtering. |
| [Fake reviews data](https://github.com/bretthollenbeck/fake-reviews-data), Amazon reviews export | First 10,000 reviews in publisher order, not a random sample. | Safe ingestion, rating and text measurements, reviewer activity, and exploratory arrival bursts. |

Separate synthetic fixtures checked text and URL handling, instruction-like
payloads, unsafe archives, resource limits, and timing SQL. BigQuery's bundled
tests cover its local planning helper, not live cloud execution.

These were limited development checks, not a detection-accuracy benchmark or
end-to-end validation of every skill. Historical trials exposed publisher labels
or outcomes and do not validate the current blind-discovery workflow. No datasets
or dataset-specific ingestion scripts are bundled here.

## BigQuery access and safeguards

BigQuery use requires the Google Cloud CLI (`gcloud` and `bq`) and Python 3.
Use `bigquery-setup` to configure access and limits, then `bigquery-query` to
prepare queries. If you do not have a project or know its ID, setup walks you
through selecting an existing project or creating one with permission, and
finding **Project ID** in the Google Cloud console. This is the project where
query jobs run, not necessarily the project storing the source tables.

Setup explains scan and result limits in plain language, recommends starting
settings, and asks you to accept or change them rather than calculate byte counts.
A scan limit is a maximum, not a payment amount; a result-row limit only bounds
retrieved output. Billing-disabled sandbox use prevents paid BigQuery usage in
that project, subject to sandbox limits, but does not cap spending elsewhere.
With billing enabled, a byte cap cannot guarantee a $0 charge. Positive scan
limits are required in both modes; zero does not mean "use only the free tier."
Remembering settings locally does not authorize any query execution.

- Billing is never enabled automatically.
- Each submission requires a dry-run estimate, a positive server-enforced
  `maximum_bytes_billed` cap, and fresh human approval.
- `LIMIT`, quotas, and budget alerts are not hard spending caps.
- Keep `.bigquery-investigation/` ignored and credentials out of version control.

See the individual skills for the full safeguards. The local helper tests need
neither credentials nor the Cloud CLI:

From this repository's root:

```bash
python3 -m unittest discover -s skills/bigquery-query/tests
```

For an installed copy, replace `skills` with the supported skill directory.

## Authoring and extending methods

Use [`scaffold-investigation-skill`](skills/scaffold-investigation-skill/SKILL.md) when
adding or standardizing a domain method. Start from its
[template](skills/scaffold-investigation-skill/assets/SKILL-template.md) and review
checklist. Extend the shared investigation protocol rather than duplicating it,
preserve existing behavior when reorganizing, and test methods against suitable
observations and controls.

For general skill creation, improvement, or evaluation, optionally install
Anthropic's
[`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator).
It is maintained upstream and is not required or bundled here.
