# Python Templates

> **Набор production-ready шаблонов и паттернов для разработки Python-приложений**

## 🎯 Назначение

Этот репозиторий — коллекция готовых к использованию шаблонов, демонстрирующих:

- **Архитектурные паттерны** — от простого CRUD до многослойной архитектуры
- **Современные технологии** — FastAPI, MongoDB, Redis, Elasticsearch, WebSocket, SSE
- **Best practices** — строгая типизация, 100% покрытие тестами, CI/CD, security checks
- **Готовые решения** — можно использовать как основу для новых проектов

## 📦 Доступные шаблоны

### [fast-simple-crud](packages/fast-simple-crud)

> **Простой FastAPI шаблон** — минимальный, но полноценный пример

**Технологии:** FastAPI, Pydantic, SSE, WebSocket

**Что демонстрирует:**
- REST API с полным CRUD
- Server-Sent Events (real-time обновления)
- WebSocket (двусторонняя связь)
- In-memory хранилище (легко заменить на БД)

**Подходит для:** MVP, микросервисов, обучения FastAPI

---

### [arch-layer-prod-mongo-fast](packages/arch-layer-prod-mongo-fast)

> **Production-ready слоистая архитектура** — полноценный enterprise-шаблон

**Технологии:** FastAPI, MongoDB (Beanie ODM), Redis, Elasticsearch

**Что демонстрирует:**
- Классическая 3-слойная архитектура (API → Services → Repositories)
- Кэширование с Redis (TTL, инвалидация)
- Полнотекстовый поиск с Elasticsearch
- Dependency Injection
- Docker Compose для локальной разработки

**Подходит для:** Production-приложений, систем с высокой нагрузкой

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

## 📋 Стандарты кода

- ✅ **Python 3.14** — последняя версия языка
- ✅ **Strict typing** — mypy в строгом режиме
- ✅ **100% test coverage** — обязательное покрытие тестами
- ✅ **Auto-formatting** — ruff (линтер + форматтер)
- ✅ **Security** — detect-secrets, gitleaks, bandit
- ✅ **Pre-commit hooks** — автоматические проверки при коммите
- ✅ **Role-based review** — проверка кода с разных ролей (dev, reviewer, architect)

## 📁 Структура

```
python-templates/
├── packages/                    # Шаблоны (git submodules)
│   ├── fast-simple-crud/        # Простой CRUD + SSE + WebSocket
│   └── arch-layer-prod-mongo-fast/  # Слоистая архитектура
├── shared/                      # Общий код
├── scripts/                     # Утилиты
│   ├── create_package.py        # Создание нового пакета
│   └── role_review.py           # Pre-commit проверка
└── ...
```

## 🔗 Использование

**Как отдельный пакет:**
```bash
pip install git+https://github.com/pavel-lezhenin/fast-simple-crud.git
```

**Как часть monorepo:**
```bash
git clone --recursive https://github.com/pavel-lezhenin/python-templates.git
```
