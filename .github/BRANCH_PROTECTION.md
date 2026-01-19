# Branch Protection Setup

> **IRON RULE:** No direct commits to `main` — all changes go through Pull Requests with passing CI

## Overview

This document describes how to configure GitHub Branch Protection Rules for the parent repository (`python-templates`) and all child packages (submodules).

## Required Settings

### For ALL Repositories (Parent + Children)

Go to: **Settings → Branches → Add branch protection rule**

**Branch name pattern:** `main`

| Setting | Value | Why |
|---------|-------|-----|
| **Require a pull request before merging** | ✅ Enabled | No direct pushes to main |
| **Require approvals** | ❌ Disabled | Solo developer workflow |
| **Require status checks to pass before merging** | ✅ Enabled | CI must pass |
| **Require branches to be up to date before merging** | ✅ Enabled | Prevent merge conflicts |
| **Do not allow bypassing the above settings** | ✅ Enabled | Even admins follow rules |

### Required Status Checks

#### Parent Repository (`python-templates`)

Select these status checks as required:
- `Security Scan (Parent Repo Only)`
- `Wait for Child CI Completion`
- `All CI Passed (Parent + Children)`

#### Child Packages

Select these status checks as required:
- `lint`
- `type-check`
- `security`
- `unit-tests`
- `integration-tests`
- `coverage`

## Step-by-Step Setup

### 1. Open Repository Settings

```
https://github.com/<owner>/<repo>/settings/branches
```

### 2. Add Branch Protection Rule

1. Click **"Add branch protection rule"**
2. Enter `main` in **"Branch name pattern"**
3. Configure settings as described above
4. Click **"Create"** or **"Save changes"**

### 3. Verify Protection

Try to push directly to main:

```bash
git checkout main
echo "test" >> test.txt
git add test.txt
git commit -m "test: direct commit"
git push
```

Expected result: **Push rejected** with error message about protected branch.

## Workflow After Setup

```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes and commit
git add .
git commit -m "feat: add my feature"

# 3. Push feature branch
git push -u origin feature/my-feature

# 4. Create Pull Request on GitHub
# 5. Wait for CI checks to pass
# 6. Merge PR (squash recommended)
# 7. Delete feature branch
git checkout main
git pull
git branch -d feature/my-feature
```

## Local Protection (Pre-commit Hook)

In addition to GitHub protection, we have a local pre-commit hook that blocks commits to `main`:

```bash
# This will fail if you're on main branch
git checkout main
git commit -m "test"
# ❌ ERROR: Direct commits to 'main' branch are not allowed!
```

## Repositories to Configure

| Repository | URL |
|------------|-----|
| **python-templates** (parent) | `github.com/pavel-lezhenin/python-templates` |
| **fast-simple-crud** | `github.com/pavel-lezhenin/fast-simple-crud` |
| **arch-layer-prod-mongo-fast** | `github.com/pavel-lezhenin/arch-layer-prod-mongo-fast` |
| **arch-hexagonal-postgresql-fast** | `github.com/pavel-lezhenin/arch-hexagonal-postgresql-fast` |

## Troubleshooting

### "Required status check is expected"

Status check names must match exactly what CI reports. Check **Actions → Recent runs** for exact job names.

### "Push rejected by branch protection"

This is expected behavior. Create a feature branch and use Pull Request.

### "Administrator can bypass"

Enable **"Do not allow bypassing the above settings"** to enforce rules for everyone.
