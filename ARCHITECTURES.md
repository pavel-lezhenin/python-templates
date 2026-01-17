# Python Architecture Patterns

## 1. Layered Architecture (Слоистая архитектура)

Most popular for web applications and APIs.

```
┌─────────────────────────┐
│   Presentation Layer    │  ← API endpoints, controllers
├─────────────────────────┤
│    Business Layer       │  ← Services, use cases
├─────────────────────────┤
│   Data Access Layer     │  ← Repositories, ORM
├─────────────────────────┤
│      Database           │
└─────────────────────────┘
```

### Structure

```
src/-
├── api/           # Presentation
├── services/      # Business logic
├── repositories/  # Data access
└── models/        # Domain entities
```

### When to use

- CRUD APIs
- Simple services
- MVP / prototypes
- Small teams

---

## 2. Clean Architecture / Hexagonal (Чистая архитектура)

For complex domains, microservices, and systems with many integrations.

```
         ┌──────────────────┐
         │   External APIs  │
         └────────┬─────────┘
                  │
    ┌─────────────▼─────────────┐
    │        Adapters           │  ← Controllers, Repos impl
    │   ┌───────────────────┐   │
    │   │    Use Cases      │   │  ← Application logic
    │   │  ┌─────────────┐  │   │
    │   │  │   Domain    │  │   │  ← Entities, business rules
    │   │  └─────────────┘  │   │
    │   └───────────────────┘   │
    └───────────────────────────┘
```

### Structure

```
src/
├── domain/        # Entities, value objects
│   ├── entities/
│   └── value_objects/
├── use_cases/     # Application services
├── adapters/      # REST, DB, external APIs
│   ├── api/
│   ├── db/
│   └── external/
└── ports/         # Interfaces (Protocol)
    ├── repositories.py
    └── services.py
```

### Key principles

- Dependency inversion (inner layers don't depend on outer)
- Use `typing.Protocol` for interfaces
- Domain layer has no external dependencies

### When to use

- Complex business logic
- Many external integrations
- Long-lived projects
- When testability is critical

---

## 3. Modular Monolith (Модульный монолит)

For growing projects that may evolve into microservices.

```
src/
├── users/              # Independent module
│   ├── api.py
│   ├── service.py
│   ├── repository.py
│   └── models.py
├── orders/             # Another independent module
│   ├── api.py
│   ├── service.py
│   ├── repository.py
│   └── models.py
├── payments/           # Third module
│   └── ...
└── shared/             # Shared utilities
    ├── database.py
    └── exceptions.py
```

### Key principles

- Each module is self-contained
- Modules communicate through defined interfaces
- Shared code is minimal
- Each module can become a microservice

### When to use

- Medium/large projects
- Teams of 3+ developers
- When future scaling is expected
- Unclear microservice boundaries

---

## Comparison Table

| Criteria              | Layered        | Clean/Hexagonal | Modular Monolith |
|-----------------------|----------------|-----------------|------------------|
| Complexity            | Low            | High            | Medium           |
| Learning curve        | Easy           | Steep           | Moderate         |
| Testability           | Good           | Excellent       | Good             |
| Scalability           | Limited        | High            | High             |
| Refactoring cost      | Medium         | Low             | Low              |
| Best for team size    | 1-3            | 3+              | 3+               |
| Typical project size  | Small          | Medium-Large    | Medium-Large     |

---

## Python-Specific Recommendations

### Use these tools

- **Pydantic** for models and validation
- **FastAPI** for APIs (automatic OpenAPI)
- **SQLAlchemy** or **SQLModel** for data access
- **typing.Protocol** for interfaces
- **dependency-injector** for DI (optional)

### Code organization

```python
# Always use type hints
from __future__ import annotations

# Use Protocol for interfaces
from typing import Protocol

class UserRepository(Protocol):
    async def get_by_id(self, user_id: int) -> User | None: ...
    async def save(self, user: User) -> User: ...

# Use dataclasses or Pydantic for entities
from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    name: str
```

### File limits

- Max 200 lines per file
- Max 30 lines per function
- Max 10 methods per class
- Max 5 arguments per function
