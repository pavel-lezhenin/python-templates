# Python API Templates Monorepo

Monorepo with templates for various Python APIs.

## 🚀 Quick Start

**Unix/Linux/macOS:**
```bash
# Clone with submodules
git clone --recursive https://github.com/pavel-lezhenin/python-templates.git

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

**Windows (PowerShell/CMD):**
```powershell
# Clone with submodules
git clone --recursive https://github.com/pavel-lezhenin/python-templates.git

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

### Unix/Linux/macOS (bash)

```bash
make dev          # Install dev dependencies
make lint         # Run linter
make format       # Format code
make type         # Type checking
make test         # Run tests
make test-cov     # Tests with coverage
make security     # Security checks
make pre-commit   # Run all checks
make new NAME=package-name DESC="description"  # Create new package
```

### Windows PowerShell

```powershell
# Install dev dependencies
pip install -e ".[dev]" ; pre-commit install ; pre-commit install --hook-type commit-msg

# Run linter
python -m ruff check .

# Format code
python -m ruff format . ; python -m ruff check --fix .

# Type checking
python -m mypy packages shared

# Run tests
python -m pytest

# Tests with coverage
python -m pytest --cov --cov-report=html --cov-fail-under=100

# Security checks
python -m bandit -r packages shared ; python -m detect_secrets scan

# Run all pre-commit hooks
pre-commit run --all-files

# Create new package
python scripts/create_package.py "package-name" "description"
python scripts/create_package.py "package-name" "description" --github
```

### Windows CMD

```cmd
REM Install dev dependencies
pip install -e ".[dev]" && pre-commit install && pre-commit install --hook-type commit-msg

REM Run linter
python -m ruff check .

REM Format code
python -m ruff format . && python -m ruff check --fix .

REM Type checking
python -m mypy packages shared

REM Run tests
python -m pytest

REM Tests with coverage
python -m pytest --cov --cov-report=html --cov-fail-under=100

REM Security checks
python -m bandit -r packages shared && python -m detect_secrets scan

REM Run all pre-commit hooks
pre-commit run --all-files

REM Create new package
python scripts/create_package.py "package-name" "description"
python scripts/create_package.py "package-name" "description" --github
```

## ➕ Add New Package

**Unix/Linux/macOS:**
```bash
make new NAME=package-name DESC="Package description"
make new-github NAME=package-name DESC="Package description"  # With GitHub repo
```

**Windows (PowerShell/CMD):**
```powershell
python scripts/create_package.py "package-name" "Package description"
python scripts/create_package.py "package-name" "Package description" --github
```

## 📋 Standards

- ✅ Strict typing (mypy strict)
- ✅ 100% test coverage
- ✅ Auto-formatting (ruff)
- ✅ Secret detection (detect-secrets, gitleaks)
- ✅ Role-based review (dev, tester, reviewer, best_practice, architect)

## 📁 Structure

```
python-templates/
├── packages/           # Child repositories (git submodules)
├── shared/             # Shared code
├── scripts/            # Utilities
└── ...
```
