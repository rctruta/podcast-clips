# podcast-clips

Extracting Ramona's questions from long-form podcast/Lunch & Learn episodes.
See [BRIEF.md](BRIEF.md) for the project scope and method.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) (not pip/requirements.txt)
for dependency management. `uv.lock` pins exact versions for reproducible
installs.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # if you don't have uv yet
uv sync
```

## Running tests

```bash
make test
# or directly:
uv run pytest -q
```

## Layout

- `podcast_clips/` — the tested library: caption parsing/dedup (`captions.py`),
  speaker-tag turn splitting (`turns.py`), tier-1 question/praise rule detectors
  (`questions.py`, `praise.py`)
- `tests/` — pytest suite, including an integration test against a real saved
  caption file
- `scripts/` — thin CLI entry points (fetch dates, scan the channel) that
  import from `podcast_clips/` rather than duplicating logic
- `raw_captions/` — fetched `.vtt` files (gitignored, regenerable via `yt-dlp`)

## Adding a dependency

Ask first. Then: `uv add <package>` (or `uv add --dev <package>` for
dev-only tools like pytest).

## Guardrails

Rules of engagement for anyone (human or agent) working in this repo live in
[AGENTS.md](AGENTS.md) — enforced by git hooks, not just written down.

- The `pre-push` hook refuses a dirty working tree and a red test suite.
- **Fresh clone? Hooks do NOT clone.** Run this once per clone or the
  guardrails above are silently absent:
  ```bash
  git config core.hooksPath .githooks
  ```
- `main` is the source of truth: work on branches, open PRs; never commit to
  `main` directly. (Branch protection isn't enabled yet — this repo has no
  GitHub remote. See [AGENTS.md](AGENTS.md) for the plan once it does.)
