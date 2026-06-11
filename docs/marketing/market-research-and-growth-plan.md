# Machines & Money — Market Research & Growth Plan

Date: 2026-06-11
Status: working document. Supersedes the AI-generated market research draft (see "Corrections to the prior draft" at the bottom). Built from repo ground truth: `README.md`, `AGENTS.md`, `docs/dashboard/*`, `docs/goals/*`.

---

## 1. What we are actually marketing

Machines & Money is Ian's newsletter on the intersection of Web3 and global finance, published on Beehiiv (<https://machinesandmoney.beehiiv.com>), backed by A1 Research. It covers DeFi, tokenized assets, RWAs, asset management, yield, derivatives, and AI x finance — making complex topics useful without stripping out the research.

The marketable asset inventory today (this is what the prior draft missed):

| Asset | Status | Growth role |
| --- | --- | --- |
| **Newsletter** (Beehiiv) | Live, recurring formats | Core product; the thing we grow |
| **Free DeFi20 metrics dashboard** | Live at <https://immeasurablematt.github.io/machines-money/>, daily auto-refresh, $0/mo data cost | Primary acquisition surface: public tool → email capture |
| **Welcome landing page** | Live (`/index.html`), embedded Beehiiv signup, live DeFi20 TVL / share-of-DeFi / %-of-Bitcoin chart | Conversion page; headline: "Know Where the Money Is Moving Before the Crowd Does" |
| **DeFi20 Index** | 20 confirmed projects (Uniswap, Aave, Pendle, Hyperliquid, Ethena, Sky, Ondo, Aerodrome, Morpho, Jupiter, Curve, Kamino, Euler, Centrifuge, Maple, EtherFi, Falcon, Canton, LayerZero, Virtuals), 308 data rows / 22 metric families | Proprietary editorial IP; the recurring hook for charts and social posts |
| **Pro dashboard** (value-accrual scorecard, project deep pages, growth & share trends) | Roadmap only; teaser cards live on welcome page | Future paid tier; snapshot history is accruing daily now to enable it |
| **News & Insights Scanner** | Paused 2026-06-10 | Future content-velocity tool, not a current channel |
| **Research Dossier methodology** | Documented standard, not yet automated | Quality moat; what makes the content trustworthy |

### Content formats (corrected)

- **DeFi In Five** — weekly context on important crypto/DeFi developments
- **Mid-Week Market Check** — market observations, DeFi20 tracking, yield opportunities
- **Friday Features** — high-level overviews of DeFi projects worth following
- **Truth Within Trends** — data-driven market/macro/geopolitical analysis
- **Building The Future** — accessible explanations of why DeFi matters

(The prior draft's "Yield Spotlight" series does not exist; cadence is multiple recurring formats, not a fixed "three weekly series".)

### Business sequencing (non-negotiable, from the repo)

**Grow the free subscriber base first. Introduce paid only once the audience is large and engaged enough.** The Pro dashboard roadmap has an explicit gate: free dashboard launched and growing, 30+ days of snapshot history, and Ian's confirmation of which pro sections matter. Any "launch paid tier" objective must respect this sequencing — see funnel math in §7.

---

## 2. Positioning

**Category:** practitioner-run onchain finance research, delivered as a newsletter + free live data tool.

**One-liner:** *Know where the money is moving before the crowd does.*

**Positioning statement:** For self-directed investors who want real onchain yield and adoption signals without institutional access or paid data terminals, Machines & Money is the research newsletter that publishes its own live DeFi20 index and dashboard — every number traceable to its source — so readers can see exactly what the analysis is built on, not just take its word for it.

**Three proof pillars (all already true and shippable):**

1. **Live, transparent data.** The DeFi20 dashboard refreshes daily, shows a source/caveat panel for every metric, and honestly flags gaps (e.g., paywalled derivatives aggregates). Competitors assert; we show receipts.
2. **Practitioner skin in the game.** Ian actively uses the projects he covers; the research methodology requires a hands-on test before writing.
3. **Independent, crypto-native research standards.** Source-priority rules, freshness rules (no >6-month-old video, stale docs treated as background), native-vs-parent metric separation. This is institutional discipline at retail accessibility.

**What we do NOT claim (honesty constraints from the repo):** no claims from sparse active-wallet data (only 3 DEX records today); aggregate derivatives volume is incomplete (DefiLlama paywalled it); altcoin-market history isn't free-tier. Marketing copy must not outrun the data — the honest-caveats posture *is* the brand.

---

## 3. Audience segments and jobs-to-be-done

| Segment | Job to be done | Entry asset | Conversion goal |
| --- | --- | --- | --- |
| **Self-directed DeFi yield seeker** (primary) | "Find real, verifiable yield without getting rugged or wading through shills" | Dashboard chart posts on X; stablecoin APY / yield metrics | Free subscriber → eventual Pro |
| **Crypto-curious TradFi/Web2 reader** | "Understand onchain finance with the rigor I'm used to, minus the jargon" | Welcome page chart (DeFi20 vs Bitcoin, share of DeFi); Building The Future / Truth Within Trends | Free subscriber |
| **Crypto-native power user / researcher** | "One place to compare DeFi20 fundamentals across fees, TVL, borrows, stablecoin supply, token performance" | The dashboard itself as a bookmarked tool | Free subscriber → Pro (deep pages, value-accrual scorecard) |
| **Institutional / family office** (A1 Research) | "Diligence-grade, independent digital-asset research and advisory" | LinkedIn (A1 Research), institutional framing of DeFi20 methodology | A1 advisory client lead |

The repo's stated audience for the dashboard: "crypto, TradFi, and Web2 readers who like interactive informative charts" — segment 2 is explicitly in scope, which most crypto newsletters ignore.

---

## 4. Competitive landscape (expanded)

The prior draft only compared newsletters. Machines & Money actually competes on two axes — **inbox attention** (newsletters) and **data utility** (dashboards/terminals) — and the strategy is to be the only player credibly doing both at the free tier.

### Newsletter competitors

| Competitor | Threat | How we win |
| --- | --- | --- |
| **Bankless** | High | They're builder/culture-first; we're data-first. Counter-program with charts and verifiable yield, not narratives. Don't compete on podcast/media scale. |
| **CoinDesk newsletters** | High (reach) | News commodity vs. research depth. We never race them on speed; we win on "what does it mean for my capital." |
| **Blockworks Daily / Research** | Medium-High | Closest analog on investor framing; their research is paywalled institutional. Our free dashboard undercuts their entry funnel. |
| **The Defiant** | Medium | Most direct topical overlap (DeFi-native, premium tier). Differentiate on the live index + portfolio practice vs. newsroom coverage. |
| **Milk Road** | Medium | The welcome page deliberately uses a Milk Road-style layout; they prove the chart-led daily format converts at scale. Watch their monetization moves. |
| Messari, Decrypt, Axios Crypto, Bloomberg Crypto | Low-Med | Episodic overlap; not worth dedicated counter-positioning. |

### Data-product substitutes (new category — this is where the dashboard lives)

| Product | Relationship | Implication |
| --- | --- | --- |
| **DefiLlama** | Source AND substitute | Free, comprehensive, but raw and curation-free. Our edge: the curated DeFi20 lens + editorial interpretation + caveat panels. Never out-DefiLlama DefiLlama; interpret it. Note: they are actively paywalling endpoints (derivatives moved to paid API) — a tailwind for curated free alternatives, and a supply risk to monitor. |
| **Token Terminal / Artemis** | Substitute for power users | Paid/institutional pricing. Our free tier is the wedge: "the fundamentals view without the terminal subscription." |
| **Dune** | Source + substitute | Requires query literacy. We pre-package the answers. |
| **hl.eco** | Design benchmark (Ian's stated reference) | Interactive charts, continuous updates, flexible timeframes, clean educational layout — the bar for dashboard UX. |

**Unfair advantage (sharpened):** no direct newsletter competitor publishes a free, daily-refreshed, source-annotated fundamentals dashboard for a named index of 20 protocols. Bankless/Defiant have opinions without live data surfaces; DefiLlama/Token Terminal have data without editorial curation or a newsletter relationship. The combination is the moat — and it costs $0/month to run, so it can't be price-pressured.

---

## 5. Funnel

```
X chart posts / LinkedIn / referrals / SEO
        │
        ▼
Welcome page (live DeFi20 chart + embedded Beehiiv signup)
        │                      │
        ▼                      ▼
Free subscriber          Dashboard bookmark (returning tool user)
        │                      │
        ▼                      ▼
Engaged reader  ◄── newsletter issues link back to dashboard charts
        │
        ▼
Pro tier (gated: dashboard growing + 30d history + Ian's section picks)
        │
        ▼ (institutional readers)
A1 Research advisory lead
```

The flywheel: every dashboard metric is a potential X post; every X post links to the welcome page; every newsletter issue embeds dashboard charts that pull subscribers back; returning dashboard users see the Pro teaser cards. The daily data refresh means the content well never runs dry.

---

## 6. Channel plan (mapped to real assets)

### X/Twitter (@machinesmoneyA1) — primary acquisition channel

- **Chart-of-the-day cadence:** the dashboard already computes 22 metric families daily. Systematize 3–5 posts/week from genuinely notable moves (7D fee growth leaders, stablecoin supply shifts, DeFi20 share-of-DeFi changes, %-of-Bitcoin milestones like the current 2.66%).
- Every chart post carries the welcome-page link with UTM tags (see §8 — not yet instrumented).
- Tag the projects featured (the DeFi20 are 20 large accounts with active communities; project retweets are free distribution). This was already anticipated in the launch-ready goal ("feeds social posts, project tagging, and newsletter CTAs").
- Build-in-public threads on the dashboard/index methodology — the transparency posture is itself content.

### Beehiiv-native growth

- **Recommendations network:** enable Beehiiv recommendations with adjacent non-competing newsletters; this is the cheapest subscriber source on the platform.
- **Boosts:** once baseline open/click rates are known, test paid Boosts against organic CPA.
- **Referral program:** Beehiiv's built-in referral tooling; reward ideas that cost nothing: early Pro access, a "DeFi20 methodology" deep-dive doc.
- Cross-promo swaps with similar-sized crypto newsletters (target: ones below the Bankless/Defiant tier).

### LinkedIn (A1 Research) — institutional lane

- Repurpose Truth Within Trends and DeFi20 index commentary into A1-branded posts targeting family offices and fund allocators. Goal here is advisory leads, not subscriber volume; keep the two motions separate.

### SEO / permanent surfaces

- The dashboard on GitHub Pages is indexable and updated daily — rare for static crypto content. Add per-page titles/meta/OG images so chart shares unfurl properly.
- Medium-term: move from `immeasurablematt.github.io/machines-money` to a branded domain (e.g., a subdomain of the eventual M&M domain). A permanent branded URL was already flagged as a launch criterion; it also consolidates SEO equity. **This is the single highest-leverage infrastructure fix for marketing.**

### Newsletter-internal

- Standing "from the dashboard" section in Mid-Week Market Check: 1–2 charts with the live link. Trains readers that the dashboard is where the numbers live, building the habit that justifies Pro.

---

## 7. Paid-tier math (reality check on the $150k EOY objective)

The prior draft carried an objective of $150k Pro revenue by EOY. Against the repo's free-first sequencing, here is what that requires:

| Pro price | Paying subs needed for $150k | Free list needed @ 5% conversion | @ 2.5% |
| --- | --- | --- | --- |
| $250/yr (~$21/mo) | 600 | 12,000 | 24,000 |
| $400/yr (~$33/mo, Bankless-tier) | 375 | 7,500 | 15,000 |
| $600/yr (research-tier) | 250 | 5,000 | 10,000 |

Crypto newsletters with a real paid-tool component convert at the higher end of the 2–5% band, but only with an engaged list. **Implication:** the binding constraint for the revenue goal is free-list size in Q3, not Pro feature scope. Every week of Pro feature work before ~5–10k free subscribers is mis-sequenced — which is exactly what the pro-dashboard sequencing rule already says. The current free list size is not recorded in this repo; pull it from Beehiiv and anchor these targets (action item).

Also note: 30+ days of snapshot history (a Pro data prerequisite) completes automatically around **mid-July 2026** given the 2026-06-10 launch sprint — the data gate and the audience gate can be worked in parallel without code effort.

---

## 8. Measurement plan (current gap: nearly nothing is instrumented)

The launch-ready goal explicitly left analytics as "the only remaining production decision." Until this is closed, growth work is flying blind.

Minimum viable instrumentation:

1. **UTM discipline:** every CTA to `machinesandmoney.beehiiv.com` tagged by surface (`utm_source=dashboard|welcome|x|linkedin`, `utm_campaign=` per chart/post). Beehiiv attributes signups to UTM automatically.
2. **Site analytics on the dashboard/welcome pages:** a privacy-light option (Plausible/GoatCounter — both have free/cheap tiers and fit the static-site setup) for pageviews, referrers, and CTA clickthrough.
3. **Beehiiv dashboard baseline:** record current subscriber count, open rate, CTR, and source mix in a dated doc so growth is measured against a known starting point.

KPI tree:

- **North star:** engaged free subscribers (opened ≥2 of last 4 issues).
- Acquisition: subs/week by source; dashboard → signup conversion rate; X post → welcome page CTR.
- Engagement: open rate, dashboard return visits, newsletter→dashboard clickthrough.
- Pro-readiness (later): teaser-card clicks, waitlist signups if one is added.

---

## 9. 90-day growth priorities (sequenced)

**Now (weeks 1–2): instrument and baseline**
1. Add UTM tags to all dashboard/welcome CTAs and stand up site analytics (§8). Smallest possible change, unblocks everything else.
2. Record Beehiiv baseline metrics.
3. Close the open Ian items blocking the welcome page (copy sign-off, bio) — `ian-changelog-2026-06-10.md` "What we need from you."

**Next (weeks 2–6): turn the dashboard into a distribution engine**
4. Start the chart-of-the-day X cadence with project tagging; track which metric families drive clicks.
5. Enable Beehiiv recommendations + set up 2–3 cross-promo swaps.
6. Add OG/meta tags to dashboard pages so shares unfurl with chart imagery.
7. Add the standing "from the dashboard" section to Mid-Week Market Check.

**Then (weeks 6–12): compound and prepare Pro**
8. Branded domain for the dashboard.
9. Beehiiv referral program with Pro early-access as the reward.
10. Pro waitlist on the teaser cards (measures willingness-to-pay before building).
11. Revisit the $150k math with real conversion data; pick Pro pricing from evidence, not the table in §7.
12. LinkedIn/A1 institutional cadence once retail motion is running itself.

---

## 10. Risks and open questions

- **Data supply risk:** DefiLlama is progressively paywalling endpoints (derivatives already moved, HTTP 402). The free stack mitigation (project-native APIs, e.g. Hyperliquid public API) is mapped in `free-api-source-map-2026-06-04.md` but not all wired. If the free stack degrades, both the product and the transparency positioning degrade with it.
- **Key-person dependency:** Ian's judgment is the quality bar; the welcome page founders section is still stubbed pending his bio and John's return.
- **Unanchored revenue goal:** the $150k EOY figure predates the repo's sequencing rule; treat it as a stretch target until baselined against actual list size (§7).
- **Brand split risk:** Machines & Money (retail) vs. A1 Research (institutional) need consistent but distinct voices; don't let institutional jargon leak into retail surfaces or vice versa.
- **Sparse-data honesty:** active-wallet coverage is 3 DEX records; never headline it in marketing until the Dune phase expands coverage (repo constraint).
- Open question for Ian: does John's DefiLlama plan include **API** access ($300/mo product)? It would unlock paywalled derivatives/users endpoints and change the §10 supply-risk picture.

---

## Corrections to the prior draft

For the record, the AI-generated draft this replaces had these factual problems:

1. Named a "Yield Spotlight" series that doesn't exist and described a "three-times-weekly" cadence; the real formats are the five listed in §1.
2. Omitted the free DeFi20 dashboard entirely — the live, deployed, primary acquisition asset.
3. Described the DeFi20 Index without its composition or the fact that it powers a public daily-refreshed product.
4. Claimed an "actively managed portfolio" with "live portfolio tracking" as the unfair advantage; the repo's actual differentiator is the transparent live *index/dashboard* plus hands-on project testing in the research process. Do not market a live portfolio surface that doesn't exist yet.
5. Compared only against newsletters, missing the data-product substitute axis (DefiLlama, Token Terminal, Dune) the dashboard actually competes on.
6. Carried the $150k paid-tier objective without reconciling it against the repo's explicit free-first sequencing or any funnel math.
7. Listed channels and objectives with no funnel, no instrumentation status, and no sequencing — none of it was runnable.
