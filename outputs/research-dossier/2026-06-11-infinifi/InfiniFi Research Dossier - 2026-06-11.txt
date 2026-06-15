# InfiniFi Research Dossier

*Machines & Money Friday Feature Research Brief*

Project: InfiniFi  
Token/ticker: iUSD / siUSD / liUSD position tokens; no separate governance token confirmed for this dossier  
X handle: https://x.com/infiniFi  
Website/app: https://infinifi.xyz/ and https://app.infinifi.xyz/  
Docs: https://docs.infinifi.xyz/  
Prepared for: Ian  
Research date: 2026-06-11

## Source Key

- **[S1] InfiniFi docs hub:** https://docs.infinifi.xyz/ - pulled 2026-06-11.
- **[S2] Deposit quickstart:** https://docs.infinifi.xyz/deposit-quickstart - pulled 2026-06-11.
- **[S3] Vaults docs:** https://docs.infinifi.xyz/vaults - pulled 2026-06-11.
- **[S4] Slashing mechanics:** https://docs.infinifi.xyz/slashing-mechanics - pulled 2026-06-11.
- **[S5] Contract addresses:** https://docs.infinifi.xyz/dev-docs/contracts - pulled 2026-06-11.
- **[S6] Changelog:** https://docs.infinifi.xyz/dev-docs/changelog - pulled 2026-06-11.
- **[S7] DefiLlama protocol API:** https://api.llama.fi/protocol/infinifi - pulled 2026-06-11.
- **[S8] DefiLlama fees API:** https://api.llama.fi/summary/fees/infinifi - pulled 2026-06-11.
- **[S9] DefiLlama stablecoins API:** https://stablecoins.llama.fi/stablecoins?includePrices=true - pulled 2026-06-11.
- **[S10] DefiLlama protocol page:** https://defillama.com/protocol/infinifi - reviewed 2026-06-11.
- **[S11] GitHub protocol repo:** https://github.com/InfiniFi-Labs/infinifi-protocol - pulled 2026-06-11.
- **[S12] Certora formal verification post:** https://www.certora.com/blog/ensuring-fair-redemptions-in-infinifi-with-formal-verification - published 2025-06-30.
- **[S13] Blockworks 0xResearch explainer:** https://blockworks.com/news/yield-protocol-infinifi-banking-onchain - published 2025-06-24; background only because it is older than 6 months.
- **[S14] InfiniFi X account API:** https://x.com/infiniFi - pulled 2026-06-11; 341 posts reviewed over the last 180 days.
- **[S15] Odyssey native siUSD positions X post:** https://x.com/infiniFi/status/2060438800501809568 - posted 2026-05-29.
- **[S16] Apyx yield integration X post:** https://x.com/infiniFi/status/2059673692481745314 - posted 2026-05-27.
- **[S17] Morpho/Merkl rewards X post:** https://x.com/infiniFi/status/2062616816489222265 - posted 2026-06-04.
- **[S18] Edge Podcast transcript:** https://www.youtube.com/watch?v=rc_Vz95Jcgw - transcript pulled 2026-06-11.

## Executive Summary

InfiniFi is an onchain yield and reserve-management protocol for stablecoin deposits. The simple version: users deposit USDC to mint iUSD, then either hold iUSD for redemption flexibility, stake it into siUSD for liquid yield, or lock it into liUSD positions for higher yield and first-loss exposure. The product pitch is "higher yields, no leverage," but the more useful explanation is that InfiniFi turns a bank-like duration mismatch into a transparent onchain system where users choose their liquidity/risk bucket. [S1][S2][S4]

The article-worthy angle is not just stablecoin APY. It is programmable fractional-reserve banking with visible liabilities, visible reserves, yield-source routing, and an explicit loss waterfall. Senior liquid users get lower yield and more protection; locked users accept first-loss risk and receive higher rewards. That makes InfiniFi a cleaner way to discuss the core question behind stablecoin yield: where does the yield come from, who absorbs losses first, and how clean is the exit? [S1][S3][S4][S13]

Current scale is meaningful but off its highs. DefiLlama showed about $77.9M TVL on 2026-06-11, up roughly 304% from 2025-06-12 but down about 55% over the prior 90 days. DefiLlama stablecoin data showed about $77.9M IUSD circulating at a $0.9989 price. DefiLlama fees data showed about $14.8K in 24h gross protocol revenue/fees, $101.6K over 7 days, and $454.3K over 30 days. [S7][S8][S9]

The product is actively expanding distribution. The last six months of X activity surfaced integrations and campaigns around Odyssey, EtherFi, Euler, Katana, Pendle, Morpho/Merkl, Apyx, Seamless, Curve/Frax, and LayerZero bridging. Treat these as current product/distribution signals, not final publication facts unless corroborated by app/docs or partner sources. [S14][S15][S16][S17]

## Ian's Four Questions

1. What does the project do?

InfiniFi accepts USDC deposits and issues iUSD receipt tokens. Users can stake iUSD into siUSD for liquid returns or lock iUSD into duration-specific liUSD positions for higher yield and governance/allocation rights. The protocol then allocates capital across liquid and illiquid yield sources such as Aave, Spark, Cap, f(x), Morpho, Sentora, Fasanara, Maple, New Silver, and other listed vaults. [S1][S2][S3]

2. Why is this important and unique?

InfiniFi is trying to make the risk-transfer logic of banking legible onchain. Traditional banks pool deposits and invest across liquid and illiquid assets, but users cannot easily see the asset-liability mismatch. InfiniFi exposes the buckets and loss waterfall: locked iUSD is the junior tranche and absorbs losses before senior siUSD/iUSD users. This is more specific than "yield aggregator" and more interesting than a simple stablecoin vault. [S3][S4][S13]

3. How can this help people?

For users, InfiniFi offers a way to choose between liquid stablecoin yield and higher-yield locked exposure. For DeFi apps and partners, it can function as yield infrastructure: users can hold or route siUSD/iUSD through other apps while InfiniFi manages the underlying yield stack. For researchers, it is a concrete case study in onchain credit, reserve transparency, duration matching, and how DeFi handles bank-run style risks without pretending they do not exist. [S1][S3][S4][S15]

4. How are we actively using it?

Lowest-risk active use is research-only first: open the app, inspect live net APY, review the vault/source mix, compare siUSD and lock APYs, inspect the contract addresses, and follow the deposit path without signing. A real test would require USDC on Ethereum mainnet plus ETH for gas, then depositing USDC to mint iUSD, staking for siUSD, or locking into liUSD. Codex did not connect a wallet or perform any transaction. [S2][S3][S5]

## Metrics And Sources

The formatted metrics table, source map, source ledger, raw API backups, X timeline backup, and video transcript backups are saved in the local companion folder:

`outputs/research-dossier/2026-06-11-infinifi/`

## Freshness Notes

- Core docs, deposit guide, vault docs, slashing docs, contracts, DefiLlama, stablecoin data, GitHub, and X were pulled on 2026-06-11. [S1]-[S11][S14]
- DefiLlama TVL and fees change continuously; use the pulled date in any article. [S7][S8]
- The website was behind Cloudflare from direct terminal fetch, so docs/app/search-index sources were used instead of raw homepage HTML. [S1][S2][S10]
- Current YouTube transcripts were pulled where available. Older founder interviews exist but were not used as primary sources because the dossier standard excludes audio/video older than 6 months. [S18]
- Blockworks is older than 6 months and should be used only as background framing, not current product truth. [S13]

## What The Project Does

InfiniFi has three user-facing position types. iUSD is the receipt token from depositing USDC. siUSD is the staked token for liquid yield and instant conversion back to iUSD. liUSD-xw is a locked position token that earns illiquid returns and governance/allocation rights over a chosen duration. [S1][S2][S5]

The mechanism is a yield allocation stack. InfiniFi routes protocol assets into a mix of liquid and illiquid vaults, while user liabilities are separated by liquidity preference. The docs list liquid sources including Aave USDC, Cap stcUSD, Spark sUSDC, and a Multi Farm, plus illiquid sources such as Cap stcUSD, f(x) fxSAVE, FalconX Institutional, Morpho infiniFi Ecosystem Vault, Sentora, sGHO, STRCx, Fasanara funds, Maple Institutional, and New Silver. [S3]

The core business question is whether InfiniFi can keep producing above-market stablecoin returns while keeping the senior tranche credible and the risk disclosures understandable. That is where the project becomes interesting for readers: the APY is the surface; the real story is how risk is allocated and disclosed. [S3][S4][S8]

## Differentiating Features

- Explicit tranche structure: siUSD is senior/liquid and Locked-iUSD is junior/first-loss. [S4]
- Onchain reserve and liability framing: users can inspect deposited assets, minted iUSD, vault composition, and contract addresses instead of trusting opaque banking reports. [S3][S5][S13]
- Multiple yield-source buckets: the vault page lists DeFi, tokenized credit, institutional lending, and RWA-style sources in the same allocation stack. [S3]
- Partner distribution strategy: recent X activity points to integrations with Odyssey, EtherFi, Euler, Katana, Pendle, Morpho/Merkl, and Apyx. [S14][S15][S16][S17]
- Formal verification/security posture: Certora described a redemption queue fairness issue, the fix, and post-fix verification; DefiLlama lists audits. [S7][S12]

## Metrics Readout

Protocol scale:

- DefiLlama TVL: about $77.9M as of 2026-06-11. [S7]
- TVL was up about 304% versus 2025-06-12, but down about 55% versus 90 days prior. [S7]
- IUSD circulating supply: about $77.9M as of 2026-06-11. [S9]
- IUSD price: about $0.9989 as of 2026-06-11. [S9]

Revenue/activity:

- DefiLlama gross protocol revenue/fees: about $14.8K over 24h, $101.6K over 7d, and $454.3K over 30d. [S8]
- DefiLlama methodology says fees include performance fees from profit events, safety-buffer movement, and final user yield or loss; protocol revenue is only performance fees. Use precise labels when publishing. [S8]
- DefiLlama search/index data showed 7 tracked yield pools and 7.38% average APY. [S10]

Distribution/social:

- X account: 41,694 followers as of 2026-06-11. [S14]
- X timeline reviewed: 341 account posts over the prior 180 days. [S14]
- Notable recent signals: Odyssey siUSD positions in-app, Apyx-issued yields integrated after Risk Council review, and Morpho/Merkl incentive campaigns. [S15][S16][S17]

## Current Activity And Announcements

InfiniFi's recent activity is mostly about distribution and yield-source expansion. The highest-signal posts in the six-month X pull included Apyx yield integration, Odyssey in-app siUSD strategy access, Euler collateral support for fixed-maturity InfiniFi positions, Katana/LayerZero bridging, Pendle pools, Morpho/Merkl reward programs, and Curve/Frax liquidity. [S14]-[S17]

The most important recent item for Ian is the Odyssey integration because it changes the user path: users can open Odyssey siUSD positions directly inside the InfiniFi app instead of treating Odyssey as an external leg. That supports the "yield infrastructure inside other apps" angle. [S15]

The Apyx post is also useful because it shows the protocol expanding beyond basic DeFi lending into dividend/preferred-equity-style yield sources after Risk Council review. That is compelling, but it should be verified against app/docs or partner materials before Ian cites it as a hard integration fact. [S16]

## Video / Transcript Takeaways

The current Edge Podcast transcript is useful for the broader narrative around private credit moving onchain. The relevant frame is that not every private-credit asset belongs onchain; the asset has to be compatible with liquidity expectations and transparent risk management. That maps directly to InfiniFi's core tension: users want liquid stablecoin UX, but some yield sources are not liquid on demand. [S18]

Older InfiniFi founder interviews and explainers exist, including videos about duration assets and prior TVL milestones, but they are older than the dossier freshness window and should not be used as current evidence. They can help Matthew or Ian understand the origin story, but the final article should lean on current docs, current metrics, and current integrations. 

## Yield Analysis

The best way to explain InfiniFi yield is not "magic higher APY." It is a duration and risk allocation engine:

1. Users deposit USDC and receive iUSD. [S2]
2. Users choose a liquidity/risk bucket: hold iUSD, stake into siUSD, or lock into liUSD. [S1][S2]
3. InfiniFi allocates assets across liquid and illiquid vaults. [S3]
4. Locked users absorb losses first and receive higher yield; senior users get more liquidity and more protection. [S4]

What needs verification before publication:

- Current live app APY for siUSD and each lock duration.
- Current allocation weights by vault/source, not just the list of possible vaults.
- Whether any listed institutional/RWA vault has current size, redemption queue, borrower concentration, or historical loss data available.
- Whether recent Apyx, Odyssey, EtherFi, Euler, Katana, Morpho, and Pendle integrations are all live in-app or partly announced/partner-side.

## How To Use The Platform

Lowest-risk path:

1. Open https://app.infinifi.xyz/ and review net APY, siUSD, iUSD, lock options, and vault/source pages before connecting a wallet. [S1][S2][S3]
2. Review docs for the deposit path and contract addresses. [S2][S5]
3. Compare the senior/liquid siUSD option against locked liUSD terms. [S1][S4]
4. If Ian wants a real test, use only a small amount of USDC on Ethereum mainnet, confirm gateway/contract addresses, and inspect the generated transaction before signing. [S2][S5]
5. Do not deposit until current app APY, redemption path, lock terms, and underlying vault allocation are understood. Codex did not connect a wallet. [S2][S4]

## Risk And Verification Notes

- Duration mismatch risk: InfiniFi intentionally routes capital across liquid and illiquid assets, so exit liquidity matters. [S3][S4]
- Junior tranche risk: Locked-iUSD absorbs realized losses before senior/liquid users; this is the source of higher yield and should not be hidden. [S4]
- Redemption queue/fairness risk: Certora found and described a high-severity queue-bypass issue that has since been fixed and re-verified. This is a positive security-process signal, but also shows the protocol's economic logic is complex. [S12]
- Metric label risk: DefiLlama "fees" include user yield/loss and safety-buffer movement under its methodology; do not casually call all of it protocol revenue. [S8]
- TVL trend risk: the protocol has grown sharply since early data, but TVL is materially below the 90-day prior level. The article should mention both facts rather than only the growth headline. [S7]
- Integration risk: X posts are strong activity signals, but partner integrations should be verified in the app or partner docs before being presented as live product facts. [S14]-[S17]

## Open Questions For Ian

- Is the article angle "stablecoin yield infrastructure" or "transparent onchain banking"?
- What live APY should be used for siUSD and each lock duration on publication day?
- What is the current vault allocation by source, and how much is DeFi lending versus institutional/RWA/private-credit exposure?
- How much junior tranche protection exists today relative to senior/liquid liabilities?
- Are Odyssey, Apyx, EtherFi, Euler, Katana, Pendle, Morpho/Merkl, and Curve/Frax integrations all live and usable from the current app?
- Does InfiniFi have a public dashboard for reserves, queue state, tranche composition, and historical yield by source?
- Which risk disclosure should Ian quote when explaining what happens in a loss event?

## Draft Article Angles

1. "Onchain Banking Without The Black Box": InfiniFi recreates bank-style maturity transformation, but makes reserves, liabilities, and the loss waterfall visible. [S1][S3][S4][S13]
2. "Stablecoin Yield Needs A Risk Stack": InfiniFi is a practical case study in matching user liquidity preferences with different yield sources and first-loss rules. [S3][S4][S8]
3. "Yield Infrastructure For DeFi Apps": Recent integrations suggest InfiniFi may become a yield back end that other apps route into, not just a destination app. [S14]-[S17]
4. "The APY Is Not The Story": The interesting part is not whether siUSD pays 6%, 8%, or 10%; it is whether users can understand the source of yield, the exit path, and who absorbs losses first. [S3][S4][S18]

## Quality Gate Before Delivery

- Every material claim above has a dated source link.
- Metrics include value, period/source, pulled date, and confidence in the companion CSV.
- Missing live app details are marked as open questions, not guessed.
- Current video/transcript material was searched and saved; older video was not used as primary evidence.
- Project-native docs and metrics were prioritized over social posts.
- X posts are treated as announcement/activity context unless corroborated elsewhere.
- Codex did not connect wallets, sign messages, trade, stake, deposit, or withdraw.
