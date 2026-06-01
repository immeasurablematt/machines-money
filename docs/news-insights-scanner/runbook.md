# X List News & Insights Scanner Runbook

## Purpose

The scanner turns a broad X-list feed into a short Machines & Money review queue. It should save Ian from reading every tweet himself: scan the recent list activity, drop low-signal posts, and retain only the most useful announcements, stats/charts, and deep-dive/article candidates. It is not newsletter copy and it is not Research Dossier. Only a high-priority single-project deep dive should emit an optional dossier seed.

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
- Human review queue: top 12 selected items
- X API safety cap: 10 pages, up to 1,000 tweets before the lookback cutoff stops pagination
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
X_BEARER_TOKEN=... PYTHONPATH=src python3 -m news_insights_scanner \
  --ingestion x_api \
  --top-n 12
```

For repeated local runs, create a private `.env` file in the repo root:

```bash
cp .env.example .env
```

Then set `X_BEARER_TOKEN` inside `.env`. The scanner loads `.env` automatically and `.gitignore` keeps it out of Git. To use a different env file path, set `NEWS_INSIGHTS_ENV_FILE=/path/to/file`.

If `--ingestion x_api` is selected without `X_BEARER_TOKEN` or `TWITTER_BEARER_TOKEN`, the scanner writes an empty digest with run-level `verification_status: manual_review_needed` and an ingestion warning. It never fabricates posts.

## Selection Behavior

The scanner does not render a catalog of every reviewed tweet. For X API runs it paginates through recent list posts until it reaches the lookback cutoff or the `--max-ingest-pages` safety cap. It then:

1. filters to the lookback window,
2. classifies and scores candidates,
3. drops retweets, low-signal language, event/podcast promos without substance, and posts with no concrete signal,
4. ranks the remaining candidates,
5. renders only `--top-n` selected items in `digest.md`.

The digest starts with an executive summary for Ian: reviewed count, selected count, filtered count, and the mix of announcements, adoption stats, and deep reads. Internal scoring, raw verification labels, and drop-reason detail should stay out of the top reader flow. A short narrowing note can appear near the bottom so Ian can trust that the scanner did real triage without reading the full feed.

## Review Checklist

- Confirm the executive summary is short enough to read first.
- Confirm the reader-facing Markdown does not expose raw labels like `needs_verification`, internal scores, or selection reasons.
- Confirm the reviewed count is larger than the selected count on normal X API runs.
- Treat manual and X-post-only claims as needing human review before reuse.
- Prefer primary source and dashboard URLs over reposted X URLs.
- Check adoption metrics for value, period, source URL, pulled date, confidence, and source kind in `digest.json`.
- Keep the broad scanner distinction: do not convert routine mentions into Research Dossier work.

## Open Product Decisions

- Sustainable X access path: official API, logged-in browser, or manual URLs.
- Digest destination: repo outputs, Google Drive, Paperclip comments, or a mix.
- Final follow-up buckets for Ian.
