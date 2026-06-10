# Free Dashboard Launch Ready

## Objective

Make the Machines & Money free dashboard truly launch-ready as a public, recurring, newsletter-growth product, while keeping the pro dashboard as a separate later roadmap.

## Original Request

Create a GoalBuddy-style goal and loop for the next phase after "Free Dashboard Production Ready": take `docs/dashboard/free.html` from "production-ready tranche complete" to genuinely launch-ready as a public DeFi20 opportunity/signal tracker that feeds social posts, project tagging, and newsletter CTAs.

## Intake Summary

- Input shape: `existing_plan` (continues `docs/dashboard/free-dashboard-production-plan.md` and the finished `free-dashboard-production-ready` goal)
- Audience: crypto, TradFi, and Web2 readers who like interactive informative charts; Ian; newsletter prospects
- Authority: `requested`
- Proof type: `demo` plus file/workflow receipts
- Product direction: Ian likes hl.eco (interactive charts, continuous updates, flexible timeframes, clean educational category layout). Free answers "what's interesting?"; Pro later answers "why exactly, with deeper source/methodology/project drilldowns?"
- Ian artifact: "DeFi20 Dashboard — Free Tier (Dune)" Google Doc (sections: Index, Spot, Derivatives, Lending, Asset Mgmt, Tokenization/RWA, Infra, AI, Token Value Accrual scorecard). The free static dashboard aligns to this taxonomy; the full per-section daily chart catalog needs historical snapshots and Dune coverage, so most of it is pro/later scope.
- Likely misfire: polishing cosmetics, implementing pro-depth charts before launch basics, or declaring done without hosting/analytics/refresh receipts.

## Goal Oracle

Do not mark this goal complete until a final Judge/PM audit proves all of:

- `docs/dashboard/free.html` is production-ready for Ian/public review.
- `docs/dashboard/prototype.html` is untouched (baseline git blob `5db332f3a03c02916730eb58bd52de54b30efe3c`).
- Public copy is concise and audience-first.
- Source/freshness/caveats are visible and honest.
- Category, metric, timeframe, sector, project, table, source, share, and CTA interactions work.
- Mobile layout is readable.
- Refresh workflow is documented and testable.
- Static bundle can be built.
- Hosting/permanent URL path is clear.
- Analytics/tracking requirements are either implemented lightly or documented as the only remaining production decision.
- There is a clear free-vs-pro boundary and a pro roadmap.

The audit must map receipts to each item and record `full_outcome_complete: true`.

## Non-Negotiable Constraints

- Do not use paid data.
- Do not mix free dashboard and pro dashboard files. Never overwrite `docs/dashboard/prototype.html`.
- Do not silently make claims from sparse active-wallet data.
- Do not overbuild pro features before the free version is production-ready.
- Do not stop at a plan if safe implementation work is possible.
- Preserve Git/worktree safety and explain state in plain English for a non-developer owner.

## Slice Sizing

Prefer the largest safe useful verified slice. Tiny cosmetic tasks are a smell. Same-shape repeated work goes in one Worker package.

## Canonical Board

Machine truth lives at `docs/goals/free-dashboard-launch-ready/state.yaml`. If this charter and `state.yaml` disagree, `state.yaml` wins.

## Run Command

```text
/goal Follow docs/goals/free-dashboard-launch-ready/goal.md.
```

## PM Loop

1. Read this charter, then `state.yaml`.
2. Scout: audit current state against the production plan and Ian artifact.
3. Judge: choose the largest safe implementation slice.
4. Worker: implement the whole slice.
5. Judge/PM: verify against the goal oracle with commands and receipts.
6. Repeat until launch-ready or blocked by a real external dependency (hosting enablement, credentials, data source access, or an Ian decision). Blocked slices get a receipt and the loop continues on remaining safe work.

## Standard Verification Commands

- Node syntax check of inline JS in `docs/dashboard/free.html`.
- `python3 -m http.server` from `docs/dashboard` and confirm `free.html` + `generated-dashboard-data.js` return HTTP 200.
- Exercise chart/category/timeframe/sector/project/sort/share/CTA behavior (scripted DOM checks or browser walkthrough).
- `bash scripts/build_free_dashboard_bundle.sh`.
- `python3 scripts/refresh_dashboard_data.py` only when safe (it validates and restores last-known-good on failure); record environment network limits honestly.
- `git diff -- docs/dashboard/prototype.html` must be empty.
