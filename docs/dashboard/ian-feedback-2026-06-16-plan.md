# Ian Feedback — 6.16.26 — Triage & Implementation Plan

Source: [Free dashboard feedback 6.16.26](https://docs.google.com/document/d/1K1TDJINe-tkfmRtuP6OgN2Z9lYxOIcF-xLumn3fGQfg/edit)
Master scope spec: [Free DeFi20 Dashboard doc](https://docs.google.com/document/d/1NDnOHWKucSQthxvpgIX41IoLdZ-is4tlprBV9IilGLA/edit)
Reference report (token utility / value capture): [DeFi20 Index Handbook](https://drive.google.com/file/d/1UgVQ3CVYAEBKpFJ5ud4NaF-ZSsv3QLmE/view)

This plan turns every item in Ian's review into an actionable task, grouped by type and
mapped to where the fix lives in this repo:

- **`config/records.toml`** — projects, sectors, DefiLlama/Dune slugs (data inputs)
- **`docs/dashboard/starter-token-map.csv`** — token → CoinGecko id, sector, token type
- **`scripts/refresh_dashboard_data.py`** — what metrics/windows get fetched and written
- **`docs/dashboard/free.html`** — what renders (Pulse view, tables, charts, sectors)

Annotate any line below to redirect. **Nothing here is built yet — this is the plan.**

---

## Build partition (verified against code, 6.16)

Every item below was traced through `refresh_dashboard_data.py` + `free.html`. Three buckets:

**✅ Buildable now — no Ian, no paid source:**
- P0 #1 Pulse cutoff (render), #2 Ethena ENA (token-type filter), #3 Jupiter→Spot (1-line CSV),
  #4 *aggregation* cases (Uniswap version sum), #6 token-volume label, #8 Pendle+Boros
  fees/volume (Boros free API confirmed 200).
- P1 windows for **Fees / Revenue / DEX Volume** — **already collected by the pipeline**
  (refresh_dashboard_data.py:523–535, 590–604); this is **render-only**, not pipeline work.
- P2 **fee market share** (+ 30D DEX/Derivatives share **already computed**, lines 606–673).
- P4 auto-scroll (confirmed free.html:2047–2049).

**🟡 Buildable now, but a judgment call first (still not Ian/source):**
- P0 #7 Value Capture — needs the scorecard *data* hand-encoded from the Handbook PDF.
- P0 #4 EtherFi/Jupiter fees — *definitional* (Cash-Liquid-only vs full project), not a bug.
- P0 #1 chart-vs-list — the `.slice(0,12)` caps the **bar chart** (arguably deliberate); the
  real fix is showing all 20 in the **list/table**.

**🔴 Pending — folds into Ian's source decision (NOT free-doable):**
- P0 #5 active wallets → "DefiLlama" — **verified: active addresses are NOT on the free
  DefiLlama API** (Pro-gated). Means DefiLlama Pro ($), keep Dune, or scrape. **Pending Ian.**
- P2 active-loan market share — `overview/active-loans` 500s; no clean free single-call.
- P1/P2 perps 7D + Jupiter perps volume — Dune (line 691 TODO).
- All P3 new-source projects — pending the scrape-or-pay decision.

**⚙️ Operational prereq:** P0 #1/#2/#3 only *render data* if `COINGECKO_DEMO_API_KEY` is set —
without it `append_market_rows` skips all market-cap/FDV/volume rows (lines 168–173).

---

## P0 — Correctness bugs (wrong/misleading numbers live right now)

These make the dashboard look untrustworthy. Fix first.

### 1. "DeFi20 Pulse" cuts off after top-12 projects
- **Symptom (Ian):** Market Cap, FDV, Token Volume, Fees, Revenue all stop at 12 projects
  in the Pulse view; the missing ones (EtherFi, LayerZero, Pendle, Falcon, Maple, Kamino,
  Centrifuge, Euler) only appear when you click their category.
- **Root cause:** `free.html:1516` hard-codes `.slice(0, 12)`.
- **Fix (decided):** **always show all 20** index projects in Pulse — no toggle. Confirm no
  other `.slice` truncates project lists.

### 2. Ethena Market Cap / FDV shows USDe instead of ENA
- **Symptom (Ian):** Market Cap and FDV display the USDe stablecoin, not the ENA token.
- **Root cause:** token map has two Ethena rows — `ENA → ethena` (governance_token) and
  `USDe → ethena-usde` (stablecoin_product). Market-cap/FDV aggregation is picking up the
  product row.
- **Fix:** Market Cap / FDV / token-performance views must use `governance_token` rows only.
  USDe stays as a product/supply metric, never as the project's market cap.

### 3. Jupiter listed under Derivatives
- **Symptom (Ian):** Jupiter shows under Derivatives in Market Cap, FDV, and Token Volume
  views; it shouldn't.
- **Root cause:** `starter-token-map.csv` tags Jupiter sector as "Spot and Derivatives".
- **Fix:** classify Jupiter as **Spot** for index/sector views. (Spec lists Jupiter under
  Spot, with perps volume tracked separately as a metric — not as a sector home.)

### 4. Wrong values vs DefiLlama (data-source audit)
Verify each against the cited source and fix the slug/window/aggregation feeding it:

| Metric | Project | Dashboard | Should be (Ian) | Source |
|---|---|---|---|---|
| TVL | Uniswap | off | 2.884B | [DefiLlama](https://defillama.com/protocol/uniswap) |
| TVL | Ondo | off | 3.79B | [rwa.xyz](https://app.rwa.xyz/platforms/ondo) |
| 30D Fees | Uniswap | wrong | $53.1M | [DefiLlama fees](https://defillama.com/fees) |
| 30D Fees | Jupiter | wrong | $16.4M | [DefiLlama fees](https://defillama.com/fees) |
| 30D Fees | EtherFi | wrong | $11.8M | [DefiLlama fees](https://defillama.com/fees) |
| 30D Revenue | Jupiter | wrong | $4.67M | [DefiLlama revenue](https://defillama.com/revenue) |
| 30D Revenue | EtherFi | wrong | $2.9M | [DefiLlama revenue](https://defillama.com/revenue) |
| Borrows | Jupiter | wrong | $957M | [DefiLlama active-loans](https://defillama.com/active-loans) |
| Active wallets | Uniswap | wrong | ~50k/wk | [DefiLlama](https://defillama.com/protocol/uniswap?activeAddresses=true&groupBy=weekly) |
| Active wallets | Aerodrome | wrong | ~27k/wk | [DefiLlama](https://defillama.com/protocol/aerodrome?activeAddresses=true&groupBy=weekly) |

- **Likely causes to check:** wrong/blended DefiLlama slug, version aggregation (e.g. Uniswap
  V2+V3+V4 fees), Dune active-wallet query (`refresh_dashboard_data.py` `append_dune_active_wallet_rows`)
  covering only DEX surface, and EtherFi pointing at `etherfi-cash-liquid` vs the full project.
- **Action:** add a source-vs-dashboard reconciliation note per project so these don't regress.

### 5. "Active wallets" data is questionable / where does it come from? 🔴 PENDING
- Ian asks where Uniswap/Aerodrome active wallets come from. Currently a Dune `dex.trades`
  distinct-`tx_from` query (`append_dune_active_wallet_rows`, only uniswap/curve/aerodrome, 7D).
- **Decision was:** switch to DefiLlama `activeAddresses`. **But verification shows the free
  DefiLlama API does not serve active addresses** — `api.llama.fi/protocol/uniswap` has no
  users field; that data is DefiLlama Pro (~$300+/mo). So "switch to DefiLlama" actually means
  one of: DefiLlama **Pro** (paid), **keep Dune** (current, but Ian questions the numbers), or
  **scrape** DefiLlama's site endpoint. **This re-opens the same source decision pending Ian —
  do not build until resolved.**

### 6. "Token volume" provenance
- Ian: "Where are these values coming from?" Currently CoinGecko `24H Token Volume`
  (`refresh_dashboard_data.py:234`). Add a visible source label so this is auditable.

### 7. Value capture view shows revenue (wrong data)
- **Symptom (Ian):** the Value Capture view brings up revenue data; it shouldn't.
- **Fix:** drive it from the token value-accrual scorecard at the bottom of the
  [DeFi20 Dune dashboard](https://dune.com/a1sash/defi20-index-full-sector-protocol-performance-dashboard),
  based on the "token utility slides" of the [Handbook report](https://drive.google.com/file/d/1UgVQ3CVYAEBKpFJ5ud4NaF-ZSsv3QLmE/view).

### 8. Pendle values may exclude Boros
- Ian: "I don't think any Pendle values include Boros." Spec says Pendle should include Boros
  fees/volume/users. Add Boros records (`boros` DefiLlama slug; users via Token Terminal) and
  blend into Pendle, clearly labelled.

---

## P1 — Missing time windows (data shown for only one period)

Spec wants 24H / 7D / 30D consistently. **Verification correction: most windows are already
fetched — the gap is the render, not the pipeline.**

| View | Pipeline status (verified) | Work needed |
|---|---|---|
| Fees | ✅ 24H/7D/30D already written (lines 523–535) | **render-only** — surface columns |
| Revenue | ✅ 24H/7D/30D already written (lines 523–535) | **render-only** |
| DEX Volume | ✅ 24H/7D/30D already written (lines 590–604) | **render-only** |
| Active wallets | 🔴 7D Dune only | blocked — see P0 #5 (source pending) |
| Perps Volume | 🟡 24H Hyperliquid native + rolling 30D only | 7D + Jupiter need Dune (pending) |

- **Where:** for the ✅ rows, just add columns in `free.html` (data is in `dashboardRows`).
  No new fetches needed.

---

## P2 — Missing market-share metrics

Ian: fees view (and others) don't show market share; spec wants it for **24H, 7D, 30D**.
**Verification: DEX + Derivatives 30D share already computed (lines 606–673).**

- ✅ **Fees market share** — addable now; the fees overview is already fetched (`fees_by_module`),
  just compute each record's share of the category total ([DefiLlama fees](https://defillama.com/fees)).
- ✅ **Spot/Perps volume market share (30D)** — **already computed** (`30D DEX Volume Share`,
  `30D Derivatives Volume Share`); just render them. 24H/7D share variants are addable from the
  same already-fetched `total24h`/`total7d` fields.
- 🔴 **Active-loan market share** — `overview/active-loans` returns 500 on the free API; no clean
  single-call. Doable only via per-protocol aggregation over our tracked set, or Pro. Defer.
- **Project-specific market share of DeFi20 aggregate** (Fees, Volume, Active loans) — fees/volume
  doable now from already-fetched data; active loans deferred with the above.

---

## P3 — Missing projects & metrics (spec gaps Ian called out)

Grouped by sector. Each is a new source + record + render.

### Asset Management
- **EtherFi card data** — card transactions, card volume, active users
  ([paymentscan](https://paymentscan.xyz/cards/etherfi)) + market share for those 3
  ([paymentscan](https://paymentscan.xyz/)).

### Tokenization / RWA
- **Ondo** — stocks & perps volume ([Ondo Global Markets](https://defillama.com/protocol/ondo-global-markets));
  Stablecoin/TVL must include **OUSG** ([rwa.xyz](https://app.rwa.xyz/assets/OUSG)) — Ondo TVL currently misses it.
- **Maple** — institutional active loans ([Dune](https://dune.com/maple-finance/maple-finance));
  syrupUSDC + syrupUSDT market cap, holders, active addresses ([rwa.xyz](https://app.rwa.xyz/platforms/maple)) — currently excluded from stablecoins.

### Infra
- **LayerZero** — messages and volume ([interoperability tracker](https://digital-asset-interoperability.com/)),
  users ([usage](https://digital-asset-interoperability.com/usage)).
- **Canton** — perps volume / burned tokens / active users ([Canton](https://canton.thetie.io/)).

### AI
- **Virtuals** (no fees/revenue showing today):
  - Funds raised for builders ([app.virtuals.io](https://app.virtuals.io/))
  - Total agent jobs, jobs completed, agent revenue, total aGDP ([virtuals.io](https://www.virtuals.io/))
  - Wallets holding agent tokens, DAW, DEX volume of agent tokens, trading revenue, total agents
    ([Dune](https://dune.com/virtual_protocol/virtual-protocol-on-base/4d3ae4ed-16c3-49ce-a390-e63ee19b817c))
  - Agent market cap ([app.virtuals.io](https://app.virtuals.io/))

### Stablecoins / yield-bearing products (Token Info section in spec)
- **Ethena** — USDe supply ([Ethena](https://app.ethena.fi/dashboards/transparency)); sUSDe supply,
  staking ratio, historical APY, yield paid ([Dune](https://dune.com/entropy_advisors/ethena-susde-usde-staking));
  asset holders incl. USDtb ([Token Terminal](https://tokenterminal.com/explorer/projects/ethena/metrics/asset-holders)).
- **Falcon** — USDf holders & active addresses ([rwa.xyz](https://app.rwa.xyz/assets/USDf));
  sUSDf supply & staking ratio ([Dune](https://dune.com/hashed_official/falcon-finance));
  sUSDf APY & yield paid ([StableWatch](https://www.stablewatch.io/analytics/assets/sUSDf-Falcon-Finance)).
- **Ondo** — USDY APY/yield ([StableWatch](https://www.stablewatch.io/analytics/assets/USDY-Ondo));
  OUSG APY/yield ([StableWatch](https://www.stablewatch.io/analytics/assets/OUSG-Ondo)).
- **Maple** — syrupUSDC APY/yield ([StableWatch](https://www.stablewatch.io/analytics/assets/syrupUSDC-Maple));
  syrupUSDT APY/yield ([StableWatch](https://www.stablewatch.io/analytics/assets/syrupUSDT-Maple)).

### Borrows — add coverage
- Add Centrifuge, Curve, EtherFi to borrows ([DefiLlama active-loans](https://defillama.com/active-loans)).

---

## P4 — UX

- **Sector card auto-scroll is annoying** — clicking a sector category auto-scrolls down to the
  chart. Make it not jump (or make scroll opt-in). `free.html` category-card click handler.

---

## Resolved decisions (annotated 6.16)

1. **Active wallets source** → **switch to DefiLlama `activeAddresses`** (folded into P0 #5).
2. **Pulse cap** → **always show all 20**, no toggle (folded into P0 #1).
3. **Scope of this pass** → **bundle everything into one change** — P0–P4 ship together, not
   staged PRs.
4. **Paid-source metrics** → **mark deferred / manual refresh**. The P3 items below with no
   free API are tagged `[deferred — manual/paid source]` and are out of scope for the
   automated pipeline this pass; capture them as a manual-refresh backlog, not a blocker.

### Paid/manual sources flagged deferred
- paymentscan — EtherFi card data
- rwa.xyz — Ondo OUSG, Maple syrup market cap/holders, Falcon USDf
- Dune (non-existing queries) — Maple institutional loans, Virtuals, Ethena/Falcon staking
- app.virtuals.io / virtuals.io — Virtuals funds raised, agent jobs, aGDP, agent market cap
- StableWatch — APY/yield for USDY, OUSG, syrupUSDC/USDT, sUSDf

Free-source P3 work (DefiLlama) stays in scope: Ondo Global Markets volume, OUSG into Ondo
TVL where DefiLlama exposes it, borrows coverage (Centrifuge/Curve/EtherFi), LayerZero where a
free endpoint exists, Pendle+Boros.

---

## Execution plan — split by what's unblocked

### Track A — buildable now (no Ian, no paid source) — one branch

1. **Data model** — `records.toml` + `starter-token-map.csv`: Jupiter token sector → `Spot`
   (fixes the `.includes()` double-match); restrict token-level market metrics to
   `token_type=governance_token` (Ethena ENA fix); add Boros record; add free-source borrows
   projects (Centrifuge/Curve/EtherFi).
2. **Pipeline** — `refresh_dashboard_data.py`: add **fee market share** (category total from the
   already-fetched fees overview); add 24H/7D **share variants** from already-fetched fields;
   fix Uniswap version-aggregation so project-level fees sum V2+V3+V4; add source labels.
   *(No active-wallet or perps changes here — those are pending.)*
3. **Render** — `free.html`: show all 20 in the Pulse **list/table** (the `.slice(0,12)` chart
   cap is a separate viz call); surface the **already-collected** 24H/7D Fees/Revenue/DEX-Volume
   columns and the **already-computed** DEX/Derivatives share; remove category auto-scroll (P4).
4. **Reconciliation** — verify each fixed P0 #4 value against its DefiLlama source before merge.

⚙️ **Prereq for the Pulse fixes to show data:** confirm `COINGECKO_DEMO_API_KEY` is set in the
refresh environment, else market-cap/FDV/volume rows never generate.

### Track B — blocked on Ian's source decision (do not start)

- P0 #5 active wallets (DefiLlama Pro / keep Dune / scrape)
- P2 active-loan market share (no free single-call)
- P1/P2 perps 7D + Jupiter perps volume (Dune)
- All P3 new-source projects (rwa.xyz / StableWatch / paymentscan / Dune / Virtuals)

### Track C — buildable now but needs a content/definition call first

- P0 #7 Value Capture scorecard (hand-encode from Handbook PDF)
- P0 #4 EtherFi/Jupiter fee *definitions* (Cash-Liquid-only vs full project)
