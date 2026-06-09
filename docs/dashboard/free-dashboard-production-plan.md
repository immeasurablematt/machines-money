# Free Dashboard Production Plan

Date: 2026-06-08

## Goal

Ship the free Machines & Money dashboard as a public audience-growth asset within two weeks.

This plan applies only to `docs/dashboard/free.html`. The broader/pro dashboard stays separate in `docs/dashboard/prototype.html`.

## Inputs

- Ian likes `hl.eco` because the charts are interactive, continuously updated, and support flexible timeframes.
- Ian also likes the clean category layout at the top because it teaches viewers the range of activity in the ecosystem.
- Ian's free Dune outline organizes the dashboard around index metrics first, then category sections: spot, derivatives, lending, asset management, tokenization/RWA, infra, AI, and token value accrual.

## Final Information Architecture

1. Top navigation: Dashboard, Leaderboard, Sources, Subscribe.
2. First viewport: clear public framing, snapshot freshness, one immediate takeaway, and subscriber CTA.
3. Summary strip: projects tracked, market cap, TVL, snapshot date, and coverage caveat.
4. Category map: Index, Spot, Derivatives, Lending, Asset Management, Tokenization/RWA, Infra, AI, Token Value Accrual.
5. Interactive chart area: timeframe selector, metric selector, sector filter, ranked chart, and chart-angle prompts.
6. Leaderboard table: project, sector, market cap, TVL, fees, revenue, usage.
7. Sources and caveats: market data, product data, usage data, methodology caveats.
8. Newsletter CTA: subscribe for weekly interpretation and deeper Machines & Money analysis.

## Free vs Pro Boundary

Free dashboard:

- Public static page.
- Broad ecosystem orientation.
- Current rankings, 24H market activity, 7D usage where available, and 30D fees/revenue.
- Clear caveats and source confidence.
- Social-share chart angles and newsletter conversion.

Pro dashboard:

- Separate later product.
- Deeper historical trends, project detail pages, richer source ledgers, research scoring, alerts, and subscriber-only interpretation.
- Can use more complex Dune/project-native metrics after source coverage is proven.

## Default First-Screen Visitor Journey

The visitor should understand within 60 seconds:

- This is a Machines & Money public fundamentals surface.
- The dashboard compares crypto platforms by market attention, product scale, activity, fees, revenue, and usage coverage.
- The category map shows what parts of the ecosystem are being tracked.
- The page is useful immediately, but the newsletter provides the interpretation.

## Category Map and Naming

Use Ian's Dune outline as the public taxonomy:

- Index: cross-project scorecard and headline tables.
- Spot: DEX volume, fees, users, and market share.
- Derivatives: perps/options volume, fees, users, and share.
- Lending: TVL, fees, borrow volume, and utilization once sourced.
- Asset Management: stablecoin, yield, card, and vault metrics.
- Tokenization/RWA: tokenized asset value, holders, and volume.
- Infra: messages, network usage, volume, and active users.
- AI: agent volume, fees, users, agents, and aGDP-style metrics once sourced.
- Token Value Accrual: buybacks, token performance, fee capture, and value-accrual evidence.

## Chart and Timeframe Model

Current production MVP:

- Current: TVL, market cap, FDV.
- 24H: token volume.
- 7D: active-wallet rows where available.
- 30D: fees, revenue, DEX volume where available.

Next production layer:

- Add 7D and 30D growth columns once historical snapshots are retained.
- Add line charts after at least 30 days of reliable refreshes.
- Add market-share charts for spot/derivatives only after source definitions are consistent.

## Data Freshness and Refresh Workflow

Near-term:

- Keep the dashboard static and generated from `docs/dashboard/generated-dashboard-data.js`.
- Refresh data with `python3 scripts/refresh_dashboard_data.py`.
- Show the generated snapshot date on the page.

Production target:

- Run a scheduled refresh, then deploy the updated static page.
- Keep dated generated snapshots so growth metrics can be calculated.
- Restore last-known-good data if a refresh fails validation.
- Keep API-key-dependent sources optional and documented.

Implemented local/scheduled pipeline:

- `scripts/refresh_dashboard_data.py` refreshes, validates, snapshots, and updates last-known-good files.
- `scripts/build_free_dashboard_bundle.sh` bundles `free.html` as `index.html` with `generated-dashboard-data.js`.
- `docs/dashboard/free-dashboard-refresh-workflow.yml` is the GitHub Actions workflow template. To activate it, copy it to `.github/workflows/free-dashboard-refresh.yml` from a GitHub account or token with workflow-file permission.

## Source and Caveat System

Every metric needs:

- Source name and URL.
- Source relationship: project-native, third-party, public dashboard, or manual.
- Confidence: high, medium, low.
- Period: current, 24H, 7D, 30D, YTD, 1Y.
- Caveat text when definitions are incomplete or coverage is directional.

Public copy should avoid implying that sparse usage rows represent total protocol users.

## Newsletter CTA and Social-Sharing Loop

The free dashboard should create three repeatable loops:

- User sees a useful chart and subscribes for weekly interpretation.
- Machines & Money shares a chart angle on social and links back to the dashboard.
- Ian uses the chart-angle prompts to choose newsletter or research-dossier topics.

CTA destination remains `https://machinesandmoney.beehiiv.com` until a dedicated landing page exists.

## Mobile Readiness

Production requirements:

- Category map wraps cleanly on mobile.
- Chart labels remain readable without horizontal page scrolling.
- Tables can horizontally scroll inside their section.
- CTA stays visible and does not crowd navigation.
- First viewport shows the brand, dashboard purpose, one takeaway, and a hint of the dashboard below.

## Analytics and Tracking Needs

Track:

- Page views.
- CTA clicks.
- Category clicks.
- Timeframe and metric changes.
- Sector filter changes.
- Social-share clicks once share controls are added.

Use privacy-conscious analytics. Do not block launch on a complex analytics stack.

## Production Hosting and Permanent URL Needs

The dashboard needs a stable public URL, not only a local file or expiring preview.

Recommended path:

- Keep `docs/dashboard/free.html` as the production source.
- Publish it as a static page with `generated-dashboard-data.js`.
- Use a permanent Machines & Money URL or a durable subpath that can be linked from Beehiiv and social posts.

Temporary preview rule:

- If here.now is used, bundle `docs/dashboard/free.html` as `index.html`.
- Do not publish `docs/dashboard/prototype.html` for free-dashboard review.
- Treat anonymous here.now links as review-only because they can expire unless claimed.

## QA Checklist

- `prototype.html` is unchanged.
- `free.html` loads without console errors.
- `generated-dashboard-data.js` loads from the same directory.
- Category cards filter or route to the expected view.
- Timeframe and metric controls work.
- Sector filter and sorting work.
- Empty states are readable.
- Newsletter CTA points to Beehiiv.
- Source cards explain market/product/usage caveats.
- Desktop and mobile layouts are readable.
- Snapshot date is visible.

## Two-Week Execution Plan

Days 1-2:

- Lock free/pro boundary.
- Update top category map and first-screen journey.
- Review current data rows against Ian's Dune outline.

Days 3-4:

- Add chart/table coverage for missing current free metrics that already exist in the generated data.
- Add source/caveat display at row or metric level.

Days 5-6:

- Improve social-sharing loop: chart-angle copy, share controls, and newsletter CTA placement.
- Add lightweight event tracking hooks.

Days 7-8:

- Add refresh workflow documentation and first scheduled-refresh design.
- Decide whether to preserve dated generated snapshots for growth metrics.

Days 9-10:

- Mobile QA, visual polish, accessibility pass, and source/caveat copy review.
- Verify no pro-dashboard code or copy has been mixed into the free surface.

Days 11-12:

- Host the static dashboard at a permanent URL.
- Test the live URL, CTA, social-card behavior, and analytics.

Days 13-14:

- Final Ian review packet: URL, what changed, source caveats, what is free now, and what moves to pro later.
- Fix review issues and prepare launch/social copy.

## First Implementation Step

Update `docs/dashboard/free.html` so the top category map reflects Ian's clarified taxonomy and can act as a useful navigation/filter layer before deeper data work.
