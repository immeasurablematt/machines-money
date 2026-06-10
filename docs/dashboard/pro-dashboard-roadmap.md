# Pro Dashboard Roadmap

Date: 2026-06-10
Status: roadmap only. No pro implementation until the free dashboard is launched and growing.

## Positioning

- Free dashboard (`docs/dashboard/free.html`, live data, public URL): answers **"what's interesting?"** Broad orientation, current rankings, honest caveats, social/newsletter loops.
- Pro dashboard (future paid/research product, prototype in `docs/dashboard/prototype.html`): answers **"why exactly?"** Deeper history, methodology, and per-project drilldowns for paying subscribers and Ian's own research.

The two surfaces stay in separate files and separate bundles. `prototype.html` is the design sandbox for pro and must never be overwritten by free-dashboard work.

## What Unlocks Pro Features

| Dependency | What it unlocks | Status |
| --- | --- | --- |
| 30+ days of retained daily snapshots | 7D/30D growth columns, line charts, market-share trends | Building automatically now via the daily refresh workflow |
| Dune API key (free tier first) | Active users/wallets across projects — Ian's top post-market-data priority | Needs key; queries to be scoped per project |
| CoinGecko Demo key | Token price/market cap/FDV/24H volume refresh | Free key, one-time setup |
| Project-native APIs (verified live: Aave, Hyperliquid, Pendle, Morpho, Kamino, Centrifuge, Maple, Ethena, LayerZero) | Per-project deep charts | Source map done (`free-api-source-map-2026-06-04.md`); wiring is pro work |
| Per-metric methodology notes | Source/methodology drilldowns subscribers can trust | Extend the existing source ledger model |

## Pro Feature Backlog (from Ian's DeFi20 Dune outline)

1. **Index section**: growth tables (7D/30D fees, volume, users, TVL growth), buyback tables, token performance table (1D/7D/30D/YTD/1Y).
2. **Sector sections (Spot, Derivatives, Lending)**: daily and cumulative fee/volume charts, fee and volume market-share charts, daily/total active users.
3. **Project deep pages**: EtherFi card spend and users; Ethena USDe/sUSDe holders, yield, reserves; Ondo/Centrifuge tokenized asset breakdowns; Maple syrup metrics; Falcon vaults; LayerZero messages/volume; Canton burns/users; Virtuals agents/aGDP.
4. **Token Value Accrual scorecard**: buybacks, fee capture, locked ratios — needs per-project source verification first (see `data-availability-comments.md` for the triage).
5. **Research workflow hooks**: route any chart into Research Dossier or scanner follow-up (per `mvp-spec.md`).

## Sequencing Rule

Ship and grow free first. Start pro work only when: (a) the free dashboard has a permanent URL and stable daily refreshes, (b) snapshot history supports growth math, and (c) Ian confirms which pro sections matter most for a paid tier.
