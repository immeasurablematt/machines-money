# Machines & Money Metrics Dashboard MVP Spec

Date: 2026-06-02

## Product Goal

Help Ian spot article-worthy changes across DeFi, tokenized assets, derivatives, lending, asset management, infra, and AI projects without manually checking many dashboards every week.

The dashboard should support Machines & Money research, not replace Ian's judgment. It should make useful metrics easier to find, compare, cite, and route into Research Dossier or News & Insights Scanner follow-up.

## Primary User

Ian, as editor and researcher for Machines & Money.

Secondary users:

- Matt when preparing research queues,
- agents doing source collection or recurring scans,
- future reviewers checking whether a chart or claim is source-backed.

## MVP Promise

The first useful version should answer:

- What changed over the selected timeframe?
- Which sectors and projects show real adoption or financial traction?
- Which metrics are reliable enough to cite?
- Which observations should become a dossier, newsletter mention, saved chart, or open question?

## Non-Goals For MVP

- Do not build every project-specific chart from Ian's outline.
- Do not connect wallets, trade, stake, deposit, borrow, redeem, or interact with protocols.
- Do not publish public subscriber-facing pages yet.
- Do not hide uncertain or conflicting data behind a single clean number.
- Do not treat parent-protocol metrics as project-native metrics.
- Do not scrape authenticated dashboards unless access and usage are explicitly approved.

## First Project Universe

The first universe should be intentionally small.

Recommended starter set:

- Uniswap,
- Aave,
- Pendle,
- Hyperliquid,
- Ethena,
- Sky,
- Ondo,
- Aerodrome,
- Morpho,
- Jupiter.

This list is only a starting hypothesis. Ian should confirm the first 10 to 20 projects before build-out.

## First Sector Set

Recommended starter sectors:

- Spot,
- Derivatives,
- Lending,
- Tokenization,
- Asset Management,
- Infra,
- AI.

## Required Global Controls

MVP controls:

- timeframe selector: 1D, 7D, 30D, quarterly, yearly, cumulative,
- custom date range,
- sector filter,
- project filter,
- metric selector,
- source confidence filter,
- verified-only toggle.

Future controls:

- chart-type selector,
- left/right axis assignment,
- metric normalization,
- watchlist save,
- weekly digest generation.

## MVP Views

### Overview

Shows the top cross-project changes for the selected timeframe.

Cards or table rows:

- largest TVL or AUM moves,
- largest volume moves,
- largest fee or revenue moves,
- largest market cap moves,
- new or changed source warnings,
- follow-up candidates.

### Compare

Lets Ian compare selected projects or sectors.

Charts:

- price performance,
- market cap and FDV,
- TVL or AUM,
- volume,
- fees,
- revenue,
- active users or wallets where available.

### Sector Detail

Shows one sector at a time.

Charts:

- sector total volume,
- project share of sector volume,
- sector TVL or AUM,
- top project changes,
- missing or low-confidence metrics.

### Project Detail

Shows one project at a time.

Sections:

- market data,
- usage/adoption,
- financials,
- tokenomics,
- project-specific metrics,
- source ledger,
- open questions,
- suggested research action.

### Research Queue

Turns dashboard observations into useful work.

Actions:

- save chart/stat,
- mark as newsletter mention,
- mark as dossier candidate,
- mark as needs verification,
- add open question.

## Data Model

Every metric observation should store:

- project,
- sector,
- metric name,
- metric category,
- value,
- unit,
- period,
- start date,
- end date,
- source name,
- source URL,
- source type,
- source relationship,
- pulled date,
- confidence,
- notes.

Metric categories:

- market,
- adoption,
- volume,
- financials,
- tokenomics,
- stablecoin,
- staking,
- project_specific.

Source relationships:

- native,
- parent,
- third_party.

Confidence levels:

- high: primary project, official protocol data, reputable data provider, or exact dashboard/API,
- medium: reputable third-party source or dashboard-derived data with clear definitions,
- low: social post, unclear methodology, stale source, or data needing confirmation.

## Data Source Discovery

Discovery should start with broadly reusable sources:

- DefiLlama,
- CoinGecko,
- Token Terminal,
- Artemis,
- Dune,
- TradingView embeds,
- project-native dashboards and APIs,
- official docs and disclosures.

For each source, record:

- whether it has a public API,
- whether it requires login,
- whether it allows programmatic access,
- available metrics,
- date coverage,
- rate limits or cost,
- and source confidence.

## MVP Acceptance Criteria

The MVP is acceptable when:

- the first project universe is confirmed,
- each MVP metric has a source map entry,
- missing metrics are clearly marked,
- at least one cross-project comparison view works,
- at least one project detail view works,
- every displayed metric has source, pulled date, and confidence,
- Ian can filter by timeframe, sector, and project,
- and dashboard observations can be routed into a research follow-up queue.

## First Build Sequence

1. Confirm starter project universe.
2. Complete metric inventory for those projects.
3. Map public data sources and access constraints.
4. Build a static sample dataset.
5. Prototype local dashboard shell.
6. Add source ledger display.
7. Add timeframe/project/sector filters.
8. Connect one reliable live source.
9. Add research follow-up queue output.
10. Review with Ian before expanding project-specific charts.
