# Copilot Instructions

## Language Rules

- **STRICT: English only** — all code, comments, docstrings, commit messages
- No transliteration, no mixed languages
- Follow English grammar and spelling rules
- Variable/function names in English (camelCase or snake_case)

## Python Paradigm

- Use **Python 3.11+** features
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

- 100% coverage required
- One test file per source file
- Use fixtures, avoid duplication
- Test file naming: `test_<module>.py`
