# Path Conventions

Machines & Money uses a two-computer setup.

## Standard Paths

MacBook Pro, where Codex edits this repo:

```text
/Users/mbaggetta/my-project - MBP/machines-money
```

GitHub, the shared source of truth:

```text
https://github.com/immeasurablematt/machines-money
```

Mattmini, where Paperclip agents should inspect or edit this repo:

```text
/Users/matthewbaggetta/Projects/machines-money
```

## Rule

Do not use iCloud Drive, network-mounted MacBook folders, Paperclip runtime folders, or agent scratch folders as the durable repo location.

Use GitHub to sync between machines:

1. Codex changes code on the MacBook.
2. Changes are pushed to GitHub.
3. Paperclip agents pull or clone the repo on `mattmini`.
4. Paperclip project workspaces point to the `mattmini` path.

## Why

This keeps runtime state, scratch work, and project source code separate:

- `~/.paperclip` is Paperclip runtime state.
- `~/.paperclip/workspace` is agent scratch space.
- `/Users/matthewbaggetta/Projects/tools` is for Paperclip, Hermes, and other tool source repos.
- `/Users/matthewbaggetta/Projects/<repo-name>` is for normal working project repos.
