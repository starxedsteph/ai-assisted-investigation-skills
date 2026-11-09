---
name: bigquery-setup
description: Helps users set up BigQuery access for investigations of public datasets, including choosing or creating a project with permission, finding its project ID, a billing-disabled sandbox or optional billing with spending safeguards, CLI installation and authentication, an explicit location, chosen public source tables, and conservative query limits. Use when preparing BigQuery for first use, finding an execution project ID, fixing setup, or intentionally changing sources or limits. Does not run investigation queries, enable billing automatically, or authorize later executions.
---

# BigQuery setup

Prepare access and a local profile for [`bigquery-query`](../bigquery-query/SKILL.md),
not an investigation or query execution. This setup is for public datasets only,
such as those in `bigquery-public-data`; it does not cover private or
access-controlled sources. A personal Google account is acceptable. Read
`../campaign-identification/SKILL.md` and `../safe-data-ingestion/SKILL.md`
for scoping which public tables the investigation uses and for evidence handling.
Do not run a test query, including `SELECT 1`, to finish setup.

## Confirm the environment and access

Identify local shell versus Cloud Shell and check for installed `gcloud` and `bq`.
Start by asking whether the user already has a Google Cloud project to use.
If they do not know, guide them through the project steps below before asking
for an execution project ID. Collect setup decisions in stages rather than
presenting a form that assumes they already know every setting.
Keep explanations, links, and step-by-step guidance in conversational chat,
giving the next manageable step rather than a full setup questionnaire.
The exception is a user who needs to create a project: first present the
new-project checklist described below, then continue in stages.
Where the host requires a structured question tool, use it only for a short
question or confirmation; do not put the walkthrough in the form or bundle
unrelated decisions such as project creation and CLI installation.
Use plain language before technical names. Reuse decisions and source identifiers
the user has already supplied; obtain missing locations from table metadata
rather than asking them to understand or re-enter every setting. Recommend
starting settings with reasons, then ask for a short confirmation with an option
to change them. Do not make a novice fill out byte counts or a configuration form.
If they express confusion, explain the immediate decision before asking again.
A cancelled confirmation is not consent; do not repeat the same questionnaire
or treat a question about a setting as approval.
Explain and get the user's permission before installing tools, creating projects,
linking billing, enabling APIs, changing IAM or quotas, or switching/impersonating
identities. Never enable billing automatically to repair a setup or quota error.

## Choose or create the execution project

Explain that the **execution project** is the Google Cloud project where query
jobs run and query usage is accounted for. It may differ from the project that
stores the source tables. The **project ID** is its unique string identifier
(for example, `investigation-sandbox-123`), not its display name, numeric project
number, or a dataset ID. Do not inherit the CLI's active project or substitute
a public dataset's project for the user's chosen execution project.

### Use an existing project and find its ID

1. Direct the user to the Google Cloud console's
   [Welcome page](https://console.cloud.google.com/welcome) and have them sign in
   with the intended Google account.
2. Have them open the project picker at the top and select the project they
   intend to use. On the Welcome page, the project name, project number, and
   **Project ID** appear below the Welcome heading; ask them to copy **Project ID**.
   If the project is missing, suggest checking the account or asking their
   administrator for access, not creating a replacement automatically.
3. Confirm the copied ID and intended use with the user. Once CLI authentication
   is available, inspect only that project's metadata with
   `gcloud projects describe EXECUTION_PROJECT --format='value(projectId)'`.
   Report permission or lookup errors explicitly; do not switch projects.

See [finding project identifiers](https://docs.cloud.google.com/resource-manager/docs/view-update-projects#identifying_projects).

### Create a project only if needed

When the user says they need to create a project, present
[`assets/new-project-checklist.md`](assets/new-project-checklist.md) in chat
before asking anything else, as inline markdown rather than a code block.
Present it nearly verbatim so the instructions don't drift between sessions.
Only these changes are allowed:

- Omit steps the environment check already confirmed, such as the CLI install
  when `gcloud` and `bq` are present or sign-in in an authenticated Cloud Shell.
- Name the platform's install method in the CLI section, such as Homebrew
  (`brew install --cask google-cloud-sdk`) on macOS.
- Replace the recommended scan limit if source metadata shows a smaller
  task-sized value is enough.

The checklist is guidance, not permission. Installing tools, signing in,
running checks, and saving settings each still need the user's OK at the time.
When they return, follow the steps below to verify each item. Install with
their permission and fall back to the linked install docs if installation fails.
Explain what each command does before running it.

The rest of this section is reference for helping with creation itself.
Explain the proposed project name, intended organization/folder, and the chosen
sandbox or billing-enabled approach, then obtain explicit permission for creation.
The user may create it in the console themselves; agent-driven creation still
needs this permission. A general setup request is not permission to create it.

1. Once signed in to the [Google Cloud console](https://console.cloud.google.com/),
   the user can click **Create project** directly. The
   [sandbox setup steps](https://docs.cloud.google.com/bigquery/docs/sandbox)
   and [Manage resources](https://console.cloud.google.com/cloud-resource-manager)
   are backup routes. The user handles sign-in and any terms acceptance.
   Do not follow the tutorial's sample-query steps.
2. Suggest the project name `Investigation sandbox`. Explain that the
   **Project ID** fills in automatically from the name, can be edited before
   creation, and is permanent afterward. Avoid sensitive information in either value.
3. Select the intended organization/folder, or **No organization** if available.
   Work-managed accounts may not offer **No organization** or may block project
   creation. The user can ask their administrator for permission or use a
   personal Google account, which is fine for public data. The project creation
   **Location** refers to its organization/folder, not the BigQuery dataset region.
4. Google may link a billing account automatically at creation, even when the
   user intended a sandbox. If they chose a billing-disabled sandbox, have them
   check the project's billing and disable it if linked, as described below, then
   verify with `gcloud billing projects describe`.
   If they need paid features or their organization requires billing, explain
   the billing-enabled option and spending safeguards below and confirm their
   choice before linking an account, starting a paid trial, or upgrading.
   Billing is supported, but project creation alone is not billing permission.
5. Have the user click **Create**, select the new project, and copy its
   **Project ID** from the Welcome page as above. If creation is denied by
   permissions, organization policy, or project quotas, report the blocker and
   suggest asking their administrator or using a personal Google account; do
   not change IAM or quotas automatically.

With installed, authenticated CLI access, an alternative is
`gcloud projects create PROJECT_ID`, adding an explicit `--organization` or
`--folder` for the approved parent when applicable. Show the exact command and
confirm the ID and parent before running it; do not rely on an implicit parent.
Project creation requires `resourcemanager.projects.create`, commonly via
Project Creator, not a reason to request Owner or Editor.
See [creating projects](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects).

### Choose sandbox or billing with spending safeguards

Offer both approaches without treating billing as a setup failure:

- A [sandbox](https://docs.cloud.google.com/bigquery/docs/sandbox) avoids paid
  usage but has usage and feature limits and automatic table expiration.
- A billing-enabled project can support needs beyond the sandbox. Explain that
  usage can incur charges and agree on the user's intended spending allowance
  and safeguards; do not assume a new project or free trial prevents overspending.

Before linking billing, explain current regional query pricing, the intended
per-query bytes-billed cap, and the limits of daily quotas and budget alerts
described below. Distinguish the user's desired total spending allowance from
an enforceable per-query scan cap: this workflow cannot guarantee an account-wide
hard spending limit. If they require that guarantee, report the limitation
before they commit to billing.

For a user who chooses billing, confirm the exact project and intended billing
account without requesting payment details. Guide them to the console's
[Billing page](https://console.cloud.google.com/billing), select the intended
project, and follow its link/change billing account flow. They handle payment
details and terms themselves. Agent-driven linking still requires explicit
permission for that specific change. Report access or organization-policy
blockers rather than changing IAM or substituting another account.
See [enabling billing for a project](https://docs.cloud.google.com/billing/docs/how-to/modify-project).

## Verify billing, authentication, and sources

After confirming the execution project, ask which public tables the
investigation uses and its purpose. Help the user obtain missing source
identifiers or location from table metadata; do not enumerate unrelated
public datasets. Public datasets need no extra role grants; do not request
IAM changes to read them.

Verify the user's chosen billing status: a billing-disabled sandbox for someone
avoiding paid usage, or billing-enabled access with agreed spending safeguards.
For billing-enabled access, verify ordinary on-demand pricing, including
reservation assignments. Unknown or capacity/edition pricing blocks this
byte-capped workflow. Do not assume unused free allowance in a new project:
free usage may be shared at the billing-account level.

If billing is enabled but the user wants unpaid BigQuery use, explain that a
billing-disabled sandbox blocks paid BigQuery usage in that project, subject to
sandbox limits. It does not guarantee zero spending elsewhere on the account.
Offer a separate sandbox if the existing project has needed or shared resources.
If asked how to disable billing, guide them to Billing > My projects, find the
exact project ID, and choose Actions > Disable billing. Warn that disabling
billing can stop services and affect resources in that project; do not close the
billing account or change IAM to work around missing permissions. Agent-driven
unlinking needs separate permission. After the user reports completion, verify
that exact project's billing status with
`gcloud billing projects describe EXECUTION_PROJECT --format='json(projectId,billingEnabled)'`.

Use `gcloud auth login` only with permission when local CLI authentication is
needed; Cloud Shell may already be authenticated. The CLI has its own credentials;
Application Default Credentials are only needed for separately requested client
libraries. Never request, display, copy, or commit tokens, service-account keys,
or credential files. The creator of a new project already has the access needed
to run query jobs in it. Do not request Owner, Editor, BigQuery Admin, or other
role changes as part of this setup.
See [authentication and access](https://docs.cloud.google.com/bigquery/docs/authentication).

Inspect the chosen tables' metadata, not rows:

```bash
bq --project_id=EXECUTION_PROJECT --location=LOCATION --format=prettyjson \
  show SOURCE_PROJECT:DATASET.TABLE
```

Verify schema, type, location, coverage, and row-access policies. Do not use
`bq head`, Preview, or `SELECT *` as an access check. Views require review of
underlying sources and functions. The query workflow supports public native
tables, not external/federated, cross-region, remote-function, or ML-backed sources.

## Agree on limits and save the profile

Explain the two settings before requesting confirmation:

- **Scan limit:** the most data one query may bill for reading. BigQuery rejects
  an ordinary on-demand query estimated above this limit. It is a maximum,
  not a minimum spend or a payment amount. This workflow requires a positive
  scan limit even in the unpaid sandbox to keep each submission bounded.
- **Result-row limit:** the most result rows retrieved locally. It limits the
  output, not the amount scanned or query cost.

Distinguish billing from scan limits: a billing-disabled sandbox prevents paid
BigQuery usage in the project; billing-enabled queries can incur charges after
any available free allowance is exhausted. A positive scan limit does not
necessarily incur a charge. Zero is not a "free tier only" setting: an unset or
zero limit blocks this workflow, and a byte cap cannot guarantee a $0 charge
on a billing-enabled project.

Always propose concrete values the user can accept or override: by default a
100 GiB scan limit, which is a tenth of the sandbox's 1 TiB monthly free query
allowance, and 1,000 result rows. Lower the scan limit when source metadata shows
a smaller task-sized value is enough. Do not ask the user to pick values from
scratch or calculate bytes. For a sandbox,
explain the unpaid route first; do not frame the scan limit as a paid allowance.
For billing-enabled use, explain the proposed scan-charge ceiling at the current
regional [price](https://cloud.google.com/bigquery/pricing), including billing
minimums, and obtain explicit acceptance rather than choosing a paid allowance
on their behalf. Explain GiB/TiB only as needed; convert the accepted limit to
an exact positive integer byte count for the profile.

Example after verifying billing is disabled and confirming project, location,
and source: "Billing is disabled, so we're using the unpaid sandbox. I recommend
a 100 GiB scan limit for this query and retrieving at most 1,000 rows. If the query
is too large, it is blocked rather than the limit being raised automatically.
I'll remember these settings locally, without credentials or results. We will
estimate the query first and ask separately before running it." Then ask only
"Use these recommended settings?" with accept, change, or pause choices.
The recommendation is not an execution approval.

Every later submission, including
sandbox, cached, metadata SQL, or repeated queries, needs fresh user approval;
setup is not standing spending permission.

Offer [custom daily quotas](https://docs.cloud.google.com/bigquery/docs/custom-quotas)
as optional additional safeguards. Per-user quotas apply uniformly within a
project and daily resets use Pacific Time; quotas are approximate and may be
exceeded. Explain shared-project impact and verify approved changes.
Offer [budget alerts](https://docs.cloud.google.com/billing/docs/how-to/budgets)
at thresholds aligned with the user's intended spending allowance, explaining
their scope and notification delays. Creating a budget requires separate
permission; alerts monitor spending but do not stop charges.
Neither safeguard is an account-wide hard
budget: other users, projects, storage, reservations, taxes, and services remain
outside a per-query scan cap. Do not provision reservations, autoscaling,
scheduled queries, permanent results, uploads, cloud exports, or billing-export
pipelines under this setup.

Fill `assets/profile-template.json` into the agreed workspace's
`.bigquery-investigation/profile.json` after confirmation, preserving local edits.
This repository's `.gitignore` already excludes that folder; in another
workspace, confirm it is ignored before saving.
Describe this as remembering agreed settings locally, not as a separate technical
"profile" decision. A short confirmation may cover the explained limits and
saving them together; the choice of source tables and other unresolved decisions still
need their own clarification.
Store operational settings only, never credentials or rows. The template starts
with no project, sources, or execution allowance; leave unresolved values null
and report incomplete setup. `unverified` pricing, null/zero ceilings, and missing
caps block execution. The profile is configuration, not proof of consent.

Check local configuration without a cloud call:

```bash
python3 <bigquery-query-skill-path>/scripts/query_plan.py \
  --profile .bigquery-investigation/profile.json --check-profile
```

Report readiness, limits, and unresolved access/pricing questions; hand off to
`bigquery-query`. For later source or limit changes, show old/new settings and
obtain separate permission rather than automatically raising a ceiling.
