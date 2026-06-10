# X List News and Insights Scanner Spec

> **PAUSED (2026-06-10).** This feature is parked while the project focuses on the free DeFi
> dashboard. Spec retained for a future resume. See the README "Paused work" section.

## Summary

Build a scanner that reviews Ian's curated X list and turns the stream into a short, source-linked news and insight inbox for Machines & Money.

Source list:

- https://x.com/i/lists/2011849979095138608

The scanner should help Ian find:

- Announcements: new products, funding rounds, partnerships, launches, integrations, governance changes, campaigns, and major roadmap updates.
- Adoption stats: users, fees, revenue, volume, TVL, AUM, buybacks, market cap, active wallets, transaction counts, and other signals that a project is growing or getting used.
- Deep dives and articles: thoughtful project analysis, explainers, technical posts, market structure pieces, and other content showing how a project is solving a real problem or building something meaningfully new.

The output is not an automated newsletter and it is not the same product as Research Dossier. It is a broad scanning layer that helps Ian decide what to read, what to save, what to mention in recurring newsletter formats, and what deserves follow-up.

## User Need

Ian already uses the X list to keep up with crypto and finance projects. The problem is volume: useful announcements, charts, stats, and deep dives are mixed into a fast-moving feed.

The scanner should reduce the feed to the items most likely to support Machines & Money research:

1. News Ian should know this week.
2. Metrics that show adoption or business traction.
3. Long-form ideas worth reading or turning into an article angle.
4. Themes, projects, or links that deserve follow-up.

## Primary User

Ian, as the editor/researcher for Machines & Money.

Secondary users:

- Matt or agents helping prepare research queues.
- Future Paperclip agents doing source collection, weekly scans, or follow-up research.

## Goals

- Save Ian time reviewing the X list without lowering his research quality.
- Highlight source-linked items that are timely and useful.
- Separate "news" from "stats" from "deep dives" so Ian can scan quickly.
- Preserve enough context for Ian to judge the item without opening every post.
- Create a broad weekly research inbox across many projects, themes, charts, and articles.
- Hand off to other workflows only when an item needs deeper work.
- Maintain a dated source ledger for any claim or metric that may be reused.

## Non-Goals

- Do not auto-publish newsletter copy.
- Do not summarize private or protected posts unless Ian has explicitly provided access and usage permission.
- Do not treat X posts as confirmed facts when they point to an external announcement, dashboard, or article. The scanner should follow and cite the original source when available.
- Do not connect wallets, sign messages, trade, stake, deposit, withdraw, or interact with protocols.
- Do not DM projects automatically.
- Do not force every good item into a single-project dossier path.

## Source Access

Preferred ingestion path:

- Use the official X List Posts API where available: `GET /2/lists/:id/tweets`.
- Store the list id as configuration: `2011849979095138608`.

Fallback ingestion paths:

- Logged-in browser review of the list.
- Manual export or pasted post URLs from Ian.
- Embedded public list timeline only for human inspection, not as the main data source.

The scanner should record which access path was used for each run. If API access fails, the run should degrade to "manual review needed" instead of fabricating results.

## Scanner Cadence

MVP cadence:

- Manual run on demand.
- Default lookback: last 24 hours.
- Optional weekly run: last 7 days.

Future cadence:

- Scheduled weekday digest.
- Separate weekend digest for long reads and deeper research.

## Item Classification

Each candidate item should be assigned one primary type.

### Announcement

Use when the post claims or links to a concrete event:

- Product launch
- New feature
- Fundraise
- Partnership
- Integration
- Roadmap update
- Governance proposal or vote
- Ecosystem incentive campaign
- Tokenomics change
- Major team/company milestone

Required fields:

- Project or company
- Event type
- What changed
- Source post URL
- Original source URL, if linked
- Date posted
- Confidence
- Why Ian should care

### Adoption Stat

Use when the item contains or links to a metric showing usage, growth, economics, or traction.

Relevant metrics include:

- Users or active wallets
- Fees
- Revenue
- Protocol earnings
- Buybacks
- Transaction volume
- Trading volume
- TVL or AUM
- Market cap
- Deposits, borrows, swaps, mints, redemptions, or other project-specific activity
- Retention, cohort, or usage-frequency charts

Required fields:

- Metric name
- Metric value
- Time period
- Source URL
- Pulled date
- Confidence
- Whether the source is primary, dashboard-derived, or reposted
- What adoption story it may support

### Deep Dive or Article

Use when the item links to or is itself a substantive analysis, thread, essay, research note, dashboard writeup, or technical explanation.

Relevant signals:

- Explains a project mechanism
- Describes a real user problem
- Shows why a product is different
- Includes useful charts or data
- Offers a defensible thesis
- Compares projects or market structures

Required fields:

- Article/thread title or topic
- Author
- Project(s) covered
- Main thesis
- Why it matters for Machines & Money readers
- Source URL
- Date published or posted
- Suggested use: short mention, chart source, article angle, saved read, or follow-up candidate

## Scoring

Each item receives a 1-5 score in four areas.

### Relevance

How directly the item fits Machines & Money's core topics: DeFi, tokenized assets, RWAs, asset management, yield opportunities, derivatives, AI, financial infrastructure, and adjacent crypto/finance markets.

### Timeliness

How fresh the item is and whether it matters now.

### Evidence Quality

How strong the source is:

- 5: primary project announcement, official dashboard, filing, protocol data source, or respected data provider.
- 4: reputable researcher or publication linking to primary evidence.
- 3: credible X post with enough detail to verify.
- 2: interesting but thin, needs confirmation.
- 1: vague, promotional, or unsupported.

### Editorial Value

How useful the item is for Ian:

- Quick newsletter mention
- Chart worth saving
- Reader-useful stat
- Strong article angle
- Follow-up research candidate

The scanner should produce a final priority:

- High: read or use this week.
- Medium: save for context or future follow-up.
- Low: probably skip unless Ian is already tracking the project.

## Output Format

The MVP output should be a Markdown digest and a machine-readable JSON backup.

### Markdown Digest

Sections:

1. Top Picks
2. Announcements
3. Adoption Stats and Charts
4. Deep Dives and Articles
5. Follow-Up Candidates
6. Needs Verification
7. Skipped or Low-Signal Items

Each item should include:

- Title
- Type
- Project
- One-sentence summary
- Why it matters
- Source links
- Date
- Confidence
- Suggested next action

### JSON Backup

Each item should include:

- `run_id`
- `source_list_id`
- `post_id`
- `post_url`
- `author_handle`
- `posted_at`
- `captured_at`
- `classification`
- `project_names`
- `summary`
- `evidence_urls`
- `metrics`
- `scores`
- `priority`
- `recommended_action`
- `verification_status`
- `notes`

## Relationship to Research Dossier

Research Dossier and the X List News and Insights Scanner are separate features.

Research Dossier is for a specific deep dive on one project or opportunity. It answers a focused set of questions, checks the project's sources, collects metrics, and helps Ian prepare a project-focused article.

The X List News and Insights Scanner is broader. It scans a live list across many accounts, projects, market themes, charts, announcements, and articles. Most useful scanner items should not become dossiers. They may instead become:

- A short DeFi In Five mention
- A Truth Within Trends chart or stat
- A saved article for Ian to read later
- A market theme to watch
- A project to keep on the radar
- A candidate for deeper research only if the item is strong enough

When an item does look like a strong candidate for a project-focused article, the scanner can produce an optional dossier seed:

- Project name
- Why it surfaced
- Best source links
- Key metrics found
- Differentiating feature or thesis
- Suggested hands-on test, if obvious
- Open questions

That optional seed should map to the existing four dossier questions:

1. What does the project do?
2. Why is this important and unique?
3. How can this help people?
4. How are we actively using it?

## Quality Rules

- Every material claim needs a dated source link.
- Every metric needs value, period, source URL, pulled date, and confidence.
- If a post links to a primary source, prefer the primary source over the X post.
- If the source is a chart image, preserve the image URL or screenshot reference and describe the chart carefully.
- If the claim cannot be verified, mark it as "needs verification."
- If the same story appears multiple times, merge duplicates and keep all useful source links.
- Do not use audio or video older than 6 months for downstream deep-dive work.
- Treat docs older than 6 months as background unless confirmed current.

## MVP Workflow

1. Run the scanner for the configured list and lookback window.
2. Collect candidate posts and linked URLs.
3. Classify each candidate.
4. Extract project names, claims, metrics, and linked sources.
5. Score each candidate.
6. Deduplicate repeated stories.
7. Produce Markdown and JSON outputs.
8. Flag anything that needs manual verification.
9. Mark follow-up actions: mention, save, verify, track theme, or optional Research Dossier seed.

## MVP Acceptance Criteria

- Given a list URL and a lookback window, the scanner produces a digest with announcements, stats, and deep dives separated.
- Each retained item includes source link, date, summary, confidence, and suggested action.
- Adoption-stat items include metric value, period, source, and confidence when available.
- Duplicate posts about the same event are grouped.
- Items that cannot be verified are clearly marked instead of treated as facts.
- The output includes a Follow-Up Candidates section for items that deserve more than a quick read.
- Research Dossier candidates are optional and only appear when a single project clearly deserves deep-dive treatment.
- A JSON backup is saved for repeatability and later automation.

## Implementation Notes

Suggested repo shape:

- `src/news_insights_scanner/` for scanner logic.
- `outputs/news-insights-scanner/YYYY-MM-DD/` for generated digests and JSON backups.
- `docs/news-insights-scanner/` for spec, runbook, and prompt notes.

Potential modules:

- `ingest_x_list`: fetch posts from the configured X list.
- `extract_links`: collect linked announcements, articles, dashboards, and media.
- `classify_items`: assign announcement, adoption stat, deep dive, or skip.
- `extract_metrics`: capture values, periods, source URLs, and confidence.
- `score_items`: calculate relevance, timeliness, evidence quality, and editorial value.
- `render_digest`: write Markdown and JSON outputs.

## Open Questions

- Should the first version run only on demand, or should it create a weekday digest automatically?
- Should the digest live in the repo, Google Drive, Paperclip comments, or all three?
- Does Ian want a strict "top 10 only" view, or a fuller inbox with low-signal items collapsed?
- What follow-up buckets does Ian want: read later, chart bank, newsletter mention, theme watch, project watch, and dossier candidate?
- What X access path is available and sustainable: official API, logged-in browser, or manual URLs?

## Recommended First Build

Build the first version as a manual, source-led digest generator:

- Input: list id, lookback window, optional max item count.
- Output: Markdown digest plus JSON backup.
- First use case: broad weekly scan for newsletter planning.
- Human review required before anything becomes newsletter copy or a downstream deep dive.

This keeps the feature useful immediately while preserving Ian's research standards.
