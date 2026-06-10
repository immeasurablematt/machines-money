# T001 Scout Audit: Free Dashboard Launch Readiness

Date: 2026-06-10
Branch: `claude/production-readiness-assessment-farxhv` (merged `codex/free-dashboard-prototype` at `27ec4da`)
Prototype baseline blob: `5db332f3a03c02916730eb58bd52de54b30efe3c`

## What Exists Now

- `docs/dashboard/free.html` (1,606 lines): complete interactive single-file dashboard. Nav, hero with takeaway card and freshness pill, 4-stat summary strip, 9-card category map matching Ian's taxonomy (Index, Spot, Derivatives, Lending, Asset Mgmt, RWA, Infra, AI, Accrual), metric-first chart with availability-gated timeframes, "What To Watch" stories, project detail panel, leaderboard table, selected-metric source/caveat panel, source strip, share/copy controls, two Beehiiv CTAs with `data-track` attributes.
- Data: `generated-dashboard-data.js` — 137 rows, 20 projects, 9 metrics, 8 sectors, snapshot 2026-06-04, 0 warnings. Every row has `source_name`, `confidence`, and `notes`.
- Pipeline: `scripts/refresh_dashboard_data.py` (validates, snapshots, last-good restore), `scripts/build_free_dashboard_bundle.sh` (verified working), `docs/dashboard/free-dashboard-refresh-workflow.yml` (GitHub Actions template, not yet activated in `.github/workflows/`).
- Docs: production plan, runbook, free-dashboard overview, data-availability triage, source maps, token-vs-product definitions, prior goal board (`free-dashboard-production-ready`, closed `full_outcome_complete: true` for its tranche).

## What Is Already Production-Ready (verified this session)

- Inline JS passes Node syntax check (1 block).
- `free.html` and `generated-dashboard-data.js` return HTTP 200 over `python3 -m http.server`.
- `bash scripts/build_free_dashboard_bundle.sh` builds `index.html` + data bundle.
- Category/metric/timeframe/sector/project/sort wiring is present and coherent in code; sector matching uses `includes()` so the combined "Spot and Derivatives" sector responds to both Spot and Derivatives cards.
- CTA hrefs point to `https://machinesandmoney.beehiiv.com`.
- `prototype.html` untouched.

## What Is Still Missing (launch gaps)

1. **No social/SEO meta**: no meta description, no Open Graph/Twitter-card tags. Social shares of the dashboard URL will render bare links — weak for the X/TG/LinkedIn loop the product exists to feed.
2. **Analytics**: `data-track` attributes exist on CTAs/share only; nothing records events, and category/metric/timeframe/sector changes are untracked. Plan requires lightweight implementation or a documented single remaining decision.
3. **Share text is generic** ("Machines & Money DeFi20 signal: <title>"): does not name the leading project or use a canonical URL.
4. **No permanent URL**: hosting remains the open external step from the previous goal. GitHub Pages is the obvious free path (bundle already builds an `index.html`).
5. **Refresh automation not activated**: the workflow template exists but is not in `.github/workflows/`.
6. **Snapshot is stale (2026-06-04)** and a live refresh is blocked *from this cloud environment* (DefiLlama returns HTTP 403 through the network proxy). Not blocked on Matt's Mac or GitHub Actions.
7. **Defensive gap**: `renderProjectDetail` calls `row.notes.includes(...)`; current data always has `notes`, but a future refresh emitting a row without it would crash the panel.
8. **No Ian review packet** and **no separate pro roadmap doc** (pro direction is scattered across plan docs).

## Free-Dashboard Scope vs Pro-Only

- Free now: current TVL/market cap/FDV, 24H token volume, 7D wallet rows (sparse, caveated), 30D fees/revenue/DEX volume, category map, leaderboard, source panel, share + CTA loops.
- Pro/later (from Ian's Dune outline): daily/cumulative line charts, market-share charts, growth columns, buybacks, per-project deep charts (EtherFi card, Ethena holders, Ondo/Centrifuge/Maple breakdowns, LayerZero/Canton/Virtuals series), token value accrual scorecard. These need historical snapshots, Dune credits, or per-project source mapping — out of free launch scope.

## Blocked / External

- **DefiLlama live refresh from this cloud session**: HTTP 403 via network proxy. Workaround: refresh runs locally on Matt's Mac or in GitHub Actions.
- **Enabling GitHub Pages**: repo Settings > Pages > Source: GitHub Actions — owner click, cannot be done from this session.
- **Analytics provider choice** (e.g., GoatCounter/Plausible): Ian/Matt decision; lightweight in-page event capture can ship now.
- **Custom domain** (optional, after Pages works).

## Ranked Implementation Slices

1. **S1 — free.html launch pass** (largest safe code slice): social/OG meta tags, lightweight event tracking wired to all key interactions, smarter share text with canonical-URL constant, `notes` crash guard.
2. **S2 — production pipeline activation**: copy refresh workflow into `.github/workflows/`, add GitHub Pages deploy workflow building the bundle, update runbook/hosting docs.
3. **S3 — Ian review packet + pro roadmap doc**: closes the review and free-vs-pro oracle items.
4. **S4 — live refresh verification**: blocked in this environment (403); document and hand to Actions/local run.

Recommended first Worker package: S1 with allowed files `docs/dashboard/free.html` only; verify with node syntax check, HTTP serve, DOM behavior checks, bundle build, prototype diff empty.
