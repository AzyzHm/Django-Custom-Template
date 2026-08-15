# Contributing

Thanks for your interest in improving this template! Contributions of all sizes are welcome, from typo fixes to new features.

## Getting Started

1. Fork the repository and clone your fork.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-dev.txt
   ```
3. Copy `.env.example` to `.env` and fill in your local values.
4. Run migrations and the dev server to confirm everything works:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Branching & Commits

- Create a feature branch off `main`: `feature/short-description` or `fix/short-description`.
- Write clear, imperative commit messages (e.g. `Add pagination to item list endpoint`).
- Keep commits focused, avoid bundling unrelated changes together.

## Code Style

This project uses `ruff` for linting and `black` for formatting. Please run both before committing:

```bash
ruff check . --fix
black .
```

If you'd like these to run automatically, install the pre-commit hooks:

```bash
pre-commit install
```

## Tests

All new functionality should be covered by tests in the appropriate tier:

- **`tests/unit/`** for service-layer logic (mock the repository).
- **`tests/integration/`** for repository/ORM behavior.
- **`tests/e2e/`** for API endpoint behavior end to end.

Run the full suite before opening a pull request:

```bash
pytest
```

## Pull Requests

1. Ensure `ruff`, `black`, `mypy`, and `pytest` all pass locally.
2. Fill out the pull request template completely.
3. Link any related issues.
4. Be responsive to review feedback. small, iterative changes are easier to review than large rewrites.

## Reporting Bugs & Requesting Features

Please use the issue templates provided in `.github/ISSUE_TEMPLATE/` rather than opening blank issues, so we have the context needed to help.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).
