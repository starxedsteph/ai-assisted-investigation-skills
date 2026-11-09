# AI investigation skills

Agent Skills for user-guided, evidence-based investigations in public data.
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
| [`campaign-identification`](campaign-identification/SKILL.md) | Shared investigation workflow: focused questions, timing, interaction graphs, content comparisons, controls, and corroboration. | A question or seed and safely prepared observational data. Produces iterative findings for discussion, not an automatic final report. |
| [`safe-data-ingestion`](safe-data-ingestion/SKILL.md) | Defensive acquisition and preparation of untrusted CSVs or databases, including outcome-blind inputs and inert text handling. | Supplied files or an explicitly authorized download source. Requires schema checks, bounded parsing, sanitation, and a provenance audit. |
| [`investigation-engagement-farming`](investigation-engagement-farming/SKILL.md) | Investigating stars, likes, upvotes, or similar endorsements through bursts, repeated timing, shared targets, and account patterns. | Account-target events and timestamps where available. Account-age and dormancy checks require actual metadata and observation history. |
| [`investigation-fake-reviews`](investigation-fake-reviews/SKILL.md) | Investigating on-platform rating concentration, arrival surges, repeated review text, and reviewer activity. | Review identities, targets, ratings, bodies, dates, and reviewer keys where available. Purchase-verification checks require a documented field. |
| [`investigation-package-impersonation`](investigation-package-impersonation/SKILL.md) | Investigating reference-led impersonation or publication-led families in software package-registry and package-manager data, such as PyPI/pip or the npm registry/npm CLI, through naming patterns, upload timing, and distinctive shared metadata across publishers. | Method scaffold using project/release relationships, publication timestamps, metadata, and registry naming rules. A reference set is needed to identify imitation, not to start family discovery. Separately authorized verification matches advisories and artifact identities while preserving conflicting assessments; this is not a validated malware detector or package-execution tool. |
| [`investigation-results`](investigation-results/SKILL.md) | Explicitly requested saving or exporting of existing work, including provisional findings. | Recorded findings and an agreed output directory. Produces requested Markdown/CSV deliverables with a shared filename prefix; chat-only summaries stay in chat. |
| [`platform-enforcement-evaluation`](platform-enforcement-evaluation/SKILL.md) | Separately comparing frozen candidates with supplied removals, restrictions, or suspensions. | An explicit evaluation request, frozen discovery results, and action observations. Does not perform enforcement or infer why an action occurred. |
| [`bigquery-setup`](bigquery-setup/SKILL.md) | One-time BigQuery setup: project, CLI sign-in, and query limits. | Public data only. Gives new users a setup checklist and never turns on billing. |
| [`bigquery-query`](bigquery-query/SKILL.md) | Running approved read-only queries against public datasets. | Triggered by natural-language requests. Each query is estimated and approved before it runs. |
| [`scaffold-investigation-skill`](scaffold-investigation-skill/SKILL.md) | Creating or standardizing another domain method using the shared protocol and template. | A domain question, scope, and required observations. Authors a skill; does not investigate a dataset. |

## Install and load

Use an agent that supports the [Agent Skills format](https://agentskills.io/)
and local file access. Copy the complete skill folders into its supported skill
directory, such as `.github/skills/` for GitHub Copilot or `.claude/skills/` for
Claude Code. Keep bundled assets and scripts, not just `SKILL.md`.

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

The BigQuery skills let your agent query public datasets, such as Google's `bigquery-public-data`, as part of an investigation. Google's free [BigQuery sandbox](https://cloud.google.com/bigquery/docs/sandbox) includes 1 TiB of queries per month, so most investigations cost nothing. A personal Google account works fine.

**Set up once.** Ask your agent to "run BigQuery setup." If you don't have a Google Cloud project yet, it gives you a short checklist. With your permission, the agent installs the Google Cloud CLI, signs you in, and suggests query limits you can accept or change. Settings are saved locally in `.bigquery-investigation/`, which git ignores.

**Then just ask.** You don't need to do anything special to use `bigquery-query`. Ask in natural language, for example "find accounts that starred these repos in the same hour," and the agent writes the SQL. It estimates how much data the query will scan and asks before it runs.

Safeguards:

- Billing is never turned on automatically.
- Every query gets a size estimate, a hard per-query scan limit, and your approval before it runs.
- Budget alerts and quotas are not hard spending caps. In a project with billing on, a scan limit can't guarantee $0.

Neither the local helper tests nor setup checks require credentials:

```bash
python3 -m unittest discover -s <skills-directory>/bigquery-query/tests
```

## Authoring and extending methods

Use [`scaffold-investigation-skill`](scaffold-investigation-skill/SKILL.md) when
adding or standardizing a domain method. Start from its
[template](scaffold-investigation-skill/assets/SKILL-template.md) and review
checklist. Extend the shared investigation protocol rather than duplicating it,
preserve existing behavior when reorganizing, and test methods against suitable
observations and controls.

For general skill creation, improvement, or evaluation, optionally install
Anthropic's
[`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator).
It is maintained upstream and is not required or bundled here.
