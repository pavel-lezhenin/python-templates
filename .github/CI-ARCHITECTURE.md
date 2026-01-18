# CI/CD Architecture

## Overview

This monorepo uses **independent submodule CI** architecture for clean separation of concerns.

## How It Works

### 1. Submodule CI (Independent)

Each package is a separate git submodule with its own CI/CD:

- **[fast-simple-crud](https://github.com/pavel-lezhenin/fast-simple-crud)**
  - Runs tests when you push to this repo
  - Has its own coverage requirements (80%+)
  - Fully independent

- **[arch-layer-prod-mongo-fast](https://github.com/pavel-lezhenin/arch-layer-prod-mongo-fast)**
  - Runs tests when you push to this repo
  - Uses testcontainers for integration tests
  - Fully independent

### 2. Monorepo CI (Orchestrator)

The parent repo CI (`monorepo-ci.yml`) checks:
- ✅ Monorepo-level linting
- ✅ Monorepo-level type checking
- ✅ Security scans across all code
- ✅ Submodule status verification

**Does NOT duplicate** submodule tests - those run in their own repos!

## Workflow

### Working on a Submodule

```bash
# 1. Make changes in submodule
cd packages/arch-layer-prod-mongo-fast
git checkout -b feature/my-feature

# 2. Commit and push to submodule repo
git add .
git commit -m "feat: add new feature"
git push origin feature/my-feature

# 3. Submodule CI runs automatically ✅
# Check: https://github.com/pavel-lezhenin/arch-layer-prod-mongo-fast/actions

# 4. After submodule CI passes, update parent repo
cd ../../
git add packages/arch-layer-prod-mongo-fast
git commit -m "chore: update arch-layer-prod-mongo-fast"
git push

# 5. Monorepo CI runs (but doesn't re-run submodule tests)
```

### Why This Architecture?

**✅ Advantages:**
- Each package is truly independent
- No duplication of CI runs
- Faster parent repo CI
- Clear separation of concerns
- Submodules can be used standalone

**❌ Old approach (don't do this):**
- Running submodule tests in parent CI
- Wastes CI time (tests run twice)
- Creates tight coupling
- Slower feedback loop

## CI Status

### View CI Status

**Monorepo:**
```bash
gh run list --repo pavel-lezhenin/python-templates
```

**Submodules:**
```bash
# fast-simple-crud
gh run list --repo pavel-lezhenin/fast-simple-crud

# arch-layer-prod-mongo-fast
gh run list --repo pavel-lezhenin/arch-layer-prod-mongo-fast
```

### Local Testing

```bash
# Test everything before committing
make submodule-check  # Check for uncommitted changes
make submodule-lint   # Lint all submodules
make submodule-test   # Test all submodules
```

## Best Practices

1. **Always commit submodule first, then parent**
   ```bash
   cd packages/my-package
   git commit && git push
   cd ../../
   git commit && git push
   ```

2. **Run `make submodule-check` before committing parent**
   - Verifies all submodules are clean
   - Prevents accidental uncommitted changes

3. **Monitor both CIs**
   - Submodule CI must pass first
   - Parent CI checks compatibility

4. **Don't duplicate tests**
   - Submodule tests belong in submodule CI
   - Parent CI is for integration only
