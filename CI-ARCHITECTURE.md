# CI Architecture

## Overview

This monorepo uses **Independent CI** architecture where each package (git submodule) has its own complete CI pipeline. The parent repository provides minimal orchestration.

## Design Principles

1. **Submodule Autonomy** — Each package can be developed and tested independently
2. **No Duplication** — Parent repo does NOT run linting/type-checking for children
3. **Clear Separation** — Parent handles security + submodule health, children handle full CI
4. **Standardization** — All packages use consistent CI structure

## Architecture Pattern

### Parent Repository (`python-templates`)

**Purpose:** Security scanning and orchestrating child CI workflows

**CI Jobs:**
- `security` — Run bandit and gitleaks on parent repo code
- `trigger-submodules` — Send `repository_dispatch` events to all child repos
- `wait-for-submodules` — Poll child repos and wait for CI completion
- `notify-success` — Aggregate status notification

**Location:** `.github/workflows/monorepo-ci.yml`

**Requirements:**
- `GH_PAT` secret with `repo` and `workflow` scopes
- See [.github/SETUP.md](.github/SETUP.md) for setup instructions

**Workflow:**
1. Parent CI runs on push/PR
2. Security job scans parent code only
3. Trigger job sends repository_dispatch to each child
4. Wait job polls child repos until their CI completes
5. Notify job reports overall status

**What it does NOT do:**
- ❌ Lint submodule code
- ❌ Type-check submodule code
- ❌ Run submodule tests
- ❌ Check submodule coverage

### Child Packages (Submodules)

**Purpose:** Complete independent CI pipeline for each package

**Standard CI Jobs:**
1. `lint` — Ruff linting and formatting checks
2. `type-check` — Mypy type checking
3. `security` — Bandit + gitleaks for package code
4. `unit-tests` — Fast tests with mocks, no external dependencies
5. `integration-tests` — Tests with testcontainers (databases, services)
6. `coverage` — Combine coverage from unit + integration, enforce 80% threshold
7. `notify-success` — Success notification

**Location:** `packages/<name>/.github/workflows/ci.yml`

**Coverage Strategy:**
- Unit tests → `.coverage.unit` artifact
- Integration tests → `.coverage.integration` artifact
- Coverage job combines both using `coverage combine`
- Upload artifacts with `include-hidden-files: true` for dotfiles
- Minimum threshold: 80% (`fail_under = 80`)

## Test Structure

Each package follows strict separation:

```
tests/
├── unit/               # Fast tests, mocked dependencies
│   ├── __init__.py
│   ├── conftest.py    # Unit test fixtures (mocks, test data)
│   └── test_*.py      # Unit tests
└── integration/       # Real integration tests
    ├── __init__.py
    ├── conftest.py    # Integration fixtures (testcontainers)
    └── test_*.py      # Integration tests
```

**Unit Tests:**
- Use mocks, no real databases/services
- Fast execution (< 1 second per test)
- Test business logic in isolation
- Example: `test_app` fixture without FastAPI lifespan

**Integration Tests:**
- Use testcontainers for real dependencies
- Test actual integrations (MongoDB, Redis, Elasticsearch)
- Slower execution (containers startup overhead)
- Verify end-to-end functionality

## Triggering CI

### Submodule CI Triggers

Each submodule CI runs on:
- `push` to `main` branch
- Pull requests to `main`
- `repository_dispatch` event `parent_repo_update`

### Parent Triggering Children

When parent repo updates, it triggers child CI via `repository_dispatch`:

```yaml
- name: Trigger child CI
  run: |
    gh api repos/owner/child-repo/dispatches \
      -f event_type=parent_repo_update \
      -f client_payload[parent_run_id]=${{ github.run_id }}
  env:
    GH_TOKEN: ${{ secrets.GH_PAT }}
```

Parent then waits for child CI completion:

```yaml
- name: Wait for child CI
  run: |
    for i in {1..60}; do
      status=$(gh api repos/owner/child-repo/actions/runs \
        --jq '.workflow_runs[0].status')
      if [[ "$status" == "completed" ]]; then
        conclusion=$(gh api repos/owner/child-repo/actions/runs \
          --jq '.workflow_runs[0].conclusion')
        if [[ "$conclusion" == "success" ]]; then
          echo "✅ Child CI passed"
          break
        else
          exit 1
        fi
      fi
      sleep 10
    done
  env:
    GH_TOKEN: ${{ secrets.GH_PAT }}
```

## Creating New Packages

Use the creation script which includes CI by default:

```bash
# Local package
python scripts/create_package.py <name> "<description>"

# With GitHub repository
python scripts/create_package.py <name> "<description>" --github

# Or via Makefile
make new NAME=<name> DESC="<description>"
make new-github NAME=<name> DESC="<description>"
```

**Generated CI includes:**
- All standard jobs (lint, type-check, security, unit-tests, integration-tests, coverage)
- Separated test structure (tests/unit/, tests/integration/)
- Coverage artifacts with hidden file support
- Python 3.14 with allow-prereleases
- Proper cache configuration for pip

## Migration Guide

### Updating Existing Packages

To align existing package with Independent CI pattern:

1. **Separate tests** (if not already done):
   ```bash
   cd packages/<name>
   mkdir -p tests/unit tests/integration
   mv tests/test_*.py tests/unit/  # or tests/integration/
   ```

2. **Update CI workflow** — Replace `.github/workflows/ci.yml` with standard template:
   - Add `repository_dispatch` trigger
   - Separate unit/integration test jobs
   - Use `COVERAGE_FILE` environment variable
   - Add `include-hidden-files: true` to artifacts
   - Add coverage combine job

3. **Update pyproject.toml** — Ensure `fail_under = 80`:
   ```toml
   [tool.coverage.report]
   fail_under = 80
   ```

4. **Update .gitignore** — Add coverage patterns:
   ```
   .coverage
   .coverage.*
   coverage.xml
   htmlcov/
   ```

5. **Commit and push** to submodule, then update parent reference

### Example: arch-layer-prod-mongo-fast

Reference implementation with all features:
- Separated unit/integration tests
- FastAPI app without lifespan for unit tests
- Testcontainers for MongoDB, Redis, Elasticsearch
- Full coverage with 80% threshold
- All standard CI jobs working

## Troubleshooting

### Coverage Artifacts Not Found

**Problem:** `upload-artifact@v4` can't find `.coverage.*` files

**Solution:** Add `include-hidden-files: true`:
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: coverage-unit
    path: .coverage.unit
    include-hidden-files: true
```

### pytest-cov vs coverage Command Conflict

**Problem:** Running `pytest --cov` with `coverage run` causes conflicts

**Solution:** Use `-p no:cov` flag:
```yaml
- run: coverage run -m pytest tests/unit -v -p no:cov
```

### Unit Tests Connecting to External Services

**Problem:** FastAPI lifespan events run even in tests

**Solution:** Create `test_app` fixture without lifespan in `tests/unit/conftest.py`:
```python
@pytest.fixture
def test_app() -> FastAPI:
    """FastAPI app WITHOUT lifespan for unit tests."""
    from myapp.api.routes import router
    app = FastAPI()  # No lifespan parameter
    app.include_router(router)
    return app
```

### Submodule Not Updating

**Problem:** Parent repo shows outdated submodule reference

**Solution:**
```bash
# In submodule
git push

# In parent repo
cd ../..
git add packages/<name>
git commit -m "chore: update <name> submodule reference"
git push
```

## Best Practices

1. **Always separate unit/integration tests** — Different fixtures, different purposes
2. **Run unit tests first** — Faster feedback, catch logic errors early
3. **Use testcontainers for integration** — Real dependencies, disposable containers
4. **Commit submodules first** — Never update parent reference before pushing submodule
5. **Keep 80% coverage minimum** — Practical threshold, focus on critical paths
6. **Use mocks in unit tests** — httpx_mock, pytest-mock for external calls
7. **Document complex fixtures** — Help future maintainers understand test setup
8. **Cache pip dependencies** — Add `cache: "pip"` to setup-python steps

## Terminology

- **Parent Repository** — Main monorepo (`python-templates`) containing submodules
- **Child Package / Submodule** — Individual package with independent git repository
- **Independent CI** — Each submodule has complete self-contained CI pipeline
- **Unit Tests** — Isolated tests with mocked dependencies
- **Integration Tests** — Tests with real external services (testcontainers)
- **Coverage Artifacts** — `.coverage.*` files uploaded as GitHub artifacts
- **Submodule Reference** — Git commit hash tracked by parent repo

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [coverage.py Documentation](https://coverage.readthedocs.io/)
- [testcontainers-python](https://testcontainers-python.readthedocs.io/)
- [Git Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
