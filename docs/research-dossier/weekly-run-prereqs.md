# Weekly Research Dossier Prereqs

This file tracks the setup needed before running a weekly Machines & Money research dossier in Codex.

## Google Drive Workspace

- Drive folder: [Machines & Money Research Dossiers](https://drive.google.com/drive/u/0/folders/1WZvk7DcWMRzb823c26vI7BI2ZCw7sjCO)
- Research queue: [Research Queue - Machines & Money](https://docs.google.com/spreadsheets/d/17JihtnYqzhLJ2nf5B7cRZkUwFKxQSk0l-v9a_W-t0P4/edit?gid=0#gid=0)
- Dossier template: [Research Dossier Template - Machines & Money](https://docs.google.com/document/d/1aIWbXgyIw2lECk5xb4s_fLzf7Uy4aAV0zepWCBSRMO0/edit?tab=t.0)

Keep the top-level Drive folder as the control room only:

- Research Queue
- Dossier Template
- One subfolder per project

Each project folder should contain that project's:

- Formatted Google Doc dossier
- Formatted Google Sheet tables
- Raw Markdown/CSV/JSON backups
- Transcript files
- Screenshots or exported artifacts, if any

Current project folders:

- [Nova Markets](https://drive.google.com/drive/folders/196_4y0MK19sYM8VdIcHUKKlefEJyexfJ)
- [Turtle](https://drive.google.com/drive/folders/1sgMbiNlPFvzBLnCCaxfW4_Nv-0OmRZIo)
- [Lite Strategy](https://drive.google.com/drive/folders/1DJLo5DmlmEE5AwYmYJN3YmzTOcvYSbl9)
- [Boros](https://drive.google.com/drive/folders/1wFcckmktyPLaA8ajwApCat2K6150sAj5)

## Verified Setup

- Preferred delivery path: Google Drive connector with write/import permissions.
- Fallback delivery path: Codex in-app browser with the user signed into Google there.
- Do not use the user's personal Chrome session for Drive or Docs delivery unless the user explicitly asks for that specific fallback.
- Google Drive folder creation works in the Codex in-app browser after Google sign-in.
- Google Docs creation and editing works in the Codex in-app browser after Google sign-in.
- The Sheet and Doc were created under the user's personal Google account, not a service account.
- If the connector can read but not write, ask the user to complete OAuth in the Codex browser or reauth the Google Drive connector with write/import scopes. Do not move to personal Chrome.

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

- Start every dossier with a Source Map pass before writing or synthesis.
- Do not start the dossier narrative until native metrics, current video, docs/app, social, and third-party sources have been searched and classified.
- Prefer project-native metrics over parent-protocol or ecosystem metrics.
- Parent-protocol metrics are allowed only as clearly labeled context after checking for project-native metrics.
- Current video/transcript sources are first-class narrative sources, not optional extras.
- Every material claim needs a dated source link.
- Every metric needs value, period, source URL, pulled date, and confidence.
- Missing metrics must be marked missing, not guessed.
- Docs older than 6 months are background only unless confirmed current.
- Conflicting source data must be shown rather than silently resolved.
- Codex must not connect wallets, sign messages, trade, stake, deposit, or withdraw.

## Source Map Pass

Before creating the dossier, build a source map for the project. The source map is the evidence plan; it decides what gets used and what still needs verification.

Create a `Source Map` tab in the project Google Sheet and a raw CSV backup in the project folder with these columns:

- Source
- URL
- Category
- Relationship
- Freshness / date
- What it can answer
- Confidence
- Use in dossier
- Notes

Use these categories:

- `official_site_app`
- `docs`
- `native_metrics`
- `parent_context`
- `video_transcript`
- `social_x`
- `blog_announcement`
- `dashboard_api`
- `contracts_github_audits`
- `third_party_analysis`

Use these relationship labels:

- `native`: the project itself or a project-owned data source.
- `parent`: parent protocol, ecosystem, or company context.
- `third_party`: outside analysis, aggregator, index, media, or commentary.

Source priority:

1. Project-native dashboards, APIs, app stats, DefiLlama protocol pages, Token Terminal, Dune, Artemis, or other project-specific metrics.
2. Current founder/team videos, podcast interviews, demos, livestreams, and transcripts from the last 6 months.
3. Current official website/app, docs, blog, release notes, and announcements.
4. X/Twitter posts and replies from the last 6 months.
5. Contracts, GitHub, audits, risk docs, or protocol specs.
6. Parent-protocol metrics and ecosystem context.
7. Third-party analysis and media commentary.

Hard-stop checks before writing:

- Search exact project-native DefiLlama pages, including `https://defillama.com/protocol/<project-slug>`.
- Search YouTube for `<project>`, `<project> founder`, `<project> demo`, `<project> interview`, `<project> podcast`, and `<project> explainer`.
- Check whether useful videos have transcripts. Pull full transcripts when available; otherwise flag them as needing manual review.
- Check for project-native app APIs, public data folders, dashboards, Dune pages, and metrics pages linked from the app/docs/site.
- Separate project-native metrics from parent/ecosystem metrics in the source map before using either.
- If parent metrics are used, label them as parent context in the metrics table and prose.

Do not publish the dossier until the source map is complete enough that an obvious native metric or current video source is unlikely to have been missed.

## Weekly Run Flow

1. Read the next queued row in the Research Queue.
2. Create or reuse a project subfolder under the Drive folder.
3. Run the Source Map pass and save it before writing.
4. Create the project-specific Google Doc and Google Sheet inside that project folder.
5. Save raw Markdown, CSV, JSON, transcript, and screenshot backups inside the same project folder.
6. Collect written sources: docs, website/app, project blog, announcements.
7. Collect X/Twitter sources from the last 6 months.
8. Collect YouTube/X audio-video sources from the last 6 months only, and pull full transcripts when available.
9. Pull metrics from project-native dashboards/APIs, exact DefiLlama protocol pages, Dune, Blockworks, Token Terminal, Artemis, and other relevant sources.
10. Add parent-protocol or ecosystem metrics only after native project metrics are checked and clearly labeled.
11. Fill the dossier, source ledger, Source Map tab, metrics tables, and transcript/source backups.
12. Run the quality gate.
13. Update the queue row with status, dossier link, project folder link, headline metrics, top differentiator, and open questions.

## Single-Project Link Flow

When Matthew gives only an X account link or project link and asks for a project deep dive, run Research Dossier, not the broad X List News & Insights Scanner.

Use this path for prompts like:

- "run skill on https://x.com/<project>"
- "do a dossier on <project>"
- "build the Boros/Turtle/Nova-style output for <project>"
- "put the final deliverable in the Research Dossiers Drive folder"

Do not run the X digest skill unless the user explicitly asks for a digest, scanner, list scan, or 24-hour news shortlist.

For a single-project link:

1. Normalize the project name, X handle, website/app, docs, and likely DefiLlama slug.
2. Create local output under `outputs/research-dossier/YYYY-MM-DD-<project-slug>/`.
3. Build Source Map, Source Ledger, Metrics, raw API backups, and transcript backups before writing synthesis.
4. Draft the dossier Markdown using the existing dossier sections.
5. Render the Markdown to clean Google-Docs-friendly HTML:

   ```bash
   python3 scripts/render_research_dossier_html.py "outputs/research-dossier/YYYY-MM-DD-<project-slug>/<Project> Research Dossier - YYYY-MM-DD.md"
   ```

6. Deliver the Google Doc from the rendered HTML, not from raw Markdown. The final Doc must have real Google Docs headings and lists; visible `#`, `##`, `**`, backticks, or typed list markers in the body are a formatting failure.
7. Verify with Google Docs readback:
   - title paragraph present,
   - H1 is `HEADING_1`,
   - main sections are `HEADING_2`,
   - bullets/numbered items are real list items,
   - no temporary focus-test text remains.
8. Verify Drive placement by listing the project folder.

## Drive Delivery Rules

- Parent folder: `https://drive.google.com/drive/u/0/folders/1WZvk7DcWMRzb823c26vI7BI2ZCw7sjCO`
- Create one project folder per dossier, for example `InfiniFi`.
- Place the formatted Google Doc in the project folder.
- When upload/write scopes are available, also add the companion table workbook, raw Markdown, CSVs, JSON backups, and transcripts to the same project folder.
- If upload/write scopes are missing, still create the formatted Google Doc through the Codex in-app browser after user OAuth. Report which companion files remain local.
- Do not claim Drive delivery until the folder listing or document readback proves the file exists in the project folder.
