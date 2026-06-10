# Ian Review Packet: Free DeFi20 Dashboard

Date: 2026-06-10

This is the launch-review packet for the free Machines & Money dashboard. Everything below can be checked in about ten minutes.

## What To Open

- Local: open `docs/dashboard/free.html` in a browser (or serve `docs/dashboard/` with `python3 -m http.server 8765` and open `http://127.0.0.1:8765/free.html`).
- Permanent URL (after one settings click, see "What Still Needs You"): `https://immeasurablematt.github.io/machines-money/`

## What The Dashboard Is

A public DeFi20 opportunity/signal tracker for crypto, TradFi, and Web2 readers who like interactive, informative charts. It answers "what's interesting?" — which platforms are gaining adoption, lagging, generating fees/revenue, attracting attention, and worth researching. The weekly interpretation lives in the newsletter; both CTAs point to `https://machinesandmoney.beehiiv.com`.

## What Changed For Launch

- Category map follows your Dune outline: Index, Spot, Derivatives, Lending, Asset Management, Tokenization/RWA, Infra, AI, Token Value Accrual. Cards filter the dashboard.
- Metric-first controls: pick a signal (TVL, Market Cap, FDV, Token Volume, Active Wallets, Fees, Revenue, DEX Volume), and only the timeframes that actually exist for it are clickable. Timeframes never silently switch your metric.
- Every selected metric shows its sources, confidence mix, period, and caveats right below the chart; the leaderboard carries a per-project confidence summary.
- Share button posts the current chart angle (it names the leading project for the selected metric) to X; copy-link supports TG/LinkedIn. Social cards now render with proper title/description meta tags.
- All key interactions are recorded in-page for analytics (nothing is sent anywhere yet — see decisions below).
- Data refresh and publishing are automated: a daily GitHub Actions job refreshes from free public sources (DefiLlama; CoinGecko/Dune optional with free keys), validates the data, keeps dated snapshots, restores last-known-good on failure, and a second job redeploys the public page whenever data changes.

## Honest Caveats On The Data

- 20 projects, 137 metric rows, all free sources. Snapshot date is always shown on the page.
- Active-wallet coverage is sparse (3 rows today). The page says so and treats usage as a lead to verify, not a verdict — please confirm you're comfortable with that framing.
- Fees/revenue definitions differ by source; the source panel keeps that visible.
- Growth columns and line charts need ~30 days of retained snapshots; the daily refresh is now building that history.

## What Is Free vs What Moves To Pro

Free: current rankings, 24H token volume, 7D usage where available, 30D fees/revenue/DEX volume, category map, source caveats, share + subscribe loops.

Pro (later, separate product — see `docs/dashboard/pro-dashboard-roadmap.md`): daily/cumulative line charts, market-share views, growth tables, buybacks, per-project deep charts (EtherFi card, Ethena holders, Ondo/Centrifuge/Maple, LayerZero/Canton/Virtuals), token value accrual scorecard, methodology drilldowns.

## What Still Needs You (the only open decisions)

1. **Enable hosting** (one click, Matt or Ian as repo owner): GitHub repo > Settings > Pages > Source: GitHub Actions. The permanent URL goes live on the next deploy.
2. **Analytics provider**: events are already captured on the page; pick a privacy-friendly provider (GoatCounter or Plausible are free/cheap) and we add one snippet. Not a launch blocker.
3. **Copy sign-off**: hero reads "See which DeFi projects are earning attention." — confirm tone.
4. Optional later: custom domain instead of the github.io URL; CoinGecko Demo key and Dune key as repo secrets to widen coverage.

## Verification Receipts

- Inline JS syntax check: pass.
- 16-step scripted browser walkthrough (categories, metrics, timeframes, sector/project/sort, project detail, source panel, share, CTAs, tracking, meta tags): pass.
- Static bundle build: pass. Both workflow files parse.
- `prototype.html` (the separate pro research prototype): byte-identical, untouched.
