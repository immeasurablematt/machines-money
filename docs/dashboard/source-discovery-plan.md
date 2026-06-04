# Machines & Money Dashboard Source Discovery Plan

Date: 2026-06-02

## Purpose

Turn Ian's dashboard outline into a verified source map before building the dashboard.

The discovery pass should find which metrics are available, which are reliable, and which are too expensive or ambiguous for MVP.

## Discovery Outputs

Create these artifacts before dashboard implementation:

- metric inventory,
- source map,
- project universe,
- metric definition notes,
- sample dataset,
- dashboard MVP backlog.

## Source Map Columns

Use these columns for source mapping:

- project,
- sector,
- metric,
- source name,
- source URL,
- source type,
- source relationship,
- access method,
- public API yes/no,
- login required yes/no,
- paid access yes/no,
- date coverage,
- update cadence,
- definition notes,
- confidence,
- MVP inclusion,
- blocker,
- next action.

## Source Types

- project_native_dashboard,
- project_native_api,
- official_docs,
- official_announcement,
- data_provider,
- public_dashboard,
- embedded_chart,
- social_x,
- manual_disclosure,
- unknown.

## Source Relationships

- native,
- parent,
- third_party.

## Recommended Discovery Order

1. Confirm Ian's first 10 to 20 projects.
2. Check broadly reusable data providers.
3. Check project-native dashboards and APIs for the starter projects.
4. Check Dune and other public dashboards for project-specific gaps.
5. Mark metrics that require paid or logged-in sources.
6. Produce a sample dataset from reliable public sources.
7. Prototype the dashboard shell against the sample dataset.

## Broad Data Providers To Check

- DefiLlama,
- CoinGecko,
- Token Terminal,
- Artemis,
- Dune,
- RWA.xyz,
- TradingView embeds,
- project-native analytics pages.

## Questions To Answer During Discovery

- Which metrics can be pulled without login or paid access?
- Which metrics are available by project but not by sector?
- Which metrics need manual review before reuse?
- Which metrics are available daily versus weekly or monthly?
- Which metrics have unstable definitions across providers?
- Which metrics can be trusted enough for Ian to cite?
- Which charts should become source-linked research notes instead of dashboard widgets?

## MVP Source Rules

- Prefer public APIs or stable project-native dashboards.
- Store every source URL and pulled date.
- Show confidence in the UI or source ledger.
- Keep missing metrics visible.
- Do not infer unavailable metrics from nearby data unless the method is explicit.
- Do not mix sources in one chart without labeling the source per series.

## First Data Pull Candidate

The first data pull should use public, reusable sources only.

Candidate starter metrics:

- token price,
- market cap,
- FDV,
- TVL,
- fees,
- revenue.

Candidate starter sources:

- DefiLlama,
- CoinGecko,
- Token Terminal if accessible.

This lets the dashboard prototype prove the filtering and comparison workflow before harder project-specific metrics are added.

## Started Source Checks

The first source check confirmed reachable DefiLlama public protocol records for the proposed starter project set. See:

- `docs/dashboard/starter-source-map.csv`
- `docs/dashboard/source-check-notes.md`

The main finding is that several projects split into multiple product/version records, so dashboard labels and aggregation rules need to be explicit before a prototype shows rolled-up numbers.

## Free Data Expansion

The next recommended no-paid-data layer is market data: token price, market cap, FDV, and token volume. See:

- `docs/dashboard/free-data-expansion-quote.md`
- `docs/dashboard/ian-confirmed-dashboard-scope.md`
- `docs/dashboard/starter-token-map.csv`
- `docs/dashboard/token-vs-product-metric-definitions.md`

Active users and wallet counts should stay in source discovery until Dune/project-native sources are mapped for each project.
