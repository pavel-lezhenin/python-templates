# Python Templates

> **Production-ready templates and patterns for Python application development**

## 🎯 Purpose

This repository is a collection of ready-to-use templates demonstrating:

- **Architecture patterns** — CRUD, Layered, Clean Architecture, Modular Monolith
- **Databases & Storage** — MongoDB, PostgreSQL, Redis, Elasticsearch
- **Cloud platforms** — AWS, Azure deployment ready
- **Best practices** — strict typing, 80%+ test coverage, CI/CD, security checks
- **Production solutions** — can be used as foundation for new projects

## 📦 Available Templates

### [fast-simple-crud](packages/fast-simple-crud)

> **Simple FastAPI template** — minimal but complete example

**Technologies:** FastAPI, Pydantic, SSE, WebSocket

**Demonstrates:**
- REST API with full CRUD
- Server-Sent Events (real-time updates)
- WebSocket (bidirectional communication)
- In-memory storage (easily replaceable with DB)

**Suitable for:** MVPs, microservices, FastAPI learning

---

### [arch-layer-prod-mongo-fast](packages/arch-layer-prod-mongo-fast)

> **Production-ready layered architecture** — complete enterprise template

**Technologies:** FastAPI, MongoDB (Beanie ODM), Redis, Elasticsearch

**Demonstrates:**
- Classic 3-tier architecture (API → Services → Repositories)
- Caching with Redis (TTL, invalidation)
- Full-text search with Elasticsearch
- Dependency Injection
- Docker Compose for local development

**Suitable for:** Production applications, high-load systems

---

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

## 📋 Code Standards

- ✅ **Python 3.14** — latest language version
- ✅ **Strict typing** — mypy in strict mode
- ✅ **80%+ test coverage** — mandatory coverage threshold
- ✅ **Auto-formatting** — ruff (linter + formatter)
- ✅ **Security** — detect-secrets, gitleaks, bandit
- ✅ **Pre-commit hooks** — automatic checks on commit
- ✅ **Role-based review** — code review from different roles (dev, reviewer, architect)

## 📁 Structure

```
python-templates/
├── packages/                    # Templates (git submodules)
│   ├── fast-simple-crud/        # Simple CRUD + SSE + WebSocket
│   └── arch-layer-prod-mongo-fast/  # Layered architecture
├── shared/                      # Shared code
├── scripts/                     # Utilities
│   ├── create_package.py        # Create new package
│   └── role_review.py           # Pre-commit validation
└── ...
```

## 🔗 Usage

**As standalone package:**
```bash
pip install git+https://github.com/pavel-lezhenin/fast-simple-crud.git
```

**As part of monorepo:**
```bash
git clone --recursive https://github.com/pavel-lezhenin/python-templates.git
```
