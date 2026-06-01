# Machines Money

Tools and experiments for growing [Machines & Money](https://machinesandmoney.beehiiv.com), Ian's newsletter about the intersection of Web3 and global finance.

Machines & Money helps readers understand financial innovation across DeFi, tokenized assets, RWAs, asset management, yield opportunities, derivatives, AI, and related markets. The newsletter's job is to make complex crypto and finance topics useful without stripping out the important research.

The business goal is to grow the free subscriber base first, then introduce a paid subscription once the audience is large and engaged enough to support it.

## Purpose

This repository exists to help Ian research, evaluate, write, and distribute Machines & Money content faster without lowering the quality bar.

The tools here should support:

- Better research throughput
- More consistent article quality
- Faster production of recurring newsletter formats
- Clearer project evaluation
- Stronger subscriber acquisition and retention
- Future paid-subscription readiness

## Current Project

The first project is **Research Dossier**.

Research Dossier is intended to help Ian prepare project-focused articles in much less time without lowering the quality of the research. It is especially relevant for Friday Features and other issues that evaluate specific DeFi projects, yield opportunities, or onchain products.

The goal is not to replace Ian's judgment or writing. The goal is to automate the repetitive parts of project research: gathering source material, checking whether information is current, extracting metrics, identifying useful product actions, and organizing everything into a structured dossier that Ian can review and turn into a feature.

Future projects may support other parts of the newsletter operation, such as audience growth, content repurposing, paid subscription packaging, or research library management.

## News & Insights Scanner

The repo also includes an MVP **X List News & Insights Scanner** for broad feed triage across announcements, adoption stats, charts, and deep dives. It is separate from Research Dossier: most scanner items become mentions, saved reads, chart/stat candidates, project-watch notes, or theme-watch notes instead of single-project dossiers.

Run the sample scanner:

```bash
PYTHONPATH=src python3 -m news_insights_scanner \
  --ingestion manual \
  --input samples/news-insights-manual.json
```

See `docs/news-insights-scanner/spec.md` and `docs/news-insights-scanner/runbook.md` for the source spec and operating notes.

## Newsletter Context

Machines & Money currently includes several recurring content formats:

- **DeFi In Five**: weekly context on important crypto and DeFi developments
- **Mid-Week Market Check**: market observations, DeFi20 tracking, and yield opportunities
- **Friday Features**: high-level overviews of DeFi projects worth following
- **Truth Within Trends**: data-driven analysis of market, macro, geopolitical, and crypto-specific activity
- **Building The Future**: accessible explanations of why DeFi and financial innovation matter

Research Dossier starts with the project-focused workflow, but it should fit into the broader newsletter strategy: helping readers find useful opportunities, understand why they matter, and see how Ian is actually using them.

## Research Process

Each dossier should start with a **Source Map pass** before any synthesis or writing. The Source Map is a short evidence plan that lists likely sources, classifies them, and decides what is reliable enough to use.

The goal is to avoid writing from the first obvious source. For example, if a project is built by a larger protocol, the dossier must still search for project-native metrics and current project-specific video before falling back to parent-protocol context.

The Source Map should classify each source by:

- Source type: official site/app, docs, native metrics, video/transcript, X/social, blog/announcement, dashboard/API, contracts/GitHub/audits, parent context, third-party analysis
- Relationship: native, parent, or third-party
- Freshness/date
- What it can answer
- Confidence
- Whether it should be used in the dossier

### Main Sources

Written sources:

- Project documentation
- Project website or app
- Project Twitter/X account
- Project announcements and release notes

Audio and video sources:

- Project Twitter/X livestreams and videos
- YouTube interviews, explainers, or demos

Visual and metric sources:

- Project-native dashboards, APIs, app stats, and public data endpoints
- Project-native DefiLlama protocol pages
- Token Terminal, Artemis, or other protocol-specific analytics
- Dune dashboards
- DeFiLlama
- Blockworks dashboards
- Metrics pages linked from the project's website or app

Parent or ecosystem metrics:

- Parent-protocol TVL, fees, volume, or token data
- Ecosystem-wide dashboards
- Parent-company or parent-protocol docs

Parent metrics are useful context, but they must not be presented as project-native metrics.

### Source Priority

Use this order before writing:

1. Project-native metrics, app data, dashboards, APIs, and exact DefiLlama protocol pages.
2. Current founder/team videos, interviews, demos, podcasts, livestreams, and transcripts.
3. Current official site/app, docs, blog, release notes, and announcements.
4. X/Twitter posts and replies from the last 6 months.
5. Contracts, GitHub, audits, risk docs, and technical specs.
6. Parent-protocol metrics and ecosystem context.
7. Third-party analysis and media commentary.

### Hard Stop Before Drafting

Do not start the dossier narrative until these checks are complete:

- Search `defillama.com/protocol/<project-slug>` and obvious project-name variants.
- Search YouTube for the project name, founder/team names when known, demo, interview, podcast, and explainer.
- Pull full transcripts for useful current videos when available.
- Check the app/site/docs for native APIs, public data folders, dashboards, analytics pages, and metrics links.
- Separate project-native metrics from parent/ecosystem metrics in the Source Map and final tables.

### Freshness Rules

- If project documentation has not been updated in the past 6 months, prioritize the current website, app, Twitter/X account, YouTube, and recent announcements.
- Do not use audio or video content that is more than 6 months old.
- Treat old documentation as background context, not the current source of truth.

## Core Metrics

Each dossier should look for the most relevant activity and adoption signals.

General metrics:

- Platform activity
- Active users
- Transaction volume
- Fees or revenue generated
- Buybacks
- TVL or AUM

For yield projects:

- Yield-bearing asset activity
- Growth in users
- Growth in market cap
- Yield sources
- Evidence that yield sources are real and verifiable
- Yield consistency over time

## Differentiation

Each dossier should identify what makes the project meaningfully different.

Examples of differentiating features:

- f(x) Protocol's architecture
- Sky's Agent Network
- Altura's gold arbitrage strategy

The goal is to find the specific mechanism, product design, market angle, or strategy that makes the project worth writing about.

## Upcoming Releases

Each dossier should look for signs of upcoming releases, announcements, integrations, campaigns, or product changes.

Likely sources:

- Twitter/X posts and replies
- Discord or Telegram announcements, if available
- Blog posts
- Roadmaps
- Project team comments
- Direct messages to the project or relevant contacts, when needed

## Active Use

Each dossier should find a practical way for Ian to use or test the project.

Examples:

- Buy a yield-bearing asset
- Stake tokens
- Earn rewards
- Open a trade
- Try a new product flow
- Use the app enough to describe the user experience honestly

## Questions Every Dossier Must Answer

Each Research Dossier should give Ian enough material to answer:

1. What does the project do?
2. Why is this important and unique?
3. How can this help people?
4. How are we actively using it?

## Research Dossier Output

The first useful version of Research Dossier should produce a structured research brief for a single project or opportunity.

Expected output:

- Project summary
- Source list with dates
- Freshness notes
- Key metrics
- Yield analysis, if relevant
- Differentiating features
- Upcoming releases or announcements
- Suggested hands-on test
- Open questions
- Draft article angles

The product should help Ian get from "what should I write about this project?" to "I have a clear research base and article angle" faster.

## Status

This project is in initial planning.
