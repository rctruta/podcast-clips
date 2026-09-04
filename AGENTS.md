# AGENTS.md — a map of the gates (deliberately short)

You are a delegate; the human owns this repository. This file documents what
the repo ENFORCES. It does not enforce anything itself — the hooks do.

Prose that an agent re-reads every turn is expensive and does not reliably
change behavior. So this file is minimal, and every rule below is backed by a
mechanism. **You do not need to memorize this: if you cross a boundary, a gate
stops you.**

## The gates (enforced)
- **Push a clean tree.** The `pre-push` hook refuses a dirty working tree and
  a red test suite. `git status` must be clean at end of turn — commit it or
  delete it; there is no third state.
- **Main is the truth.** `git pull` at the start of a file-modifying turn;
  `git add -A && git commit && git push` in the SAME turn as the change. Work
  on branches, open PRs; never commit to `main` directly.
- **Remote branch protection** (Require PR + Include administrators) is
  layer 2, applied once this repo has a GitHub remote — see README.

## The rules a hook can't enforce (on your honor — and watched)
- **No bypass.** Never `git push --no-verify`, `git commit --no-verify`, or
  `gh pr merge --admin` to route around a gate.
- **No agent attribution** in commit messages or PRs. The human owns the
  history.
- **Ask before adding a dependency.** `uv add <package>` only after flagging
  it — see CLAUDE.md.
