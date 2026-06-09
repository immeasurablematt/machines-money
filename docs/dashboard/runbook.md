# Machines & Money Dashboard Runbook

## Purpose

This runbook explains how to refresh and review the static dashboard files.

There are two dashboard surfaces:

- `docs/dashboard/free.html` is the public free dashboard for audience growth, social sharing, and newsletter conversion.
- `docs/dashboard/prototype.html` is the broader/pro research prototype.

Keep those surfaces separate. Do not overwrite `prototype.html` while working on the free dashboard.

## Open The Dashboards

For the free public dashboard, open:

- `docs/dashboard/free.html`

For the broader/prototype research dashboard, open:

- `docs/dashboard/prototype.html`

Both pages load:

- `docs/dashboard/generated-dashboard-data.js`

That generated JavaScript file lets the local HTML work from `file://` without needing a web server.

For a closer production check, serve the dashboard directory:

```bash
cd docs/dashboard
python3 -m http.server 8765
```

Then open:

- `http://127.0.0.1:8765/free.html`

## Hosted Preview

The current here.now preview is tracked in:

- `docs/dashboard/here-now.md`

Anonymous here.now publishes expire after 24 hours unless claimed. Keep the claim URL outside the repo because it contains the one-time claim token.

For free-dashboard work, publish `docs/dashboard/free.html` as `index.html`. For broader/prototype work, publish `docs/dashboard/prototype.html` as `index.html`. The two bundles should not be mixed.

## Refresh The Data

From the repo root:

```bash
python3 scripts/refresh_dashboard_data.py
```

The script writes:

- `docs/dashboard/generated-dashboard-data.csv`
- `docs/dashboard/generated-dashboard-data.js`
- `docs/dashboard/snapshots/dashboard-data-YYYY-MM-DD.csv`
- `docs/dashboard/snapshots/dashboard-data-YYYY-MM-DD.js`
- `docs/dashboard/last-good/generated-dashboard-data.csv`
- `docs/dashboard/last-good/generated-dashboard-data.js`

The refresh script validates row count, required metric families, and warning volume before replacing the live generated files. If a refresh fails or validates poorly, it restores the last-known-good generated files instead of publishing broken data.

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

## Free Dashboard Production Refresh Path

Near-term production refresh:

1. Run `python3 scripts/refresh_dashboard_data.py`.
2. Review `docs/dashboard/generated-dashboard-data.csv` for source, period, confidence, and notes.
3. Open `docs/dashboard/free.html` locally or over HTTP.
4. Confirm the selected-metric source panel uses the expected sources and caveats.
5. Publish `free.html` plus `generated-dashboard-data.js` together.

Future scheduled refresh:

- run the same refresh script on a schedule,
- keep dated raw or generated snapshots so 7D/30D growth can be calculated,
- deploy the updated static files to the permanent dashboard URL,
- alert or stop publish if row count, source confidence, or generated warnings change unexpectedly.

The scheduled workflow template is:

- `docs/dashboard/free-dashboard-refresh-workflow.yml`

To activate it, copy it to `.github/workflows/free-dashboard-refresh.yml` from a GitHub account or token with workflow-file permission. It runs daily and can also be triggered manually. It refreshes the data, builds the free-dashboard static bundle, and commits changed generated data/snapshots back to the repo. Optional secrets:

- `COINGECKO_DEMO_API_KEY`
- `DUNE_API_KEY`

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

Before sharing the free dashboard publicly:

- confirm `free.html` and `generated-dashboard-data.js` load over HTTP,
- confirm category, timeframe, metric, sector, and sort controls work,
- confirm selected-metric source confidence and caveats are visible,
- confirm the Beehiiv CTA points to `https://machinesandmoney.beehiiv.com`,
- confirm share controls use the current dashboard URL,
- confirm `docs/dashboard/prototype.html` has no unintended diff,
- confirm the URL is permanent before using it in social posts or newsletter links.

## Next Build Step

For the free dashboard, the next useful production step is a durable hosted preview or permanent public URL that serves `free.html` and `generated-dashboard-data.js` together.

For the broader/prototype dashboard, the next useful step remains deeper source discovery and a local app shell or hosted version that can refresh data on demand.

For the no-paid-data expansion plan and Ian quote, see:

- `docs/dashboard/free-data-expansion-quote.md`
- `docs/dashboard/ian-confirmed-dashboard-scope.md`
- `docs/dashboard/token-vs-product-metric-definitions.md`
- `docs/dashboard/dune-active-wallets.md`
- `docs/dashboard/chart-and-data-organization.md`
