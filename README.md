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

### [arch-hexagonal-postgresql-fast](packages/arch-hexagonal-postgresql-fast)

> **Event-Driven Hexagonal Payment Service** — production-ready payment processing

**Technologies:** FastAPI, PostgreSQL, RabbitMQ, Redis

**Demonstrates:**
- Hexagonal Architecture (Ports & Adapters pattern)
- Transactional Outbox — guaranteed event delivery
- Idempotency Keys via Redis — prevents duplicate payments
- Provider Abstraction — easily swap Stripe/PayPal/Adyen
- Event-Driven — publishes lifecycle events to RabbitMQ
- Domain-Driven Design with Value Objects and Entities

**Suitable for:** Payment systems, multi-tenant platforms, regulated domains (finance)

---

## 🚀 Quick Start

```bash
git clone --recursive https://github.com/pavel-lezhenin/python-templates.git
cd python-templates
pip install -e ".[dev]"
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
make new NAME=package-name DESC="description"  # Create new package
```

**Windows:** Use `python -m <tool>` instead of `make`

## ➕ Add New Package

```bash
make new NAME=package-name DESC="Package description"
make new-github NAME=package-name DESC="Package description"  # With GitHub repo
```

## 📋 Code Standards

- Python 3.14+, strict typing (mypy)
- 80% test coverage minimum
- Auto-formatting (ruff), security scanning (bandit, gitleaks)
- Pre-commit hooks, role-based review

## 📁 Structure

```
python-templates/
├── packages/                    # Templates (git submodules)
│   ├── fast-simple-crud/        # Simple CRUD + SSE + WebSocket
│   ├── arch-layer-prod-mongo-fast/  # Layered architecture
│   └── arch-hexagonal-postgresql-fast/  # Hexagonal + Event-Driven
├── shared/                      # Shared code
├── scripts/                     # Utilities
│   ├── create_package.py        # Create new package
│   ├── check_branch.py          # Branch protection hook
│   └── role_review.py           # Pre-commit validation
└── ...
```

## 🔗 Usage

```bash
# Standalone package
pip install git+https://github.com/pavel-lezhenin/<package-name>.git

# Monorepo
git clone --recursive https://github.com/pavel-lezhenin/python-templates.git
```
