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
