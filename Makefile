.PHONY: help install dev lint format type test test-cov security pre-commit clean

PYTHON := python
PIP := $(PYTHON) -m pip

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	$(PIP) install -e .

dev: ## Install development dependencies
	$(PIP) install -e ".[dev]"
	pre-commit install
	pre-commit install --hook-type commit-msg

lint: ## Run linter
	ruff check .

format: ## Format code
	ruff format .
	ruff check --fix .

type: ## Run type checker
	mypy packages shared

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov --cov-report=html --cov-fail-under=100

security: ## Run security checks
	bandit -r packages shared
	detect-secrets scan

pre-commit: ## Run all pre-commit hooks
	pre-commit run --all-files

clean: ## Clean cache files
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

submodule-add: ## Add submodule (URL=<url> NAME=<name>)
	git submodule add $(URL) packages/$(NAME)
	git submodule update --init --recursive

submodule-update: ## Update all submodules
	git submodule update --remote --merge

submodule-init: ## Initialize all submodules
	git submodule update --init --recursive

submodule-check: ## Check all submodules for uncommitted changes
	@echo "Checking submodules for uncommitted changes..."
	@git submodule foreach 'git status --short && test -z "$$(git status --short)" || (echo "❌ Uncommitted changes in $$name" && exit 1)'
	@echo "✅ All submodules are clean"

submodule-test: ## Run tests in all submodules
	@echo "Running tests in all submodules..."
	@git submodule foreach 'if [ -f pytest.ini ] || grep -q pytest pyproject.toml 2>/dev/null; then echo "Testing $$name..." && pytest; fi'

submodule-lint: ## Run linting in all submodules
	@echo "Running linting in all submodules..."
	@git submodule foreach 'if [ -f pyproject.toml ]; then echo "Linting $$name..." && ruff check .; fi'

# ===========================================
# Package creation
# ===========================================
new: ## Create new package (NAME=<name> DESC=<description>)
	@if [ -z "$(NAME)" ]; then echo "Usage: make new NAME=package-name DESC='description'"; exit 1; fi
	python scripts/create_package.py "$(NAME)" "$(DESC)"

new-github: ## Create new package with GitHub repo (NAME=<name> DESC=<description>)
	@if [ -z "$(NAME)" ]; then echo "Usage: make new-github NAME=package-name DESC='description'"; exit 1; fi
	python scripts/create_package.py "$(NAME)" "$(DESC)" --github
