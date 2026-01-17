# Task: Python Monorepo

## Goal
Create a Python API templates monorepo with autonomous child packages.

## Requirements

### Structure
- [x] Root repository with shared configs
- [x] Child packages as git submodules in `packages/`
- [x] Each package works autonomously when cloned separately
- [x] Template for creating new packages

### Code Quality
- [x] Strict typing (mypy strict)
- [x] Linting/formatting (ruff)
- [x] 100% test coverage (pytest-cov)
- [x] Security checks (detect-secrets, gitleaks, bandit)

### Automation
- [x] Pre-commit: auto-format, secrets, role-review
- [x] GitHub Actions: lint, type-check, test, security
- [x] Makefile with commands

### Copilot Rules
- [x] File `.github/copilot-instructions.md`
- [x] Limits: file <200 lines, function <30 lines, class <10 methods
- [x] Secrets only via env variables

### Role Review (pre-commit)
| Role | Checks |
|------|--------|
| dev | File/function size, no print() |
| tester | No assert in production |
| reviewer | Typing, no commented code, TODO format |
| best_practice | Secrets, bare except, eval/exec |
| architect | Class/method/import count |

## Created Files

```
pyton-templates/
├── .github/
│   ├── copilot-instructions.md
│   └── workflows/ci.yml
├── scripts/
│   └── role_review.py
├── packages/
│   ├── .gitkeep
│   └── api-template-example/    # Автономный пакет-пример
│       ├── .github/workflows/ci.yml
│       ├── .pre-commit-config.yaml
│       ├── .gitignore
│       ├── .secrets.baseline
│       ├── pyproject.toml
│       ├── README.md
│       ├── src/api_template_example/
│       │   ├── __init__.py
│       │   ├── py.typed
│       │   └── client.py
│       └── tests/
│           ├── conftest.py
│           └── test_client.py
├── shared/
│   └── __init__.py
├── .pre-commit-config.yaml
├── .gitignore
├── .gitmodules
├── .secrets.baseline
├── pyproject.toml
├── ruff.toml
├── mypy.ini
├── pytest.ini
├── Makefile
└── README.md
```

## Run Commands

```bash
pip install -e ".[dev]"
pre-commit install
pre-commit install --hook-type commit-msg
git add .
git commit -m "feat: initial monorepo setup"
```
