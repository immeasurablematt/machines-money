# DeFi20 Dashboard — Metric Availability & Cost Map

Date: 2026-06-11. Maps every metric in Ian's free-Dune outline to source status, verified against live API behavior (not just docs).

**Legend:**
- ✅ **Live now** — already on the dashboard, $0
- 🟢 **Free, buildable** — source verified free; just needs wiring
- 🟡 **Dune** — needs forked/scheduled Dune queries (free tier ≈ $0, worst case $5–25/mo)
- 🔴 **Expensive / paywalled** — confirmed paid-only or manual-collection cost
- ⚠️ **No clean source** — needs outreach, scraping, or heavy custom build

## Section 1 — Index

| Metric | Status | Notes |
| --- | --- | --- |
| 7D/30D fees + growth | ✅ | Live; growth precomputed by DefiLlama |
| 7D/30D spot volume + growth | ✅/🟢 | 30D live; 7D + growth one wiring pass |
| 7D/30D **derivatives** volume + growth | 🔴 | DefiLlama aggregate returns **HTTP 402 (paid tier)** — confirmed live 2026-06-10. Free path: Hyperliquid/Jupiter native APIs (🟢 per-protocol) |
| 7D/30D active users + growth | 🟡 | Dune, dedup baked into SQL; DefiLlama's version is paid-API |
| TVL + 7D growth | ✅ | Live |
| 30D TVL growth | 🟢 | Computable once 30 days of our snapshots accrue (started 06-10) |
| Buybacks (30D/total, tokens + value) | 🟡 | Dune per-protocol buyback wallets; coverage will be uneven. Holders-revenue proxy ✅ already live |
| Token performance 1D/7D/30D/1Y | ✅ | Live via CoinGecko |
| Token performance YTD | 🟢 | One extra CoinGecko call per token |

## Sections 2 & 3 — Spot / Derivatives

| Metric | Spot | Derivatives | Notes |
| --- | --- | --- | --- |
| Daily + cumulative fees (charts) | 🟢 | 🟢 | Per-protocol fee history is free (`totalDataChart`); cumulative = running sum |
| Fee market share | 🟢 | 🟢 | Free fees overview works for both |
| Daily + cumulative volume (charts) | 🟢 | 🔴→🟢 | Spot free; derivatives aggregate paywalled (402) — per-protocol via Hyperliquid native API |
| Volume market share | ✅ | 🔴 | Spot 30D share live; derivatives share needs the paid aggregate (no free denominator) |
| Daily active users / total users | 🟡 | 🟡 | Dune |
| 1D/7D/30D fee + volume tables | ✅/🟢 | partial | Fees fine both; derivatives volume per-protocol only |

## Section 4 — Lending

| Metric | Status | Notes |
| --- | --- | --- |
| TVL chart/current/growth | ✅ | Live |
| Daily/cumulative fees + share | 🟢 | Free fee history |
| Borrow volume (outstanding) | ✅ | Live — defined as current stock per decision |
| Daily **new-borrow flow** + share | 🟡 | Dune borrow events |

## Section 5 — Asset Management

| Metric | Status | Notes |
| --- | --- | --- |
| EtherFi card users + spend | 🟡 | Official `ether_fi/etherfi-cash` Dune dashboard — fork + schedule |
| EtherFi eETH yield paid | 🟡 | Dune |
| Ethena USDe/sUSDe holders | 🟡 | Dune (no free REST source; Etherscan holder counts are paywalled) |
| sUSDe yield over time | ✅/🟢 | Current APY live; history one call (DefiLlama yields chart) |
| sUSDe yield paid (cumulative) | 🟡 | Dune (entropy_advisors / hildobby dashboards) |
| Falcon USDf market cap | ✅ | Live |
| Falcon vault deposits | ✅ | Live (protocol TVL) |

## Section 6 — Tokenization / RWA

| Metric | Status | Notes |
| --- | --- | --- |
| Ondo tokenized mcap **by category** | ⚠️ | rwa.xyz is canonical, no self-serve API (CSV downloads or email data@rwa.xyz). Headline numbers ✅ live; categories deferred per decision |
| Ondo tokenized stock volume + holders | 🟡 | Dune (Ondo GM dashboards) |
| Centrifuge mcap by category + holders | 🟢/🟡 | Centrifuge native GraphQL verified live; holders via Dune |
| Maple syrup mcaps | 🟢 | DefiLlama stablecoins or Maple GraphQL (verified live) |
| Maple syrup yield paid | 🟡 | Dune or Maple GraphQL `interestEarned` |

## Section 7 — Infra

| Metric | Status | Notes |
| --- | --- | --- |
| LayerZero messages / volume / users | 🟡 | Dune decoded tables; official Scan API is message-level (would mean paginating millions of rows) |
| Canton burned tokens + active users | ⚠️ | Permissioned chain: no Dune/DefiLlama. Splice Scan API is free but a heavy custom build; The Tie dashboard has no API. **Budget the most build time here, or defer** |

## Section 8 — AI (Virtuals)

| Metric | Status | Notes |
| --- | --- | --- |
| Daily volume / users / fees | 🟡 | Official Virtuals Dune account + community dashboards |
| Total aGDP | 🟡 | hashed_official ACP dashboard |
| Daily new agents / total agents | 🟡 | Dune launchpad dashboard; `api.virtuals.io` is an undocumented fallback |
| Funds raised for builders | 🔴 | Announcement/manual tracking, not dashboard data |

## Section 9 — Token Value Accrual Scorecard

| Input | Status | Notes |
| --- | --- | --- |
| Holders revenue | ✅ | Live (30D) |
| Revenue vs fees split | ✅ | Live |
| Buyback specifics | 🟡 | Section 1 Dune queries |
| P/F, P/S ratios | 🟢 | Computable from live mcap + fees |

## Bottom Line

- **Live today ($0):** ~40% of the outline — all Index basics, spot tables/share, lending, stablecoin products, token performance, scorecard inputs.
- **Free wiring away (🟢):** daily/cumulative chart series, fee shares, 1D tables, YTD — no new accounts.
- **One Dune setup away (🟡):** every users metric, buybacks, EtherFi/Ethena/Maple/LayerZero/Virtuals specifics — the single highest-leverage next step (~15 min of forking queries, ~$0–25/mo).
- **Genuinely expensive or hard (🔴/⚠️):** derivatives aggregates (DefiLlama paid API — worth asking if John's plan covers it), Ondo category breakdowns (rwa.xyz outreach), Canton (custom build), Virtuals fundraising (manual). Recommend: paid/awkward items go to Pro or get deferred, per the existing rule.
