# Dashboard Data Availability Comments

Date: 2026-06-09

Purpose: comment on Ian's requested dashboard charts and tables from a practical production standpoint. This is not a final source audit; it is a triage layer for what belongs in the free dashboard now, what needs source mapping, and what is probably impractical or costly for the free surface.

## Legend

- **Ready for free dashboard**: data is already wired or likely available from a broad source with acceptable caveats.
- **Needs source map**: useful, but definitions or project coverage vary enough that it should be sourced before charting.
- **Project detail only**: useful for one project, but not comparable across the whole category.
- **Likely costly/manual**: may require paid data, logged-in dashboards, private APIs, or recurring manual collection.
- **Defer**: unclear live status or not important enough for the two-week free-dashboard push.

## Cross-Project Metrics

| Chart/table | Comment | Status |
| --- | --- | --- |
| Market cap, FDV, token price, 24H token volume | Good shared comparison layer. These are token metrics, not proof of product adoption. | Ready for free dashboard |
| TVL | Good shared adoption/scale metric, but record-level notes must distinguish product, chain, vault, lending, and parent-protocol TVL. | Ready with caveats |
| Fees and revenue | Strong fundamentals layer. Definitions differ by source, so source notes should stay visible. | Ready with caveats |
| Active users/wallets | High-value but inconsistent. Current Dune rows cover only a narrow DEX surface. Artemis or Token Terminal may improve coverage but could add cost. | Needs source map |
| Volume by sector | Useful, but spot, perps, lending, vault, card, and bridge volume are not the same thing. Avoid one blended chart until each category has a clean definition. | Needs source map |
| TVL by type | Useful once the dashboard has product taxonomy. For now, a single TVL comparison is safer. | Needs source map |
| Treasury balance | Uneven disclosure and likely manual/project-native collection. | Likely costly/manual |
| Buybacks | Good value-accrual signal where available, but source coverage will be uneven. | Project detail only |
| Stablecoin supply and yield-bearing stablecoin supply | Good fit for asset-management and tokenization detail views. Needs exact product mapping. | Needs source map |
| APY, total yield paid, staking yield | Valuable for Machines & Money readers, but definitions are fragile and source-specific. | Project detail only |
| Locked-token ratio | Useful for ve-token projects, but not universal. | Project detail only |

## Category And Project Detail Notes

| Category/project | Chart/table | Comment | Status |
| --- | --- | --- | --- |
| Spot / Uniswap | LP fees paid out by token | Useful project detail, not sector-comparable without matching LP fee definitions for other DEXs. | Project detail only |
| Spot / Uniswap | UNI token burns | First confirm current burn mechanics and whether the metric exists as stated. | Needs source map |
| Spot / Curve | veCRV to CRV circulation ratio | Good project-detail tokenomics chart. | Project detail only |
| Spot / Curve | CRV incentives by timeframe | Requires reliable incentive definition and source. | Needs source map |
| Spot / Jupiter | Solana DEX aggregator volume share | Useful, but needs a trusted total Solana spot-volume denominator. | Needs source map |
| Spot / Jupiter | Active users by product | Product taxonomy needs confirmation. | Needs source map |
| Spot / Aerodrome | Base spot volume share | Useful if total Base spot volume source is reliable. | Needs source map |
| Spot / Aerodrome | veAERO and incentives | Good project-detail tokenomics, not broad comparison. | Project detail only |
| Derivatives / Pendle | PT and YT volume | High editorial value and project-specific. | Project detail only |
| Derivatives / Pendle | vePENDLE yield paid | Requires token-level source definitions. | Needs source map |
| Derivatives / Pendle | Boros stats | Needs product definition and live data confirmation before charting. | Defer |
| Derivatives / Hyperliquid | HIP-3 / HIP-4 volume | Useful but depends on current product status and provider breakdowns. | Needs source map |
| Derivatives / Hyperliquid | Liquidations by asset | Potentially useful but source quality must be verified. | Needs source map |
| Lending / Aave | V3 deposits and utilization | Good first project-detail candidate. | Needs source map |
| Lending / Aave | V4 hub and spoke deposits | Depends on V4 live data availability. | Defer |
| Lending / Morpho | AUM by vault, asset, curator | Good project-detail candidate; not a clean sector-wide comparison unless other lending projects expose the same shape. | Project detail only |
| Lending / Kamino | Looped assets, RWA deposits, utilization, APY | High complexity and Solana-specific source work. | Defer |
| Lending / Sky | sUSDS/stUSDS/SKY APY and yield paid | High Machines & Money value, but should be project-detail until source methodology is locked. | Project detail only |
| Tokenization / Ondo | Tokenized assets by asset sector | Good tokenization starter if sourced from RWA.xyz/Ondo consistently. | Needs source map |
| Tokenization / Maple | New loans originated and syrup stats | Useful but needs timeframe and product definitions. | Needs source map |
| Asset Mgmt / Ethena | USDe/sUSDe holders, staked ratio, yield, reserves | Very strong project-detail candidate. Reserve and attestation caveats must be prominent. | Project detail only |
| Asset Mgmt / EtherFi | Debit card spend and active users | Exactly the type of metric that should live in project detail, not sector comparison. It may not be public or may require disclosures/manual tracking. | Likely costly/manual |
| Asset Mgmt / EtherFi | Restaked ETH and yield | More practical than card spend; can likely use DefiLlama/EtherFi/Dune after source mapping. | Needs source map |
| Asset Mgmt / Falcon | Holders, collateral value, vault AUM, yield paid | Project-detail only until reserve/source confidence is proven. | Needs source map |
| Infra / Canton | Active users, burned tokens, institutional metrics | Institutional metrics are likely manual evidence, not an automated free-dashboard chart. | Likely costly/manual |
| Infra / LayerZero | Messages and value routed | Good infra metrics if LayerZero Scan/Dune definitions are stable. | Needs source map |
| AI / Virtuals | Agents, x402 volume, transactions, aGDP, revenue | Potentially high editorial value but source definitions need confirmation. | Needs source map |
| AI / Virtuals | Funds raised for builders | Likely announcement/manual tracking rather than dashboard data. | Likely costly/manual |

## Product Implication

The free dashboard should keep broad comparable metrics at the top: market cap, FDV, token volume, TVL, fees, revenue, DEX volume, and narrow usage where available.

The next UI layer should be:

1. Pick category.
2. Pick project.
3. Show all shared metrics for that project.
4. Add project-specific metrics only when they are meaningful for that project and clearly labeled as not sector-comparable.

That matches Ian's EtherFi card-spend example: it is valuable for EtherFi, but it should not be forced into an asset-management sector leaderboard where other projects do not have a comparable metric.
