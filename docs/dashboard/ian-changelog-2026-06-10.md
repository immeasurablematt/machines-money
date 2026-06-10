# Machines & Money — Changelog for Ian

Date: 2026-06-10
Live site: https://immeasurablematt.github.io/machines-money/ (dashboard at /dashboard.html)

Everything below shipped today and is live. Ten minutes to review; the open questions for you are at the bottom.

## The welcome page (new)

- New public landing page: headline "Know Where the Money Is Moving Before the Crowd Does", Milk Road-style layout — copy and email signup left, live stats right.
- Beehiiv subscribe form embedded directly on the page (no link-out), dark-themed, with the line: "Join Machines & Money for onchain finance research that doesn't waste your time."
- One interactive aggregate chart with three toggleable series, per your spec:
  - **DeFi20 total TVL** — mint area, dollar axis (left), full year of history.
  - **Share of all DeFi** — dashed blue line, percent axis (right): the DeFi20's slice of all DeFi TVL over time.
  - **% of Bitcoin (market cap)** — dotted amber line: the DeFi20's combined market cap as a share of Bitcoin's, the price-based market-share view. Today: **2.66% of Bitcoin**.
- Hover anywhere on the chart for a crosshair with exact date, TVL, DeFi share, and %-of-Bitcoin readouts.
- "Machines & Money Pro is coming" section with three locked preview cards (value-accrual scorecard, project deep pages, growth & share trends).
- Founders section stubbed — waiting on your bio; expands when John is back.

## The free dashboard

- Category cards now switch the featured metric per vertical (your feedback): Lending → Outstanding Borrows, Derivatives → Perps Volume, Asset Mgmt → Stablecoin Supply, Spot → DEX Volume.
- New chart tabs: Perps Volume, Borrows, Stablecoins.
- Data grew from 137 rows / 4 metric families to **308 rows / 22 metric families**, all free sources: 7D+30D fees and revenue, fee growth (7D/30D), TVL growth, holders revenue (value-accrual input), DEX volume share, outstanding borrows (defined as current stock, not daily flow), stablecoin supplies (USDe, USDtb, USDf, USDY, USDS), live sUSDe/sUSDS APY, token performance (24H/7D/30D/1Y), and 7D active wallets from Dune (deduped unique addresses).

## Behind the scenes

- Data refreshes itself daily (and on demand) via GitHub Actions, validates before publishing, keeps dated snapshots, and restores last-known-good data if a pull fails. Site redeploys automatically when data changes.
- Cost: $0/month. CoinGecko and Dune free keys are installed as encrypted secrets (an earlier accidental key exposure was caught, both keys rotated same hour).
- Growth/share history is now accruing daily, which is what makes Pro's trend charts possible later.

## Known data limits (honest list)

- **Aggregate derivatives volume is paywalled** — DefiLlama moved it to their paid API (HTTP 402). Free path: Hyperliquid's own public API, planned for the next data phase. Until then perps volume shows only where free records exist.
- **Altcoin-market history** isn't on any free tier, so the Bitcoin comparison is DeFi20-vs-BTC over time (current-day altcoin total is still collected).
- Active-wallet coverage remains narrow (3 DEX records) until the Dune phase expands it.

## What we need from you

1. **Copy sign-off** on the welcome page headline and lede — and a phone check of the layout.
2. **Your bio** (2–3 sentences) for the founders section.
3. **Value-accrual scorecard spec** — the Pro teaser references it; the data input (holders revenue) is already flowing.
4. Your pass through the DeFi20 dashboard doc flagging which sector data points are impractical — we've hit the first one (paid derivatives aggregate) and want your priorities before the Dune build.
5. Does John's DefiLlama plan include **API** access (separate $300/mo product, not the Pro website)? It would unlock the paywalled derivatives/users endpoints if so.
