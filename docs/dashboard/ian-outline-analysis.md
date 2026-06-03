# Machines & Money Dashboard: Ian Outline Analysis

Date: 2026-06-02

## Summary

Ian's outline is enough to begin dashboard discovery and MVP planning. It is not yet enough to build the full dashboard because the outline defines desired views, but not data availability, source reliability, update cadence, or the first user workflow to optimize.

The safest starting point is a discovery pass that turns the wishlist into:

- a metric inventory,
- a source map,
- an MVP dashboard scope,
- a prototype plan,
- and a backlog of future dashboard modules.

## What Ian Clearly Wants

Ian wants a metrics dashboard that can compare DeFi and onchain finance projects across:

- price and market performance,
- adoption,
- volume,
- TVL, AUM, deposits, borrows, and utilization,
- fees and revenue,
- treasury balances,
- tokenomics,
- buybacks,
- stablecoin supply and staking/yield behavior,
- sector-level share,
- and project-specific metrics by vertical.

The major interaction patterns are also clear:

- daily, weekly, monthly, quarterly, yearly, cumulative, and custom timeframes,
- project and sector toggles,
- multiple metrics on one chart,
- hover values,
- left/right axis support for different units,
- bar charts for time series,
- pie charts for period snapshots,
- and project-specific drilldowns.

## What Is Missing

The outline does not yet answer:

- Which projects are in version 1?
- Which metrics are required every week versus only useful occasionally?
- Which metrics have reliable public sources?
- Which metrics require paid data, logged-in dashboards, or custom collection?
- Which metrics are project-native versus parent-protocol or ecosystem context?
- Which definitions should be standardized across projects?
- How often each data feed should update.
- Whether the dashboard is internal-only for Ian or eventually public/subscriber-facing.
- Whether the first output should be a local web app, Google Sheet dashboard, embedded BI dashboard, or static recurring report.

## Product Risk

The biggest risk is trying to build every chart at once.

Ian's outline spans many sectors and dozens of project-specific data definitions. A full build without a data-source pass would likely produce a dashboard with inconsistent metrics, stale numbers, and unclear confidence.

The dashboard should follow the same research-quality bar as Research Dossier:

- every material metric needs value, period, source URL, pulled date, and confidence,
- missing data should be marked missing, not guessed,
- parent or ecosystem metrics should not be presented as project-native,
- and conflicting source data should be visible instead of silently resolved.

## Recommended First Slice

Start with a cross-project comparison dashboard for a small universe of projects and sectors.

Version 1 should focus on metrics that are broadly useful and most likely to have reliable sources:

- token price,
- market cap,
- FDV,
- TVL or AUM,
- active users or active wallets where available,
- transaction or trading volume,
- fees,
- revenue,
- buybacks where available,
- and stablecoin/staking/yield metrics only for projects where those are central to the thesis.

This first slice should answer:

1. What changed this week?
2. Which sectors are gaining or losing activity?
3. Which projects have article-worthy adoption, financial, or tokenomics changes?
4. Which metrics are verified enough for Ian to cite?
5. Which project needs a Research Dossier follow-up?

## Dashboard MVP Sections

### 1. Market and Token Overview

Purpose: give Ian a quick way to compare project performance.

Initial charts:

- price by project,
- market cap by project,
- FDV by project,
- price and market cap performance over selected timeframe.

Likely sources:

- CoinGecko,
- DefiLlama coins API,
- TradingView embed for visual price charts.

### 2. Adoption and Usage

Purpose: surface whether projects are actually being used.

Initial charts:

- active users or wallets,
- transactions,
- volume by sector,
- project share of sector volume.

Likely sources:

- Artemis,
- Token Terminal,
- DefiLlama,
- project-native dashboards,
- Dune dashboards.

### 3. Financials

Purpose: show business traction.

Initial charts:

- TVL or AUM by project,
- fees by project,
- revenue by project,
- treasury balance where available.

Likely sources:

- DefiLlama,
- Token Terminal,
- project treasury dashboards,
- project-native APIs,
- Dune dashboards.

### 4. Tokenomics

Purpose: identify changes that matter for token holders and article angles.

Initial charts:

- circulating supply,
- max supply,
- market cap,
- FDV,
- buybacks where available,
- locked or staked token ratio where available.

Likely sources:

- CoinGecko,
- DefiLlama,
- Token Terminal,
- project-native tokenomics pages,
- project disclosures.

### 5. Research Follow-Up Queue

Purpose: connect dashboard observations to Machines & Money research workflows.

Initial fields:

- project,
- metric change,
- source,
- confidence,
- why it matters,
- suggested next action,
- dossier candidate yes/no,
- open question.

This should connect directly to Research Dossier and the News & Insights Scanner, rather than becoming a separate disconnected tool.

## Open Decisions For Ian

Ask Ian to choose:

- the first 10 to 20 projects,
- the first 3 to 5 sectors,
- whether the dashboard is internal-only or eventually public,
- whether a weekly digest from the dashboard matters more than live interactivity,
- and which data providers he already has access to.

## Next Implementation Step

Build a metric inventory and source map before coding the dashboard.

The first useful deliverable is not a polished frontend. It is a verified table showing which requested metrics are currently available, where they come from, how fresh they are, and whether they can be trusted enough for Machines & Money research.
