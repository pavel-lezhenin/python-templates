#!/usr/bin/env python3
"""Pre-commit hook to prevent direct commits to main/master branch.

This script enforces trunk-based development by blocking commits
to protected branches. All changes must go through feature branches
and Pull Requests.
"""

from __future__ import annotations

import subprocess
import sys


PROTECTED_BRANCHES = frozenset({"main", "master"})


def get_current_branch() -> str:
    """Get the name of the current git branch."""
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def main() -> int:
    """Check if current branch is protected and block commit if so."""
    try:
        branch = get_current_branch()
    except subprocess.CalledProcessError:
        # Not in a git repository or git error
        return 0

    if branch in PROTECTED_BRANCHES:
        print(f"\n❌ ERROR: Direct commits to '{branch}' branch are not allowed!")
        print("\n📋 Trunk-Based Development Rules:")
        print("   1. Create a feature branch: git checkout -b feature/<name>")
        print("   2. Make your changes and commit")
        print("   3. Push and create a Pull Request")
        print("   4. Wait for CI checks to pass")
        print("   5. Merge PR (squash or rebase)")
        print("\n💡 Quick fix:")
        print("   git checkout -b feature/<your-feature-name>")
        print()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
