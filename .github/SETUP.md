# GitHub Actions Setup

## Required Secrets

### GH_PAT (Personal Access Token)

Parent repository needs a Personal Access Token to trigger CI in child repositories.

**Setup:**

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Set token name: `python-templates-ci`
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. Copy the token
7. Go to repository settings: https://github.com/pavel-lezhenin/python-templates/settings/secrets/actions
8. Click "New repository secret"
9. Name: `GH_PAT`
10. Value: paste the token
11. Click "Add secret"

## How It Works

### Parent Repository Workflow

1. **security** — Runs bandit + gitleaks on parent repo code only
2. **trigger-submodules** — Sends `repository_dispatch` events to all child repos
3. **wait-for-submodules** — Polls child repos until their CI completes
4. **notify-success** — Reports overall status

### Child Repository Workflow

Triggered by:
- Direct push to child repo
- Pull request in child repo
- `repository_dispatch` event from parent (event type: `parent_repo_update`)

Runs:
- lint (ruff)
- type-check (mypy)
- security (bandit + gitleaks)
- unit-tests
- integration-tests
- coverage (combines unit + integration)

## Verification

After setup, push to parent repo should:

1. Trigger parent CI: https://github.com/pavel-lezhenin/python-templates/actions
2. Parent triggers children via repository_dispatch
3. Child CI runs appear in:
   - https://github.com/pavel-lezhenin/fast-simple-crud/actions
   - https://github.com/pavel-lezhenin/arch-layer-prod-mongo-fast/actions
4. Parent waits for children to complete
5. Parent reports final status

## Troubleshooting

### "Resource not accessible by integration"

- Check `GH_PAT` secret exists
- Verify token has `repo` and `workflow` scopes
- Token must not be expired

### Child CI not triggering

- Verify child `.github/workflows/ci.yml` has `repository_dispatch` trigger:
  ```yaml
  on:
    repository_dispatch:
      types: [parent_repo_update]
  ```

### Timeout waiting for child CI

- Default timeout: 10 minutes (60 attempts × 10 seconds)
- Increase loop range if needed: `{1..120}` for 20 minutes
