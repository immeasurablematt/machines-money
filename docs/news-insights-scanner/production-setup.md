# Production Setup: Daily Digest to Google Doc

> **PAUSED (2026-06-10).** The daily digest is parked while the project focuses on the free
> DeFi dashboard. The scheduled run in `.github/workflows/daily-digest.yml` is disabled and
> the required GitHub Actions secrets are not configured, so this setup is not live. This
> guide is kept for whenever the digest is resumed. See the README "Paused work" section.

This guide takes the scanner from manual runs to production: every morning,
GitHub runs the scanner against the live X list and saves the digest as a new
Google Doc in baggetta@gmail.com's Drive.

How it works:

1. A GitHub Actions workflow (`.github/workflows/daily-digest.yml`) runs daily
   at 11:00 UTC (7:00 AM US Eastern in summer).
2. It runs the scanner with live X API ingestion.
3. It sends the digest to a small Google Apps Script "webhook" that runs as
   baggetta@gmail.com and creates a Google Doc named
   `Machines & Money News Digest YYYY-MM-DD` in a Drive folder you choose.

There are three one-time setup steps. None require a developer.

## Step 1: Create the Drive folder

Signed in as **baggetta@gmail.com**:

1. In Google Drive, create a folder for the digests (for example
   `M&M Daily Digests`).
2. Open the folder and copy the **folder ID**: it is the long string at the
   end of the browser URL, after `/folders/`.

## Step 2: Deploy the Apps Script webhook

Signed in as **baggetta@gmail.com**:

1. Go to [script.google.com](https://script.google.com) and click
   **New project**.
2. Delete the placeholder code and paste in the full contents of
   `scripts/apps_script/digest_webhook.gs` from this repo.
3. At the top of the pasted code:
   - Replace `PASTE_DRIVE_FOLDER_ID_HERE` with the folder ID from Step 1.
   - Replace `PASTE_A_LONG_RANDOM_TOKEN_HERE` with a long random password
     (30+ characters; a password manager can generate one). Keep it handy for
     Step 3.
4. In the left sidebar, click the **+** next to **Services**, choose
   **Drive API**, and click **Add**. (This makes the digest arrive as a
   nicely formatted Doc. If you skip it, the digest still arrives, just as
   plain text.)
5. Click **Deploy > New deployment**, choose type **Web app**, and set:
   - **Execute as:** Me
   - **Who has access:** Anyone
6. Click **Deploy**, approve the permissions prompt, and copy the
   **Web app URL**. Keep it handy for Step 3.
7. Quick check: paste the Web app URL into a browser tab. You should see
   "Machines & Money digest webhook is live."

The "Anyone" setting only means anyone with the secret URL can send a POST to
the script; the script also rejects any request that does not include the
shared token, and it can only create docs — it cannot read existing Drive
files beyond the digest folder.

## Step 3: Add the three GitHub secrets

In the GitHub repo, go to **Settings > Secrets and variables > Actions** and
add three **repository secrets**:

| Secret name | Value |
| --- | --- |
| `X_BEARER_TOKEN` | Bearer token from the X developer portal (developer.x.com) with read access to lists. |
| `DIGEST_WEBHOOK_URL` | The Web app URL from Step 2. |
| `DIGEST_WEBHOOK_TOKEN` | The random token you pasted into the script in Step 2. |

## Test it once

In the GitHub repo, go to **Actions > daily-news-digest > Run workflow**.
Within a few minutes:

- A new Google Doc should appear in the Drive folder from Step 1.
- If the run fails, open the failed step in GitHub — the error messages are
  written in plain English (for example, a missing or invalid X token).

After a successful manual run, the schedule takes over: a fresh digest Doc
every morning, no terminal involved.

## Changing things later

- **Delivery time:** edit the `cron` line in
  `.github/workflows/daily-digest.yml`. Times are in UTC.
- **Number of items:** edit `--top-n 12` in the same file.
- **Rotating the token:** generate a new random string, update it in both the
  Apps Script code (then **Deploy > Manage deployments > Edit > New version**)
  and the `DIGEST_WEBHOOK_TOKEN` GitHub secret.
- **A new Apps Script deployment URL** is only needed if you redeploy as a
  *new* deployment; editing an existing deployment keeps the same URL.

## Safety behavior

- If the X token is missing or invalid, the scanner records
  `manual_review_needed` and the delivery step **fails the workflow loudly**
  instead of sending Ian an empty doc. GitHub emails the repo owner about
  failed scheduled runs.
- Every run's raw `digest.md` and `digest.json` are kept for 30 days as a
  workflow artifact on the run page, so nothing is lost if delivery fails.
