# Dashboard Source Check Notes

Date: 2026-06-02

## What Was Checked

The first live source check used DefiLlama public protocol records for the proposed starter project set:

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

The check confirmed reachable DefiLlama protocol records for the core projects and identified where projects split into multiple source records.

## Important Splits

These projects should not be treated as a single undifferentiated metric source:

- Uniswap: V2, V3, and V4 have separate records.
- Aave: V3, V4, and additional Aave variants have separate records.
- Hyperliquid: bridge, HLP, spot orderbook, and perps are separate records.
- Ethena: USDe, USDtb, and tsUSDe are separate records.
- Sky: lending, money, and RWA have separate records.
- Ondo: yield assets and global markets are separate records.
- Aerodrome: Slipstream and V1 are separate records.
- Jupiter: aggregator, perps, lend, staked SOL, prediction, and other products are separate records.

## MVP Implication

The first dashboard should show source/product labels clearly. It should not silently sum related records unless the dashboard explicitly says how the aggregation was done.

For example:

- `Uniswap TVL` may mean V2 + V3 + V4, or only the current primary version.
- `Hyperliquid activity` may mean perps volume, HLP TVL, bridge TVL, or spot orderbook activity.
- `Jupiter usage` may mean aggregator volume, perps, lending, prediction markets, staking, or another product.

## First Reliable Metrics

The best first metrics for a prototype are:

- protocol TVL or AUM,
- token price,
- market cap,
- FDV,
- fees,
- revenue.

DefiLlama is a good starting source for protocol TVL and some fee/revenue checks, but not every project-specific metric in Ian's outline.

## Metrics Still Needing Source Discovery

These are high-value but should not be charted until source definitions are verified:

- active users,
- project share of sector volume,
- PT/YT volume,
- ve-token yield paid by token,
- Hyperliquid HIP-3 and HIP-4 volume,
- lending utilization by hub/spoke/vault,
- curator-level lending data,
- yield paid by asset,
- stablecoin reserves and collateral composition,
- tokenized asset mints and holders,
- institutional Canton metrics,
- AI agent transaction and revenue metrics.

## Next Discovery Step

Build a sample dataset from the first reliable metric group:

- project,
- product/source record,
- sector,
- metric,
- value,
- unit,
- period,
- source URL,
- pulled date,
- confidence.

That sample dataset should drive the first dashboard prototype.

The first sample snapshot is saved at:

- `docs/dashboard/sample-protocol-tvl-2026-06-02.csv`

A static prototype using the sample data is saved at:

- `docs/dashboard/prototype.html`

The prototype now also supports generated multi-metric data:

- `docs/dashboard/generated-dashboard-data.csv`
- `docs/dashboard/generated-dashboard-data.js`
- `scripts/refresh_dashboard_data.py`

The first generated pass includes TVL, 30D fees, 30D revenue, and 30D DEX volume where public DefiLlama source coverage exists.
