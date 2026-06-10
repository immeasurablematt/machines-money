# Machines & Money Dashboard: Free Data Expansion Quote

Date: 2026-06-03

## Plain-English Recommendation

Build the next dashboard layer using only free/public data.

The best next metric layer is **market data**:

- token price,
- market cap,
- FDV,
- 24h volume,
- 7d / 30d price movement where available.

This is more reliable as a no-paid-data addition than active users. Active users are valuable, but they are not consistently available through the same free public source across Ian's project list.

## Suggested Quote For Ian

**Scope:** Add a no-paid-data market layer to the Machines & Money dashboard and map the remaining active-user / usage metrics into a source backlog.

**Data cost:** $0.

**Estimated build effort:** 10 to 14 hours.

**Review / iteration buffer:** 2 to 3 hours.

**Total recommended quote:** 12 to 17 hours of work, with no paid data subscription.

If Ian wants a fixed-scope version, quote it as:

> Build a no-paid-data market layer for the dashboard, including token price, market cap, FDV, source confidence, and a source backlog for active users and harder project-specific metrics. Data subscription cost: $0. Estimated delivery: 2 to 3 working sessions after token mappings and a free API key are confirmed.

## What This Includes

- Add CoinGecko market-data integration using the free Demo plan or approved keyless path.
- Add token mapping for the starter project universe.
- Add dashboard metrics for price, market cap, FDV, and 24h volume where available.
- Keep source URLs, pulled date, and confidence visible.
- Keep project/product record labels visible so token-level and protocol-level metrics are not mixed.
- Add a backlog table for active users, wallets, utilization, yield paid, and other harder metrics.
- Add notes on which metrics need Dune, project-native dashboards, or manual source review.

## What This Does Not Include

- Paid API subscriptions.
- Guaranteed active-user coverage across all projects.
- Custom Dune query engineering for every project.
- Wallet connections, trading, staking, deposits, or protocol interactions.
- Subscriber-facing production hardening.

## What Matt Can Help With

Ask Ian for these four things:

1. **Confirm the starter project list.**
   Complete. Ian confirmed the first 20 projects. See `docs/dashboard/ian-confirmed-dashboard-scope.md`.

2. **Confirm token mappings.**
   Complete at the business level. CoinGecko IDs still need verification for rows marked `needs_verification`.

   Starter mapping file:

   - `docs/dashboard/starter-token-map.csv`

3. **Create or approve a free CoinGecko Demo API key.**
   This is still $0, but it is better than depending on an unstable keyless path.

4. **Choose the next priority after market data.**
   Complete. Ian ranked the next metrics as active users/wallets, sector volume share, stablecoin APY, yield paid, and lending utilization.

## Free Source Assessment

### DefiLlama

Use for:

- TVL,
- historical protocol TVL,
- fees,
- revenue,
- DEX volume,
- stablecoin supply,
- yields.

DefiLlama's free API requires no authentication and already powers the current dashboard prototype. Its Pro API adds exclusive datasets such as active users and higher limits, but that would introduce paid cost.

### CoinGecko

Use for:

- token price,
- market cap,
- FDV,
- token volume,
- historical market charts where plan limits allow.

CoinGecko has a free Demo plan with a monthly call cap and rate limit. That should be enough for an internal dashboard prototype with a small starter project list.

### GeckoTerminal

Use for:

- DEX token/pool price,
- liquidity,
- OHLCV,
- pool-level volume,
- onchain token/pool context.

GeckoTerminal is useful when token-level DEX data matters more than broad market data. It is free but beta, and rate limits are lower than paid CoinGecko access.

### Dune

Use for:

- active users,
- wallet counts,
- project-specific utilization,
- custom onchain calculations,
- protocol-specific dashboards.

Dune can support no-paid-data work, but it requires manual query/dashboard discovery and may need a free account/API key. It is not as quick as CoinGecko or DefiLlama for a broad dashboard layer.

### Token Terminal / Artemis

Use as:

- research references,
- manual review sources,
- possible future paid-source candidates.

Do not build the next automated layer around these if the constraint is no paid data.

## Recommended Build Order

1. Add token mapping CSV for the starter projects.
2. Add free CoinGecko market data to `scripts/refresh_dashboard_data.py`.
3. Add market metrics to the dashboard metric selector.
4. Add source confidence notes for token-level versus protocol-level metrics.
5. Add backlog rows for active users and harder project metrics.
6. Republish the here.now preview for Ian review.

## Prework Completed While Waiting For Ian

- Added `docs/dashboard/starter-token-map.csv`.
- Added `docs/dashboard/ian-confirmed-dashboard-scope.md`.
- Added `docs/dashboard/token-vs-product-metric-definitions.md`.
- Added CoinGecko-ready market-data scaffolding to `scripts/refresh_dashboard_data.py`.
- The refresh script now skips market data unless `COINGECKO_DEMO_API_KEY` is set.
- Rows marked `needs_confirmation` are skipped until Ian confirms the token/product mapping.
- The prototype metric order is ready for Token Price, Market Cap, FDV, and 24H Token Volume once generated.

## Key Risk

The main risk is not cost. The main risk is **metric mismatch**:

- TVL is protocol/product-level.
- Market cap and FDV are token-level.
- Active users are app/protocol-level and often source-specific.

The dashboard should keep these labels visible so Ian does not accidentally compare different kinds of metrics as if they were equivalent.
