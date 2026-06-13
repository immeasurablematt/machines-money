# Machines & Money — Changelog for Ian

Date: 2026-06-13
Live site: https://immeasurablematt.github.io/machines-money/ (dashboard at /dashboard.html)

**Status: in review on branch, not yet merged to main.** Everything below is built and tested; merging the branch publishes it.

---

## What changed today: dashboard UX/UI improvements

This session started with a competitive audit of every dashboard linked in the DeFi20 Dashboard doc — DeFiLlama (fees, DEX, active loans), Token Terminal, Dune community dashboards (the DeFi20 reference, Maple, Falcon, Ethena, Virtuals), hl.eco (Hyperliquid), Ethena's transparency dashboard, Canton analytics, StableWatch, and RWA.xyz. The goal was to identify what the best-in-class tools do that ours doesn't, then implement the highest-impact gaps.

### Token Returns table view (new)

A toggle has been added to the Project Signal Table: **Fundamentals** (existing columns) and **Token Returns** (new). Token Returns shows:

| # | Project | Sector | Mkt Cap | FDV | 24H | 7D | 30D | 1Y | Data |
|---|---------|--------|---------|-----|-----|----|-----|----|------|

All return columns are colour-coded — green for positive, red for negative. This was the biggest gap vs DeFiLlama and Token Terminal, both of which show price performance alongside fundamentals as a matter of course. The data was already being collected daily (CoinGecko 24H/7D/30D/1Y price change); the dashboard just wasn't showing it.

### 30D Fee Δ% column (new, Fundamentals view)

The Fundamentals view now includes a **30D Δ%** column next to 30D Fees, showing month-over-month fee growth with the same green/red colour coding. DeFiLlama's table has this; ours didn't. Again — already collected via DefiLlama's `change_1m` field, just not surfaced.

### Fee mini-bar in the 30D Fees cell

The 30D Fees value now has a small proportional bar beside it showing each project's relative size within the current filtered view. The top project's bar is full-width; others scale accordingly. Borrowed from hl.eco's style — makes the rank difference immediately visible without reading numbers.

### Clickable chart bars

Clicking any bar in the chart now selects that project and scrolls to the Project Detail panel. Previously the chart was view-only; clicking required going back to the filter dropdown. Small but the interaction was broken without it.

### Smarter "What To Watch" stories

The three insight cards on the right of the chart now surface:
- **Fee momentum** — the project with the biggest 30D fee growth and a prompt to check whether it's structural or a one-off
- **Token momentum / Underperformer** — the strongest or weakest 30D token return, with a reminder to cross-check fundamentals
- **Capital efficiency**, **Value capture**, and the existing signals as fallbacks

Previously these cards were only driven by the active metric (who leads, who's second, what's lagging). Now they pull from the growth and performance data.

### Behind the scenes

- `aggregateByProject()` now maps all twelve extended metrics the pipeline already collects but the UI ignored: `perf24h`, `perf7d`, `perf30d`, `perf1y`, `feeGrowth7d`, `feeGrowth30d`, `tvlGrowth7d`, `fees7d`, `fees24h`, and `revenue7d`.
- Sort logic for % columns fixed — negative values (e.g. −25% return) now sort correctly; previously they were treated as 0.
- Mobile: columns 3 (Sector), 7, and 8 hide on small screens to keep both views readable.

---

## What is and isn't live

| | Status |
|---|---|
| GitHub Pages (main branch) | Running the previous version — no token returns, no fee growth column |
| This branch (`claude/dashboard-audit-consolidate-sflo6s`) | All changes above — ready to merge |
| Data pipeline | Unchanged — already collecting all these metrics daily |

To go live: merge the branch to main. GitHub Actions deploys automatically within ~2 minutes.

---

## What the audit said about the reference dashboards

**DeFiLlama** is the strongest reference for table design — multi-timeframe columns side-by-side and % change colouring are standard there. Weaknesses: no narrative or curation, no cross-metric views, no token performance column. We beat it on context.

**Token Terminal** is strongest on capital efficiency ratios and chart quality. Some of that is behind a paywall. Their P/F ratio (market cap / annualised fees) is a useful lens we haven't added yet — worth discussing for the Pro tier.

**Dune dashboards** are powerful but slow (each chart queries separately), visually inconsistent, and hard to navigate for a non-analyst audience. The DeFi20 Dune dashboard in the doc is a good data reference but not a UX model.

**hl.eco** is excellent for Hyperliquid-native depth and real-time data but too specialised to borrow from structurally. The relative bar sizing is useful.

**Ethena's transparency dashboard** is a good template for the Pro per-project pages — clean cards, clear data, trust-building.

**StableWatch, RWA.xyz, PaymentScan** are narrow but polished for their niche. Relevant when we build the per-project depth pages.

---

## Open questions for Ian

1. **Merge timing** — ready to deploy now; just need the go-ahead to merge.
2. **P/F ratio** — Token Terminal shows market cap / annualised fees as a valuation lens. Worth adding to the table (maybe as a third table view) or saving for Pro?
3. **7D Fees tab** — the data is there; easy to add as a chart metric. Useful for spotting weekly momentum. Want it?
