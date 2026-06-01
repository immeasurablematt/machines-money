# X List News & Insights Scanner Runbook

## Purpose

The scanner turns a broad X-list feed review into a dated Machines & Money research inbox. It is not newsletter copy and it is not Research Dossier. Most retained items should become short mentions, saved reads, chart/stat candidates, project-watch notes, or theme-watch notes. Only a high-priority single-project deep dive should emit an optional dossier seed.

## Default Manual Run

From the repo root:

```bash
PYTHONPATH=src python3 -m news_insights_scanner \
  --ingestion manual \
  --input samples/news-insights-manual.json \
  --output-dir outputs/news-insights-scanner/2026-06-01
```

The command writes:

- `outputs/news-insights-scanner/2026-06-01/digest.md`
- `outputs/news-insights-scanner/2026-06-01/digest.json`

Defaults:

- Source list ID: `2011849979095138608`
- Lookback: 24 hours
- Destination: `outputs/news-insights-scanner/YYYY-MM-DD/`

Use a weekly lookback when needed:

```bash
PYTHONPATH=src python3 -m news_insights_scanner \
  --ingestion manual \
  --input samples/news-insights-manual.json \
  --lookback-days 7
```

## Manual Input Format

Preferred input is JSON:

```json
{
  "source_list_id": "2011849979095138608",
  "posts": [
    {
      "post_id": "optional stable id",
      "post_url": "https://x.com/account/status/123",
      "author_handle": "account",
      "posted_at": "2026-06-01T13:15:00Z",
      "project_names": ["Project"],
      "title": "Short title",
      "text": "Post text with links",
      "urls": [
        {"url": "https://project.example/blog", "source_kind": "primary"}
      ],
      "source_verified": false,
      "verification_status": "needs_verification"
    }
  ]
}
```

Plain newline input also works for quick pasted URLs or notes. Each non-empty line becomes one candidate item.

A primary or dashboard URL improves evidence quality, but it does not make an item verified by itself. Use `source_verified: true` or `verification_status: "verified"` only after a human has checked that the linked source directly supports the claim.

## Optional X API Run

Official X API ingestion is present but optional. To use it, set a bearer token and run:

```bash
X_BEARER_TOKEN=... PYTHONPATH=src python3 -m news_insights_scanner --ingestion x_api
```

For repeated local runs, create a private `.env` file in the repo root:

```bash
cp .env.example .env
```

Then set `X_BEARER_TOKEN` inside `.env`. The scanner loads `.env` automatically and `.gitignore` keeps it out of Git. To use a different env file path, set `NEWS_INSIGHTS_ENV_FILE=/path/to/file`.

If `--ingestion x_api` is selected without `X_BEARER_TOKEN` or `TWITTER_BEARER_TOKEN`, the scanner writes an empty digest with run-level `verification_status: manual_review_needed` and an ingestion warning. It never fabricates posts.

## Review Checklist

- Confirm the ingestion path shown at the top of `digest.md`.
- Treat manual and X-post-only claims as needing human review before reuse.
- Prefer primary source and dashboard URLs over reposted X URLs.
- Check adoption metrics for value, period, source URL, pulled date, confidence, and source kind in `digest.json`.
- Keep the broad scanner distinction: do not convert routine mentions into Research Dossier work.

## Open Product Decisions

- Sustainable X access path: official API, logged-in browser, or manual URLs.
- Digest destination: repo outputs, Google Drive, Paperclip comments, or a mix.
- Inbox shape: strict top-N or fuller inbox with low-signal items collapsed.
- Final follow-up buckets for Ian.
