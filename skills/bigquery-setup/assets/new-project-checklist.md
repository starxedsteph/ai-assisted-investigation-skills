**What this is and why**

BigQuery is Google's data warehouse. Some large public datasets we use in investigations live there, such as package-registry download and metadata records. To query them, you need your own Google Cloud project. Queries run in that project and count against its usage, even though the data belongs to someone else.

We'll use the free **BigQuery sandbox**, which doesn't need a credit card or billing account. According to [Google's sandbox documentation](https://docs.cloud.google.com/bigquery/docs/sandbox), it includes:

- **1 TiB of query processing per month for free.** This is the amount of data your queries read, not the size of the results.
- **10 GiB of storage.** We don't store data in BigQuery, so this doesn't matter for this setup.

If you go over the monthly allowance, the sandbox blocks further queries instead of charging you.

Here's everything you need to get BigQuery ready. You can follow along now, or do the console steps on your own and come back. I'll ask before running anything on your computer.

**Create the project**

1. Sign in to the [Google Cloud console](https://console.cloud.google.com/) and click **Create project**. You'll find it on the welcome screen or in the project picker at the top.
2. For **Project name**, enter `Investigation sandbox`. The **Project ID** fills in automatically from the name. You can edit it before you click **Create**, but you can't change it afterward.
3. For **Organization**, a personal Google account is fine, because this setup only queries public data. If you sign in with a work account, you may not see **No organization**, or you may not be allowed to create projects at all. If so, ask your admin for permission or switch to a personal account.
4. Click **Create**, select the new project, and copy its **Project ID** from the [Welcome page](https://console.cloud.google.com/welcome).
5. Check billing. Google sometimes links a billing account automatically when you create a project. For the free sandbox, open [Billing](https://console.cloud.google.com/billing), go to **My projects**, find your project, and choose **Actions > Disable billing** if billing is linked. If you chose to keep billing on, leave it linked. I'll double-check that billing matches your choice once the command-line tools are set up.

If the console looks different, Google's guides can help: [BigQuery sandbox](https://docs.cloud.google.com/bigquery/docs/sandbox) and [creating projects](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects).

**Set up the command-line tools**

With your OK, I'll install the Google Cloud CLI for you. It includes the `gcloud` and `bq` commands used to run queries. If you'd rather install it yourself, follow [Google's install guide](https://docs.cloud.google.com/sdk/docs/install).

After the install, and with your OK, I'll run these checks:

- `gcloud auth login` opens your browser so you can sign in with the same Google account. This lets the command-line tools act as you. I never see or store your password or tokens.
- `gcloud projects describe PROJECT_ID` confirms your account can see the new project.
- `gcloud billing projects describe PROJECT_ID` confirms billing matches your choice: off for the sandbox, or on if you chose billing.

**Query limits**

I recommend these starting limits. You can accept them or pick your own:

- **Scan limit: 100 GiB per query.** This is the most data a single query can read. A larger query is blocked rather than run. In the free sandbox this doesn't cost money, but it keeps one query from using up a big share of your 1 TiB monthly allowance.
- **Result limit: 1,000 rows.** This is the most rows brought back to your computer. It doesn't change how much data is scanned.

**Save your settings**

I'll save your project ID, location, chosen tables, and limits to `.bigquery-investigation/profile.json`. Git ignores that folder, so it won't be committed. It never contains passwords, tokens, or query results.

When you're ready, send me your Project ID and I'll take it from there.
