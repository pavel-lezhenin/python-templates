#!/usr/bin/env python3
"""Push changes to submodule repositories with proper markers."""

from __future__ import annotations

import subprocess
from pathlib import Path


def push_submodule(submodule_path: str) -> None:
    """Push submodule changes with [from-parent] marker."""
    path = Path(submodule_path)

    if not path.exists():
        print(f"❌ Submodule not found: {submodule_path}")
        return

    # Check if there are changes
    result = subprocess.run(
        ["git", "-C", str(path), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    )

    if not result.stdout.strip():
        print(f"✅ No changes in {submodule_path}")
        return

    # Add all changes
    subprocess.run(["git", "-C", str(path), "add", "-A"], check=True)

    # Commit with marker
    commit_msg = input(f"Commit message for {submodule_path}: ")
    full_msg = f"{commit_msg} [from-parent]"

    subprocess.run(
        ["git", "-C", str(path), "commit", "-m", full_msg],
        check=True,
    )

    # Push
    subprocess.run(["git", "-C", str(path), "push"], check=True)
    print(f"✅ Pushed {submodule_path}")


def main() -> None:
    """Push all submodules."""
    submodules = [
        "packages/arch-layer-prod-mongo-fast",
        "packages/fast-simple-crud",
    ]

    for submodule in submodules:
        push_submodule(submodule)

    print("\n✅ All submodules updated!")


if __name__ == "__main__":
    main()
