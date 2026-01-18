# Copilot Instructions

## Language Rules

- **STRICT: English only** — all code, comments, docstrings, commit messages
- No transliteration, no mixed languages
- Follow English grammar and spelling rules
- Variable/function names in English (camelCase or snake_case)

## Project Creation

- **STRICT: Use CLI only** — never create packages manually
- Always use: `python scripts/create_package.py <name> "<description>"`
- Or via Makefile: `make new NAME=<name> DESC="<description>"`
- With GitHub: `make new-github NAME=<name> DESC="<description>"`
- This ensures all base configurations are applied automatically

## Git Submodules Workflow

- **STRICT: Commit submodules first, then parent repo** — never commit only parent
- Each package in `packages/` is a separate git submodule
- **Workflow:**
  1. Make changes in submodule (e.g., `packages/arch-layer-prod-mongo-fast/`)
  2. Commit and push changes **inside the submodule** first
  3. Return to parent repo root (`cd ../../`)
  4. Commit submodule reference update in parent repo
  5. Push parent repo
- **Before committing parent repo:** always run `make submodule-check` to verify all submodules are clean
- **Never leave uncommitted changes** in submodules when updating parent
- Each submodule has its own CI/CD that must pass before updating parent reference

## API Standards

- **STRICT: OpenAPI/Swagger required** — every API service must have OpenAPI spec
- Place spec in `openapi.yaml` or `openapi.json` at package root
- Use FastAPI with automatic OpenAPI generation when possible
- Missing OpenAPI spec = architecture error
- Document all endpoints, request/response schemas, error codes

## Python Paradigm

- Use **Python 3.14+** features
- **Strict typing** everywhere: all functions, methods, variables
- Use `from __future__ import annotations` in all files
- Prefer `dataclass` or `pydantic.BaseModel` over plain dicts
- Use `async/await` for I/O operations
- Prefer composition over inheritance
- Follow **SOLID** principles

## Code Style

- **Max file length: 200 lines** — split into modules
- **Max function length: 30 lines** — extract helpers
- **Max class methods: 10** — split responsibilities
- **Max function arguments: 5** — use dataclasses for more
- One class per file (exceptions: small related classes)
- Use `typing.Protocol` for interfaces

## File Structure

```
src/package_name/
├── __init__.py          # Public API only
├── client.py            # Main entry point
├── models/              # Pydantic models
├── services/            # Business logic
├── repositories/        # Data access
├── exceptions.py        # Custom exceptions
└── types.py             # Type aliases
```

## Secrets & Config

- **NEVER** hardcode secrets, keys, passwords
- Use environment variables via `pydantic-settings`
- Config in `.env` files (gitignored)
- Provide `.env.example` with dummy values

## Output & Logging

- **Minimal console output** — use `logging` module
- No `print()` in production code
- Log levels: DEBUG for dev, INFO for prod
- Structured logging with context

## Comments

- **Minimal comments** — code should be self-documenting
- Docstrings: public API only (Google style)
- No commented-out code
- TODO format: `# TODO(username): description`

## Testing

### Test Structure

- **Separate unit and integration tests** — use `tests/unit/` and `tests/integration/` directories
- **Unit tests** (`tests/unit/`) — use mocks, no external dependencies, fast execution
- **Integration tests** (`tests/integration/`) — use testcontainers, test real integrations
- Each directory has its own `conftest.py` with appropriate fixtures
- Test file naming: `test_<module>.py`

### Coverage Requirements

- **Minimum: 80%** (`fail_under = 80`) — CI fails below this
- **Target: 90%** — aim for this in practice
- **100% not always practical** — focus on critical paths and business logic
- Use fixtures, avoid duplication
- One test file per source file structure

## CI/CD Architecture

### Independent CI Pattern

- **Each submodule has its own complete CI pipeline** — lint, type-check, security, tests, coverage
- **Parent repo runs minimal orchestration** — only security scan and submodule health checks
- **No duplication** — parent does NOT run lint/type-check/tests for children
- **Submodules are autonomous** — can be developed and tested independently

### Parent Repository CI (`python-templates`)

**Location:** `.github/workflows/monorepo-ci.yml`

**Jobs:**
- `security` — Security scanning (bandit + gitleaks) on parent code only
- `check-submodules` — Verify all submodules are on latest commits
- `notify-success` — Aggregate status notification

**Does NOT include:**
- ❌ Linting submodule code
- ❌ Type-checking submodule code
- ❌ Running submodule tests

### Child Package CI (Submodules)

**Location:** `packages/<name>/.github/workflows/ci.yml`

**Standard Jobs (in order):**
1. `lint` — Ruff linting and formatting checks
2. `type-check` — Mypy type checking with strict mode
3. `security` — Bandit + gitleaks for package code
4. `unit-tests` — Fast tests with mocks, generate `.coverage.unit` artifact
5. `integration-tests` — Tests with testcontainers, generate `.coverage.integration` artifact
6. `coverage` — Combine both coverage files, enforce 80% threshold, upload to codecov
7. `notify-success` — Success notification (depends on all previous jobs)

**Triggers:**
- `push` to `main` branch
- Pull requests to `main`
- `repository_dispatch` event `parent_repo_update`

**Coverage Strategy:**
- Use `COVERAGE_FILE` environment variable for predictable filenames
- Upload artifacts with `include-hidden-files: true` for dotfiles (`.coverage.*`)
- Combine unit + integration coverage in final job
- Use `-p no:cov` flag to avoid pytest-cov conflicts

### Creating New Packages

Script automatically generates proper CI:

```bash
python scripts/create_package.py <name> "<description>"
make new NAME=<name> DESC="<description>"
make new-github NAME=<name> DESC="<description>"  # With GitHub repo
```

**Generated structure includes:**
- Complete CI workflow with all standard jobs
- Separated test directories (`tests/unit/`, `tests/integration/`)
- Coverage configuration with 80% threshold
- Proper artifact upload/download with hidden files support

### CI Best Practices

1. **Commit submodules first, then parent** — Never update parent reference before pushing submodule
2. **Separate unit/integration tests** — Different fixtures, different execution contexts
3. **Use mocks in unit tests** — No external dependencies, fast execution
4. **Use testcontainers in integration tests** — Real services, disposable containers
5. **Cache pip dependencies** — Add `cache: "pip"` to setup-python steps
6. **Always verify submodules clean** — Run `make submodule-check` before committing parent
7. **Let submodule CI pass first** — Wait for green CI before updating parent reference

### Terminology

- **Parent Repository** — Main monorepo (`python-templates`) containing submodules
- **Child Package / Submodule** — Individual package with independent git repository and CI
- **Independent CI** — Pattern where each submodule has complete self-contained CI pipeline
- **Unit Tests** — Isolated tests with mocked dependencies in `tests/unit/`
- **Integration Tests** — Tests with real external services in `tests/integration/`
- **Coverage Artifacts** — `.coverage.unit` and `.coverage.integration` files uploaded as GitHub artifacts
- **Submodule Reference** — Git commit hash tracked by parent repo

For detailed CI architecture documentation, see [CI-ARCHITECTURE.md](../CI-ARCHITECTURE.md)
