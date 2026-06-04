# Token Metrics vs Product Metrics

Date: 2026-06-04

## Short Answer For Ian

For this dashboard, I am using **token metrics** to describe the asset itself and **product metrics** to describe how the protocol, app, or product is being used.

The key rule is:

> Token metrics tell us what the market is doing with the asset. Product metrics tell us what users are doing with the product.

Both are useful, but they should not be mixed without labels.

## Token Metrics

Token metrics are asset-level metrics. They apply to governance tokens, tradeable tokens, and sometimes stablecoins when we only need market context.

Examples:

- price,
- market cap,
- FDV,
- circulating supply,
- total supply,
- max supply,
- token trading volume,
- token buybacks,
- token burns,
- locked token ratio,
- staking or locking ratio.

Use token metrics to answer:

- How is the asset valued?
- How much of the supply is circulating or locked?
- Is the token gaining market interest?
- Is there a tokenomics story worth tracking?

Token metrics do **not** prove product usage by themselves.

Example:

- `UNI price` and `UNI market cap` are token metrics.
- They do not directly tell us whether Uniswap volume, liquidity, fees, or users are rising.

## Product Metrics

Product metrics are usage, adoption, and business metrics for the protocol, app, product, market, or stablecoin system.

Examples:

- active users or wallets,
- transaction count,
- protocol volume,
- sector volume share,
- TVL,
- AUM,
- deposits,
- borrows,
- utilization,
- fees,
- revenue,
- stablecoin supply,
- staked stablecoin supply,
- APY,
- yield paid,
- reserves,
- collateral mix,
- holders,
- product-specific volume.

Use product metrics to answer:

- Is the product actually being used?
- Are users, volume, assets, or revenue growing?
- Is the project gaining share in its sector?
- Is the product generating yield or cash flow?
- Is this useful enough for Ian to write about?

## Special Cases

### Locked Governance Tokens

Examples:

- `veCRV`,
- `veAERO`,
- `vePENDLE`.

These are not normal market-cap tokens in the dashboard. Treat them as tokenomics/product-governance metrics.

Track:

- locked supply,
- locked-to-circulating ratio,
- voting power,
- incentives,
- emissions,
- yield paid to lockers.

### Stablecoin Products

Examples:

- `crvUSD`,
- `USDS`,
- `USDe`,
- `USDf`,
- `sUSDS`,
- `sUSDe`,
- `sUSDf`,
- `syrupUSDC`,
- `syrupUSDT`.

These should mostly be treated as product metrics, not token-market proxies.

Track:

- supply,
- holders,
- peg,
- reserves,
- collateral,
- APY,
- yield paid,
- staked/base ratio,
- mint/redemption activity where available.

### Governance Tokens For Product Companies

Examples:

- `AAVE`,
- `HYPE`,
- `PENDLE`,
- `SKY`,
- `ONDO`,
- `MORPHO`,
- `ZRO`,
- `VIRTUALS`.

These can be tracked with market data, but the dashboard should keep them separate from product metrics.

For example:

- `HYPE market cap` is a token metric.
- `Hyperliquid perps volume` is a product metric.
- `Hyperliquid HLP TVL` is a product metric.

## Dashboard Labeling Rule

Every metric row should carry one of these roles:

- `governance_token`
- `stablecoin_product`
- `yield_bearing_stablecoin`
- `locked_governance_position`
- `protocol_usage`
- `financials`
- `sector_share`

This lets the dashboard compare related things without pretending they are the same kind of data.

## Current Priority Order From Ian

After market data, Ian prioritized:

1. Active users/wallets
2. Sector volume share
3. Stablecoin APY
4. Yield paid
5. Lending utilization

## Build Implication

The next market-data layer can start with confirmed governance tokens and tradeable assets. Product assets and special cases should enter the dashboard only when the source can support the right product metric.

In practice:

- Pull market cap/FDV for governance tokens.
- Pull supply/APY/yield/reserve metrics for stablecoin products.
- Pull locked-supply and incentive metrics for ve-token positions.
- Pull usage and financial metrics separately from token market data.
