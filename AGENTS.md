# Agent Instructions

The user is not a developer. Manage Git, branch, worktree, and cleanup details safely and explain blockers in plain English.

## Repo

- MacBook Codex folder: `/Users/mbaggetta/my-project - MBP/machines-money`
- Mattmini Paperclip agent folder: `/Users/matthewbaggetta/Projects/machines-money`
- GitHub repo: `https://github.com/immeasurablematt/machines-money`
- Default branch: `main`

Before switching branches, creating/removing worktrees, deleting branches, or recommending cleanup, always inspect:

```bash
git status -sb
git branch --show-current
git worktree list
```

Do not use destructive Git commands unless they have been verified safe. Preserve uncommitted or untracked work before cleanup.

## Paperclip

This repo is linked to the Paperclip project:

- Paperclip project: `Machines and Money`
- Paperclip company/prefix: `OPE`
- Project URL: `http://mattmini.tail59b5f4.ts.net:3100/OPE/projects/machines-and-money/issues`
- Project ID: `41bcfd8a-d264-4eb9-8a28-53dded1607f6`
- Primary Paperclip workspace: `/Users/matthewbaggetta/Projects/machines-money`
- Workspace repo URL: `https://github.com/immeasurablematt/machines-money`

Do not point Paperclip project workspaces at MacBook-only paths. Paperclip runs on `mattmini`, so agent-editable project repos should live under `/Users/matthewbaggetta/Projects/<repo-name>`.

Use Paperclip for multi-step work, agent handoffs, durable task tracking, review loops, and any work that should survive beyond one chat.

When a task maps to Paperclip:

1. Check the live Paperclip project before assuming current priorities.
2. Create or update an issue in the `Machines and Money` project.
3. Keep repo changes tied to the relevant issue when possible.
4. Leave a clear comment on the issue with what changed, what was verified, and what remains.

## Current Product Direction

The first active project is **Research Dossier**: a tool or workflow that helps Ian research project-focused Machines & Money articles faster without lowering quality.

The broader business goal is to grow the free Machines & Money subscriber base first, then introduce a paid subscription once the audience is large and engaged enough.

## Research Standards

For Research Dossier work, preserve Ian's research quality bar:

- Prefer current project websites/apps, Twitter/X, YouTube, dashboards, and recent announcements when docs are stale.
- Treat docs older than 6 months as background unless confirmed current.
- Do not rely on audio or video more than 6 months old.
- Track source dates and confidence.
- Always look for a practical way Ian can use the project directly.

Every dossier should help answer:

1. What does the project do?
2. Why is this important and unique?
3. How can this help people?
4. How are we actively using it?
