# Free Dashboard Production Ready

## Objective

Make the Machines & Money free dashboard production-ready as a public audience-growth asset, while keeping it separate from the broader/pro dashboard.

## Original Request

Create a goal to autonomously work toward getting the Machines & Money free dashboard production-ready.

## Intake Summary

- Input shape: `existing_plan`
- Audience: Machines & Money public readers, social visitors, Ian, and newsletter prospects
- Authority: `requested`
- Proof type: `demo`
- Completion proof: a live or locally served `docs/dashboard/free.html` walkthrough shows the free dashboard is public-ready, source-caveated, mobile-readable, subscriber-oriented, and separate from `docs/dashboard/prototype.html`.
- Goal oracle: local/browser walkthrough plus file diff and verification receipts proving the free dashboard meets the production plan without overwriting the pro prototype.
- Likely misfire: GoalBuddy could spend effort on planning, the pro prototype, or decorative polish while failing to produce a public-ready free dashboard with real caveats, refresh workflow, CTA, and QA proof.
- Blind spots considered: hosting permanence, analytics, source confidence, sparse usage coverage, mobile readability, social-sharing loop, refresh cadence, and the free/pro boundary.
- Existing plan facts: use `docs/dashboard/free-dashboard-production-plan.md`; keep `docs/dashboard/free.html` separate from `docs/dashboard/prototype.html`; use Ian's clarified `hl.eco` preferences; incorporate the Dune-style category outline; keep the Beehiiv CTA; preserve source caveats.

## Goal Oracle

The oracle for this goal is:

`A verified local or hosted walkthrough of docs/dashboard/free.html shows: the first screen explains the public value; category/timeframe/chart interactions work; source and freshness caveats are visible; newsletter CTA works; mobile layout is readable; docs/dashboard/prototype.html remains untouched; and a final Judge/PM audit records full_outcome_complete: true against the production plan.`

The PM must keep comparing task receipts to this oracle. Planning, discovery, a passing tiny slice, or a clean-looking board is not enough. The goal finishes only when a final Judge/PM audit maps receipts and verification back to this oracle and records `full_outcome_complete: true`.

## Goal Kind

`existing_plan`

## Current Tranche

Use the existing production plan as the source of truth, then complete successive safe verified slices until the free dashboard is ready for public review and launch preparation. Start with evidence mapping and gap assessment, then implement the largest safe UI/data/documentation slice available, verify it, and continue until the final audit proves the plan's launch-readiness criteria.

## Non-Negotiable Constraints

- Keep the free dashboard separate from the broader/pro dashboard.
- Do not overwrite or repurpose `docs/dashboard/prototype.html`.
- Preserve Git/worktree safety and explain state in plain English.
- Treat source freshness, confidence, and caveats as product requirements, not cleanup.
- Keep public copy honest about sparse usage coverage and source limitations.
- Keep the Beehiiv newsletter CTA wired to `https://machinesandmoney.beehiiv.com` unless a better approved destination exists.
- Do not require paid data subscriptions for the free-dashboard production tranche.

## Stop Rule

Stop only when a final audit proves the full original outcome is complete.

Do not stop after planning, discovery, or Judge selection if a safe Worker task can be activated.

Do not stop after a single verified Worker package when the broader owner outcome still has safe local follow-up work. Advance the board to the next highest-leverage safe Worker package and continue unless a phase, risk, rejected-verification, ambiguity, or final-completion review is due.

Do not create one Worker/Judge pair per repeated card, chart, source row, or copy tweak. Put repeated same-shape work into one Worker package and review the package as a whole.

Do not stop because a slice needs owner input, credentials, production access, destructive operations, or policy decisions. Mark that exact slice blocked with a receipt, create the smallest safe follow-up or workaround task, and continue all local, non-destructive work that can still move the goal toward the full outcome.

## Slice Sizing

Safe means bounded, explicit, verified, and reversible. It does not mean tiny.

A good task is the largest safe useful slice.

Small is not the goal. Useful is the goal.

A Worker should finish the whole assigned slice. A Judge should judge the whole assigned slice. A PM should reorient the board when tasks are safe but not moving the outcome.

Tiny tasks are allowed when the failure is isolated, the risk is high, the scope is unknown, or the tiny task unlocks a larger slice. Tiny tasks are bad when they keep happening, do not change behavior, only add wrappers/contracts/proof files, or avoid the real milestone.

## Canonical Board

Machine truth lives at:

`docs/goals/free-dashboard-production-ready/state.yaml`

If this charter and `state.yaml` disagree, `state.yaml` wins for task status, active task, receipts, verification freshness, and completion truth.

## Run Command

```text
/goal Follow docs/goals/free-dashboard-production-ready/goal.md.
```

## PM Loop

On every `/goal` continuation:

1. Read this charter.
2. Read `state.yaml`.
3. Run the bundled GoalBuddy update checker when available and mention a newer version without blocking.
4. Re-check the intake: original request, input shape, authority, proof, blind spots, existing plan facts, and likely misfire.
5. Work only on the active board task.
6. Assign Scout, Judge, Worker, or PM according to the task.
7. Write a compact task receipt.
8. Update the board.
9. If safe local work remains, choose the next largest reversible Worker package and continue unless blocked.
10. Review at phase, risk, rejected-verification, ambiguity, or final-completion boundaries; do not review every small Worker by habit.
11. Finish only with a Judge/PM audit receipt that maps receipts and verification back to the original user outcome and records `full_outcome_complete: true`.
