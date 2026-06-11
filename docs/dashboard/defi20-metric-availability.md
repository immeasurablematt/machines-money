# DeFi20 Dashboard — Metric Availability & Cost Map

Updated: 2026-06-11 (v2 — reflects the wired free tranche; adds estimated cost per metric).

**Legend:** ✅ Live now · 🟢 Free, buildable · 🟡 Dune · 🔴 Expensive/paywalled · ⚠️ No clean source

## Section 1 — Index

| Metric | Status | Est. cost | Notes |
| --- | --- | --- | --- |
| 24H/7D/30D fees + growth | ✅ | $0 | Live; growth precomputed by DefiLlama |
| 24H/7D/30D spot volume | ✅ | $0 | Live (DEX overview windows) |
| Derivatives volume + growth (aggregate) | 🔴 | $300/mo | DefiLlama paid API (confirmed HTTP 402). Hyperliquid 24H now ✅ via native API at $0 |
| 7D/30D active users + growth | 🟡 | $0–25/mo | Dune scheduled queries, dedup in SQL |
| TVL + 7D growth | ✅ | $0 | Live |
| 30D TVL growth | 🟢 | $0 | Auto-unlocks ~July 10 when our snapshots reach 30 days |
| Buybacks (30D/total) | 🟡 | $5–25/mo | Dune buyback-wallet queries; uneven coverage. Holders-revenue proxy ✅ $0 |
| Token performance 24H/7D/30D/1Y | ✅ | $0 | Live (CoinGecko) |
| Token performance YTD | 🟢 | $0 | ~21 extra CoinGecko calls/day, inside free quota |

## Sections 2 & 3 — Spot / Derivatives

| Metric | Spot | Derivatives | Est. cost | Notes |
| --- | --- | --- | --- | --- |
| Daily + cumulative fee charts | 🟢 | 🟢 | $0 | Free per-protocol fee history; front-end chart work |
| Fee market share | 🟢 | 🟢 | $0 | Free fees overview |
| Daily + cumulative volume charts | 🟢 | 🔴/🟢 | $0–300/mo | Spot free; derivatives history paywalled — Hyperliquid daily via native API $0 |
| Volume market share | ✅ | 🔴 | $0 / $300/mo | Spot live; derivatives needs paid denominator |
| 24H Perps Volume (Hyperliquid) | — | ✅ | $0 | **Live** via official Hyperliquid info API |
| Daily/total active users | 🟡 | 🟡 | $0–25/mo | Dune |
| 1D/7D/30D fee + volume tables | ✅ | partial | $0 | Live both for fees; volume live for spot |

## Section 4 — Lending

| Metric | Status | Est. cost | Notes |
| --- | --- | --- | --- |
| TVL chart/current/growth | ✅ | $0 | Live |
| Daily/cumulative fees + share | 🟢 | $0 | Free fee history; chart work |
| Borrow volume (outstanding) | ✅ | $0 | Live (stock definition) |
| Daily new-borrow flow + share | 🟡 | $0–25/mo | Dune borrow events |

## Section 5 — Asset Management

| Metric | Status | Est. cost | Notes |
| --- | --- | --- | --- |
| EtherFi card users + spend | 🟡 | $0–25/mo | Fork official ether.fi Cash Dune dashboard |
| EtherFi eETH yield paid | 🟡 | $0–25/mo | Dune |
| Ethena USDe/sUSDe holders | 🟡 | $0–25/mo | Dune; Etherscan holder counts are paywalled |
| sUSDe yield (current) | ✅ | $0 | Live |
| sUSDe yield history | 🟢 | $0 | One DefiLlama yields-chart call |
| sUSDe yield paid (cumulative) | 🟡 | $0–25/mo | Dune |
| Falcon USDf mcap + vault deposits | ✅ | $0 | Live |

## Section 6 — Tokenization / RWA

| Metric | Status | Est. cost | Notes |
| --- | --- | --- | --- |
| Ondo tokenized mcap by category | ⚠️ | quote via data@rwa.xyz | No self-serve API; headline numbers ✅ $0 |
| Ondo stock volume + holders | 🟡 | $0–25/mo | Dune (Ondo GM dashboards) |
| Centrifuge by category + holders | 🟢/🟡 | $0–25/mo | Native GraphQL verified live; holders via Dune |
| Maple syrupUSDC/syrupUSDT mcaps | ✅ | $0 | **Live** via DefiLlama stablecoins |
| Maple syrup yield paid | 🟡 | $0–25/mo | Dune or Maple GraphQL |

## Section 7 — Infra

| Metric | Status | Est. cost | Notes |
| --- | --- | --- | --- |
| LayerZero messages/volume/users | 🟡 | $0–25/mo | Dune decoded tables |
| Canton burns + active users | ⚠️ | days of build time | Splice Scan API is free but heavy custom parsing; The Tie has no API. Recommend defer |

## Section 8 — AI (Virtuals)

| Metric | Status | Est. cost | Notes |
| --- | --- | --- | --- |
| Daily volume/users/fees, aGDP, agents | 🟡 | $0–25/mo | Official + community Dune dashboards |
| Funds raised for builders | 🔴 | manual hours | Announcement tracking, not dashboard data |

## Section 9 — Token Value Accrual Scorecard

| Input | Status | Est. cost | Notes |
| --- | --- | --- | --- |
| Holders revenue + revenue/fees split | ✅ | $0 | Live |
| Buyback specifics | 🟡 | $5–25/mo | Section 1 Dune queries |
| P/F, P/S ratios | 🟢 | $0 | Computable from live data |

## Bottom Line (v2)

| Tranche | Coverage | Monthly cost |
| --- | --- | --- |
| ✅ Live today | ~50% of the outline (was 40% — 24H windows, syrup supplies, Hyperliquid perps just wired) | **$0** |
| 🟢 Free wiring remaining | chart series, fee shares, YTD, APY history, ratios; 30D TVL growth auto-arrives ~Jul 10 | **$0** |
| 🟡 Dune phase (one setup) | all users metrics, buybacks, EtherFi/Ethena/Maple/LayerZero/Virtuals | **$0–25/mo** |
| 🔴/⚠️ Expensive or hard | derivatives aggregates ($300/mo unless John's plan covers API), Ondo categories (rwa.xyz quote), Canton (custom build), Virtuals fundraising (manual) | case-by-case → Pro or defer |

**Realistic total to reach ~90% of Ian's outline: $0–25/month.**
