# Contributing

Thanks for your interest in contributing! This guide explains how to report issues and submit changes.

## Reporting Issues

- Search existing issues first to avoid duplicates.
- When possible, link the issue to the specific line of code (click the line number on GitHub → "Reference in new issue").
- Describe the problem, how to reproduce it, and the expected behavior.
- For security vulnerabilities, follow [SECURITY.md](SECURITY.md).

## Development Setup

```bash
git clone https://github.com/MariamRukhaia/mr6610-assignment1.git
cd mr6610-assignment1
poetry install --no-root
poetry run pre-commit install
```

## Submitting Pull Requests

1. Create a branch from `main` (direct pushes to `main` are blocked by branch protection).
2. Keep each PR focused on one fix or feature.
3. Reference related issues in the PR description (e.g. `Fixes #3`).
4. Make sure all checks below pass before requesting review.
5. PRs are merged with **Squash and merge** to keep history linear.

## Coding Style

- Format code with Ruff: `poetry run ruff format .`
- Linting must pass with zero errors: `poetry run ruff check .`
- Type checking must pass: `poetry run mypy main.py merkle_proof.py util.py`
- Security scanning must show no unresolved findings: `poetry run bandit -r . -x ./tests,./.venv`

## Testing Requirements

- New features and bug fixes must include tests in the `tests/` directory.
- All tests must pass: `poetry run pytest`
- Overall test coverage must stay at or above **75%**.
- Tests must not call the live Rekor API. Mock network calls instead.

## Secrets

A TruffleHog pre-commit hook scans every commit for secrets. Never commit credentials, tokens, or keys. If the hook blocks your commit, remove the secret instead of bypassing the hook.
