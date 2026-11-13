# AGENTS.md — Nebulus Forge

## Project overview

- **Forge** is an AI-native project scaffolder with a profile-driven pipeline (`forge new`).
- It is **not** an agent runtime. The runtime is [neo-harness](https://github.com/westailabs/neo-harness).
- Part of the West AI Labs / Nebulus ecosystem. Public repo: [westailabs/nebulus-forge](https://github.com/westailabs/nebulus-forge). MIT licensed.

## Setup and commands

Use the project virtualenv (`.venv`), never the global Python.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e . -r requirements-dev.txt   # install (editable) + dev tools
./scripts/run_tests.sh                     # test (or: pytest -q)
flake8 src tests --select=E9,F63,F7,F82   # lint (same gate as CI)
pre-commit run --all-files                 # all hooks

forge profiles list
forge new /tmp/demo -p base --no-interactive --neo off
forge update [path]
```

## Build, test, and lint

- `pytest` must be green before work is called done. Tests live in `tests/`; run a subset with `pytest tests/test_<name>.py -q`.
- CI: `.github/workflows/unittests.yml` (flake8 + pytest on Python 3.10–3.12) runs on pushes and PRs to `main` and `develop`.

## Code style

- Python 3.10+ (dev usually 3.12). flake8 (`.flake8`) gates syntax errors in CI. Black (88 cols) is configured in `pyproject.toml`, but the tree is not fully Black-formatted yet: format only files you touch, never the whole tree.
- Type hints on public functions, Google-style docstrings.
- Tests for any pipeline or profile change.

## Architecture (v2)

Profile-driven: **load → merge inheritance → render Jinja2 → apply → `.forge.lock`**.

| Module | Role |
|--------|------|
| `models.py` | Pydantic data models only; minimal logic |
| `profile_loader.py` | Reads `profile.toml` + `structure.toml`, resolves inheritance |
| `renderer.py` | Pure Jinja2 rendering, no I/O |
| `applier.py` | Writes files (CREATE / UPDATE / FORCE), respects the lock file |
| `pipeline.py` | Orchestrates the stages. **No hardcoded file trees** — profiles own structure |
| `wizard.py`, `workspace_wizard.py`, `defaults.py` | Interactive prompts and `--no-interactive` defaults |
| `hooks.py` | Optional `neo init-workspace` post-hook (`--neo`, `FORGE_NEO_CMD`) |
| `cli.py` | Typer entry point: `new`, `update`, `info`, `profiles`, `workspace` |

| Directory | Purpose |
|-----------|---------|
| `src/forge/` | CLI and pipeline |
| `profiles/` | Shipped profiles: **base**, **fullstack**, **monorepo** (+ templates) |
| `templates/workspace/` | `forge workspace` templates (not a `forge new` profile) |
| `tests/` | Pytest suite |
| `docs/` | User docs — start at [docs/README.md](docs/README.md) |

- Check `profiles/` before inventing a new scaffold shape. Profile authoring: [docs/creating-a-profile.md](docs/creating-a-profile.md).
- Do **not** document legacy `forge .` or removed profiles (`openclaw-agent`, standalone `workspace` as a `forge new` profile).
- Deeper rules: [AI_DIRECTIVES.md](AI_DIRECTIVES.md), [WORKFLOW.md](WORKFLOW.md), [CONTEXT.md](CONTEXT.md) (§5 is CLI truth).

## Git workflow

- Gitflow-lite: `develop` is integration, `main` is releases.
- Branch off `develop` with `feat/`, `fix/`, `docs/`, or `chore/`. Conventional commits.
- Merge back with `--no-ff` (or squash to one commit). Never commit straight to `main`.
- Keep feature branches local until Jason approves a push. Do not push, tag, or open a PR unless asked.

## Security and privacy

- Never commit secrets, tokens, or `.env` files. Name environment variables only; never print values.
- Never read vault files or `~/.config/neo4j-shared.env`.
- No proprietary employer data in this repo or in agent context.

## Agent boundaries

- Ask before installing packages globally, changing remotes, merging, pushing, or releasing.
- Small, focused diffs. Update or add tests for the code you change.
- Generated projects get their agent files from `profiles/base/templates/` — change those templates, not hand-edited output.
