# Machines & Money Dashboard Runbook

## Purpose

This runbook explains how to refresh and review the static dashboard prototype.

The prototype is still intentionally source-first. It should help Ian react to the dashboard shape while keeping source coverage, confidence, and aggregation limits visible.

## Open The Prototype

Open:

- `docs/dashboard/prototype.html`

The page loads:

- `docs/dashboard/generated-dashboard-data.js`

That generated JavaScript file lets the local HTML work from `file://` without needing a web server.

## Hosted Preview

The current here.now preview is tracked in:

- `docs/dashboard/here-now.md`

Anonymous here.now publishes expire after 24 hours unless claimed. Keep the claim URL outside the repo because it contains the one-time claim token.

## Refresh The Data

From the repo root:

```bash
python3 scripts/refresh_dashboard_data.py
```

The script writes:

- `docs/dashboard/generated-dashboard-data.csv`
- `docs/dashboard/generated-dashboard-data.js`

Current generated metrics:

- TVL
- 30D Fees
- 30D Revenue
- 30D DEX Volume

Optional generated metrics after a free CoinGecko Demo key is available:

- Token Price
- Market Cap
- FDV
- 24H Token Volume

To enable the market-data layer, set:

```bash
export COINGECKO_DEMO_API_KEY=...
python3 scripts/refresh_dashboard_data.py
```

Only `verified_search` rows in `docs/dashboard/starter-token-map.csv` are pulled. Rows marked `needs_confirmation` are skipped until Ian confirms the token/product mapping.

## Current Source Coverage

The refresh script uses public DefiLlama endpoints.

Good current coverage:

- protocol TVL,
- 30D fees where DefiLlama exposes a protocol fees record,
- 30D revenue where DefiLlama exposes a protocol revenue record,
- 30D DEX volume for DEX records.

Known gaps:

- derivatives volume is not consistently available through the same public endpoint,
- lending volume/utilization needs project-native or dashboard-specific discovery,
- active users still need Artemis, Token Terminal, Dune, project-native dashboards, or another verified source,
- stablecoin reserves, APY, and yield paid need project-native source checks,
- curator-level lending data needs Morpho/Kamino/Euler-specific discovery.

## Review Checklist

Before showing a metric as cite-ready:

- confirm the source URL,
- check the metric period,
- check whether the record is project-native, product-specific, or third-party,
- keep product/version records labeled,
- avoid silently summing records like Uniswap V2/V3/V4 or Aerodrome V1/Slipstream,
- treat medium-confidence rows as exploratory.

## Next Build Step

After Ian confirms the metric selector and source-first layout, the next useful step is a small hosted version or a local app shell that can refresh data on demand.

For the no-paid-data expansion plan and Ian quote, see:

- `docs/dashboard/free-data-expansion-quote.md`
- `docs/dashboard/ian-confirmed-dashboard-scope.md`
- `docs/dashboard/token-vs-product-metric-definitions.md`
- `docs/dashboard/dune-active-wallets.md`
