# Free API Source Map

Date: 2026-06-04

This is the verified free-data source map for the Machines & Money dashboard.

The goal is to avoid paid data subscriptions while still building a dashboard Ian can trust. The practical answer is that we should not rely on one provider. Use free aggregators for broad coverage, then project-native APIs where they exist.

## Best Sources To Use First

### 1. DefiLlama

Use for:

- TVL
- fees
- revenue
- DEX volume
- stablecoin supply
- stablecoin history
- APY/yield pools

Verified live on 2026-06-04:

- `https://api.llama.fi/protocols`
- `https://api.llama.fi/overview/fees?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true`
- `https://api.llama.fi/overview/dexs?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true`
- `https://stablecoins.llama.fi/stablecoins`
- `https://yields.llama.fi/pools`

Why it matters:

DefiLlama is the best free backbone for the MVP because it covers most of Ian's 20 projects and already powers the prototype.

Important note:

Stablecoin and yield endpoints use separate live hosts (`stablecoins.llama.fi` and `yields.llama.fi`) even though the API docs map them as part of the free DefiLlama API family.

## Market Data Sources

### CoinGecko

Use for:

- token price
- market cap
- FDV
- 24H volume
- circulating supply
- total supply
- token metadata

Status:

- Keyless `/ping` endpoint verified live.
- Free Demo plan verified in current pricing docs.
- User still needs to create the free Demo API key before production refreshes.

Free tier from current docs:

- 10,000 call credits/month
- 100 calls/minute
- no credit card required
- attribution required

Use CoinGecko as the primary token market-data source.

### CoinPaprika

Use for:

- backup token price
- backup market cap
- backup volume
- historical OHLC
- coin metadata

Verified live on 2026-06-04:

- `https://api.coinpaprika.com/v1/tickers/uni-uniswap`

Use as a backup because token IDs differ from CoinGecko and the free quota is smaller.

### CoinMarketCap

Use for:

- backup latest token market data

Status:

- Free Basic plan verified from current pricing docs.
- Not live-tested because it needs an API key.

Free tier from current docs:

- 15,000 call credits/month
- 50 requests/minute
- personal use only
- no historical data

Use only if we need another market-data backup. CoinGecko is cleaner for this project.

## DEX / Pool Data Sources

### GeckoTerminal

Use for:

- pool liquidity
- pool volume
- token/pool discovery
- DEX token OHLCV

Verified live on 2026-06-04:

- `https://api.geckoterminal.com/api/v2/networks`

Current public API rate limit:

- 30 calls/minute

Use as the first DEX-pool fallback after DefiLlama.

### DEX Screener

Use for:

- DEX pairs
- token profiles
- liquidity
- pair search
- long-tail token discovery

Verified live on 2026-06-04:

- `https://api.dexscreener.com/token-profiles/latest/v1`

Docs show endpoint-specific rate limits such as 60/minute and 300/minute.

Use as a discovery/fallback source, not the primary dashboard source.

### DexPaprika

Use for:

- DEX pools
- token/pool search
- OHLCV
- batch prices

Verified live on 2026-06-04:

- `https://api.dexpaprika.com/networks`

Use as another no-key DEX fallback. It is promising, but should be tested more deeply before becoming a main dependency.

## Query Engines And Raw Chain Data

### Dune

Use for:

- active users/wallets
- protocol-specific SQL metrics
- sector share when aggregators are not enough
- project-specific public dashboards

Status:

- Free query engine/API access verified from current docs.
- Not live-tested because it needs a Dune API key.

Use Dune for Ian's top post-market-data metric: active users/wallets.

### The Graph

Use for:

- protocol events
- swaps
- pools
- lending positions
- time-series subgraph data

Status:

- Free plan verified from current docs.
- Not live-tested because The Graph Network query URLs require an API key.

Free tier from current docs:

- 100,000 queries/month

Use for Uniswap, Aave, Euler, and other EVM protocols when project-native APIs or DefiLlama are not enough.

### Etherscan

Use for:

- EVM transaction lookup
- token transfers
- logs
- contract ABI
- balances

Status:

- Free tier verified from current docs.
- Not live-tested because it needs an API key.

Free tier from current docs:

- 3 calls/second
- up to 100,000 calls/day
- selected chains only

Use only for verification/backfill. It is too raw to be the main dashboard source.

### Alchemy

Use for:

- reliable EVM/Solana RPC
- logs
- transfers
- token data
- webhooks

Status:

- Free plan verified from current docs.
- Not live-tested because it needs an API key.

Free tier from current docs:

- 30M compute units/month
- 25 requests/second

Use if raw-chain reads become a real requirement.

### Solana Public RPC / Helius

Use for:

- Solana raw-chain reads
- parsed transactions
- account data
- Jupiter/Kamino active wallets if no better source exists

Verified live:

- Solana public RPC health check returned `ok`.

Important note:

Solana's public RPC is shared infrastructure and not meant for production traffic. Helius has a free tier and is the better free option for repeatable Solana ingestion.

## Project-Native Sources

### Live Verified Native APIs

These responded successfully in live tests:

- Aave GraphQL: `https://api.aave.com/graphql`
- Hyperliquid Info API: `https://api.hyperliquid.xyz/info`
- Pendle API: `https://api-v2.pendle.finance/core/v2/markets/all?limit=1`
- Morpho GraphQL: `https://api.morpho.org/graphql`
- Kamino API: `https://api.kamino.finance/kvaults/summary`
- Centrifuge GraphQL: `https://api.centrifuge.io`
- Maple GraphQL: `https://api.maple.finance/v2/graphql`
- Ethena public API, limited: `https://public.api.ethena.fi/asset-availability`
- LayerZero Scan API: `https://scan.layerzero-api.com/v1/messages/latest`

These are high-priority because they are closer to the protocol than a third-party aggregator.

## Project Coverage Notes

### Strong Free API Coverage

- Uniswap: DefiLlama, CoinGecko, The Graph, DEX APIs
- Aave: DefiLlama, Aave GraphQL, Aave subgraphs, The Graph
- Pendle: DefiLlama, Pendle native API
- Hyperliquid: DefiLlama, Hyperliquid native Info API
- Ethena: DefiLlama stablecoins/yields, Ethena limited public API
- Sky: DefiLlama stablecoins/yields, Sky contracts/docs
- Morpho: DefiLlama, Morpho GraphQL
- Jupiter: DefiLlama, Jupiter APIs, Solana/Helius, DEX APIs
- Kamino: DefiLlama, Kamino API, Solana/Helius
- Euler: DefiLlama, Euler subgraphs
- Centrifuge: DefiLlama, Centrifuge API
- Maple: DefiLlama, Maple GraphQL
- LayerZero: LayerZero Scan API, Dune

### Partial Or Still Needs Source Discovery

- Curve: DefiLlama and DEX APIs are good; clean native API for veCRV/gauge detail still needs verification.
- Aerodrome: DefiLlama and DEX APIs are good; native veAERO/emissions source still needs verification.
- Ondo: DefiLlama is good; RWA.xyz may be ideal but appears keyed/request-access.
- EtherFi: DefiLlama is good; no clean public native API verified yet.
- Falcon: public website shows TVL, USDf supply, and APY, but no documented API found.
- Canton: official docs explain Canton Coin; CC View appears to provide a keyed API, but free access was not verified.
- Virtuals: public website and token market data are available, but no clean product-metric API was verified.

## Recommended Build Order

1. Add CoinGecko market data once the free Demo key is available.
2. Add DefiLlama stablecoin and yield endpoints.
3. Add project-native APIs for Morpho, Pendle, Kamino, Centrifuge, Maple, Hyperliquid, and LayerZero.
4. Add Dune for active users/wallets once we have a free Dune key.
5. Use The Graph, Etherscan, Alchemy, Helius, and raw RPC only for metrics that cannot be obtained cleanly from a native API or aggregator.

## Bottom Line

We can build a meaningful no-paid-data dashboard, but not every Ian metric has a clean free API.

Best free coverage:

- market data
- TVL
- fees/revenue
- DEX volume
- stablecoin supply
- APY/yield pool data
- several project-native lending and tokenization metrics

Hardest free coverage:

- active users/wallets across all 20 projects
- exact sector share outside DEX volume
- ve-token incentive/yield data
- Falcon, Canton, and Virtuals product metrics

The best next step is to wire the sources we already verified, then quote any remaining source-discovery work separately.

