# Python API Templates Monorepo

Monorepo with templates for various Python APIs.

## 🚀 Quick Start

```bash
# Clone with submodules
git clone --recursive https://github.com/yourname/pyton-templates.git

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

## 📦 Install Single Package

```bash
pip install git+https://github.com/yourname/openai-template.git
```

## 🛠️ Commands

```bash
make dev          # Install dev dependencies
make lint         # Run linter
make format       # Format code
make type         # Type checking
make test         # Run tests
make test-cov     # Tests with coverage
make security     # Security checks
make pre-commit   # Run all checks
```

## ➕ Add New Package

```bash
make submodule-add URL=https://github.com/yourname/new-template.git NAME=new-template
```

## 📋 Standards

- ✅ Strict typing (mypy strict)
- ✅ 100% test coverage
- ✅ Auto-formatting (ruff)
- ✅ Secret detection (detect-secrets, gitleaks)
- ✅ Role-based review (dev, tester, reviewer, best_practice, architect)

## 📁 Structure

```
pyton-templates/
├── packages/           # Child repositories (git submodules)
├── shared/             # Shared code
├── scripts/            # Utilities
└── ...
```
