# Python Architecture Patterns

## 1. Layered Architecture

Most popular for web applications and APIs.

```
┌─────────────────────────┐
│   API Layer             │
├─────────────────────────┤
│   Business Layer        │
├─────────────────────────┤
│   Data Access Layer     │
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

## 2. Clean Architecture / Hexagonal

For complex domains and microservices.

```
         ┌──────────────────┐
         │   External APIs  │
         └────────┬─────────┘
                  │
    ┌─────────────▼─────────────┐
    │      Adapters             │
    │   ┌───────────────────┐   │
    │   │   Use Cases       │   │
    │   │  ┌─────────────┐  │   │
    │   │  │   Domain    │  │   │
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

## 3. Modular Monolith

For growing projects that may evolve into microservices.

```
src/
├── users/              # Independent module
│   ├── api.py
│   ├── service.py
│   └── repository.py
├── orders/
└── payments/
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

## Example Implementations

### 1. Layered Architecture
**Package**: `arch-layer-prod-mongo-fast`

**Stack**: FastAPI + MongoDB + Redis + Elasticsearch + RabbitMQ

**Structure**:
```
src/arch_layer_prod_mongo_fast/
├── api/              # FastAPI routes
├── services/         # Business logic
├── repositories/     # Data access (MongoDB, Redis, Elasticsearch)
├── models/           # Pydantic models
└── middleware/       # Logging, auth
```

**Use case**: Product catalog service with caching and search

**Features**:
- Transparent caching (Redis)
- Full-text search (Elasticsearch)
- Event logging (RabbitMQ)
- Observability (Loki + Grafana)

---

### 2. Hexagonal Architecture
**Package**: `arch-hexagonal-postgresql-fast`

**Stack**: FastAPI + PostgreSQL + Stripe/PayPal + RabbitMQ + Redis

**Structure**:
```
src/arch_hexagonal_postgresql_fast/
├── domain/           # Pure business logic (no deps)
│   ├── entities/     # Payment, Transaction, Customer
│   └── value_objects/ # Amount, Status, PaymentMethod
├── application/      # Use cases + ports (interfaces)
│   ├── ports/        # Repository, Provider, EventPublisher
│   └── use_cases/    # ProcessPayment, RefundPayment
└── adapters/         # Infrastructure implementations
    ├── database/     # PostgreSQL (SQLAlchemy)
    ├── payment_providers/ # Stripe, PayPal
    ├── messaging/    # RabbitMQ
    └── api/          # FastAPI
```

**Use case**: Payment processing service with multiple providers

**Features**:
- Multiple payment providers (Stripe, PayPal)
- Idempotency guarantees (Redis)
- Event-driven (RabbitMQ)
- ACID transactions (PostgreSQL)
- Full hexagonal pattern implementation

**Key differences from Layered**:
- Domain layer has zero external dependencies
- Ports (interfaces) defined with `typing.Protocol`
- Easy to swap implementations (e.g., add new payment provider)
- Use cases orchestrate domain logic without infrastructure concerns

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
