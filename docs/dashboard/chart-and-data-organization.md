# Chart And Data Organization Notes

Date: 2026-06-05

## Should Every Chart Be A Bar Chart?

No. The prototype uses bar charts because the current data is mostly one-point snapshots by project or product record. Bar charts are the right first chart type for ranking and comparing current values.

Recommended chart types by metric:

- **Current rankings:** bar chart
  - TVL
  - Market cap
  - FDV
  - 24H token volume
  - 7D active wallets

- **Change over time:** line chart
  - token price history
  - TVL history
  - active wallets over time
  - APY history

- **Composition:** stacked bar or treemap
  - stablecoin supply by chain
  - protocol TVL by product
  - sector share
  - collateral or reserve mix

- **Yield comparison:** dot plot or ranked bar
  - stablecoin APY
  - yield paid
  - lending utilization

- **Research opportunity view:** scatter plot
  - market cap vs active wallets
  - FDV vs revenue
  - TVL vs fees

The first non-bar visual is a **research opportunity scatter plot** that helps Ian find gaps like high usage with lower market attention, or high valuation with weak product traction.

Current scatter plot:

- X-axis: Market Cap
- Y-axis: 7D Active Wallets
- Bubble size: TVL where available, otherwise market cap
- Color: sector

This is intentionally narrow. It only includes projects where the current generated data has both market cap and active-wallet rows.

## How The Pulled Data Is Stored

The dashboard currently stores data as generated static files under `docs/dashboard/`.

Main files:

- `scripts/refresh_dashboard_data.py`
  - pulls data from the APIs
  - normalizes it into one shared row format
  - writes the generated dashboard files

- `docs/dashboard/starter-token-map.csv`
  - maps projects and tokens to CoinGecko IDs
  - separates verified token rows from product-only rows

- `docs/dashboard/generated-dashboard-data.csv`
  - spreadsheet-readable copy of the current pulled data
  - useful for review, QA, and source checks

- `docs/dashboard/generated-dashboard-data.js`
  - browser-ready copy of the same data
  - loaded directly by `prototype.html`

- `docs/dashboard/prototype.html`
  - static dashboard UI
  - reads `window.dashboardRows` from `generated-dashboard-data.js`

## Current Row Shape

Every generated data row uses the same fields:

- pulled date
- project
- record
- sector
- metric
- value
- unit
- period
- source name
- source URL
- source relationship
- confidence
- notes

This keeps token metrics, protocol metrics, Dune metrics, and DefiLlama metrics in one comparable ledger without pretending they are the same type of data.

## Current Source Organization

Current wired sources:

- DefiLlama
  - TVL
  - 30D fees
  - 30D revenue
  - 30D DEX volume

- CoinGecko
  - token price
  - market cap
  - FDV
  - 24H token volume

- Dune
  - 7D active wallets for the first DEX surface

## Better Future Storage Model

If this moves beyond prototype, split the generated data into source-specific raw snapshots plus a normalized table:

- `data/raw/defillama/<date>.json`
- `data/raw/coingecko/<date>.json`
- `data/raw/dune/<date>.json`
- `data/normalized/dashboard-metrics.csv`

That would make it easier to audit changes, rerun transformations, and explain exactly where a number came from.
