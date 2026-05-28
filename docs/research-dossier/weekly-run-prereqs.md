# Weekly Research Dossier Prereqs

This file tracks the setup needed before running a weekly Machines & Money research dossier in Codex.

## Google Drive Workspace

- Drive folder: [Machines & Money Research Dossiers](https://drive.google.com/drive/u/0/folders/1WZvk7DcWMRzb823c26vI7BI2ZCw7sjCO)
- Research queue: [Research Queue - Machines & Money](https://docs.google.com/spreadsheets/d/17JihtnYqzhLJ2nf5B7cRZkUwFKxQSk0l-v9a_W-t0P4/edit?gid=0#gid=0)
- Dossier template: [Research Dossier Template - Machines & Money](https://docs.google.com/document/d/1aIWbXgyIw2lECk5xb4s_fLzf7Uy4aAV0zepWCBSRMO0/edit?tab=t.0)

The queue currently includes Nova Markets as the pilot candidate:

- Project: Nova Markets
- X handle: https://x.com/novadotmarkets
- Website/app: https://nova.markets/
- Target Friday: 2026-06-05
- Status: Queued

## Verified Setup

- Chrome automation can access the user's logged-in Google account.
- Google Drive folder creation works.
- Google Sheets creation and editing works.
- Google Docs creation and editing works.
- The Sheet and Doc were created under the user's personal Google account, not a service account.

## Still Needed Before First Full Research Run

- Live X/Twitter research path:
  - Preferred: source `/Users/mbaggetta/.codex/private/env/research.env` for `XAI_API_KEY`.
  - This key was copied from `mattmini` without printing the value and verified with a small xAI API smoke test.
  - Fallback: logged-in browser inspection of the project X account.
- Confirm transcript path:
  - Use available public transcripts when reliable.
  - If no reliable transcript exists, mark the video as needing manual review.
  - Do not use audio/video older than 6 months.
- Confirm metrics access:
  - DeFiLlama public pages/API for TVL, fees, revenue, volume where available.
  - Dune dashboards if public or if the user is logged in.
  - Blockworks dashboards only if visible from the user's browser/session.
  - Project-native dashboards or app metrics where available.

## Required Dossier Guardrails

- Every material claim needs a dated source link.
- Every metric needs value, period, source URL, pulled date, and confidence.
- Missing metrics must be marked missing, not guessed.
- Docs older than 6 months are background only unless confirmed current.
- Conflicting source data must be shown rather than silently resolved.
- Codex must not connect wallets, sign messages, trade, stake, deposit, or withdraw.

## Weekly Run Flow

1. Read the next queued row in the Research Queue.
2. Copy the Dossier Template into a new project-specific Google Doc in the Drive folder.
3. Collect written sources: docs, website/app, project blog, announcements.
4. Collect X/Twitter sources from the last 6 months.
5. Collect YouTube/X audio-video sources from the last 6 months only.
6. Pull metrics from DeFiLlama, Dune, Blockworks, project dashboards, and app-native stats.
7. Fill the dossier and source ledger.
8. Run the quality gate.
9. Update the queue row with status, dossier link, headline metrics, top differentiator, and open questions.
