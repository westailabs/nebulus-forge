# Contributing to Nebulus Forge

1. Branch off `develop`: `git switch develop && git switch -c feat/<short-name>` (or `fix/`, `docs/`, `chore/`).
2. Keep changes small and focused. Use conventional commit messages (`feat:`, `fix:`, `docs:`, `chore:`).
3. Run the checks before you merge:

   ```bash
   ./scripts/run_tests.sh
   ```
   ```bash
   black --check src tests && flake8 src tests
   ```
4. Merge back into `develop` with `git merge --no-ff` (or `git merge --squash` for a single clean commit), then delete the branch.
5. `main` is the release branch. Do not commit to it directly.

Agent and tool instructions live in [AGENTS.md](AGENTS.md).
