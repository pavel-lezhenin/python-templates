#!/usr/bin/env python3
"""CLI tool for creating new packages with base configurations.

Uses Jinja2 templates from the `templates/` directory for maintainability
and separation of concerns.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


ROOT_DIR = Path(__file__).parent.parent
PACKAGES_DIR = ROOT_DIR / "packages"
TEMPLATES_DIR = ROOT_DIR / "templates"

# =============================================================================
# Version Constants (single source of truth)
# =============================================================================
PYTHON_VERSION = "3.14"
PYTHON_VERSION_SHORT = "py314"
RUFF_VERSION = "v0.14.0"


# =============================================================================
# Jinja2 Environment Setup
# =============================================================================


def _create_jinja_env() -> Environment:
    """Create Jinja2 environment with template directory."""
    return Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        keep_trailing_newline=True,
        trim_blocks=False,
        lstrip_blocks=False,
    )


# =============================================================================
# Package Creation
# =============================================================================


def _create_directory_structure(package_dir: Path, module_name: str) -> None:
    """Create package directory structure."""
    dirs = [
        package_dir / "src" / module_name,
        package_dir / "tests" / "unit",
        package_dir / "tests" / "integration",
        package_dir / ".github" / "workflows",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def _write_package_files(package_dir: Path, template_vars: dict[str, str]) -> None:
    """Write all package files from Jinja2 templates."""
    env = _create_jinja_env()
    module_name = template_vars["module_name"]

    # Map of output file path -> template file path
    files = {
        "pyproject.toml": "pyproject.toml.j2",
        ".pre-commit-config.yaml": ".pre-commit-config.yaml.j2",
        ".gitignore": ".gitignore.j2",
        ".secrets.baseline": ".secrets.baseline.j2",
        ".github/workflows/ci.yml": ".github/workflows/ci.yml.j2",
        "README.md": "README.md.j2",
        ".env.example": ".env.example.j2",
        f"src/{module_name}/__init__.py": "src/__init__.py.j2",
        f"src/{module_name}/client.py": "src/client.py.j2",
        "tests/__init__.py": None,  # Empty file
        "tests/unit/__init__.py": None,  # Empty file
        "tests/unit/conftest.py": "tests/unit/conftest.py.j2",
        "tests/unit/test_client.py": "tests/unit/test_client.py.j2",
        "tests/integration/__init__.py": None,  # Empty file
        "tests/integration/conftest.py": "tests/integration/conftest.py.j2",
    }

    # Static files (no template rendering needed)
    static_files = {
        f"src/{module_name}/py.typed": "",
    }

    for filepath, template_name in files.items():
        file_path = package_dir / filepath
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if template_name is None:
            # Empty file
            file_path.write_text("", encoding="utf-8")
        else:
            template = env.get_template(template_name)
            content = template.render(**template_vars)
            file_path.write_text(content, encoding="utf-8")

        print(f"  Created: {filepath}")

    for filepath, content in static_files.items():
        file_path = package_dir / filepath
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        print(f"  Created: {filepath}")


def _init_git_repo(package_dir: Path) -> None:
    """Initialize git repository with initial commit."""
    print("\nInitializing git repository...")
    subprocess.run(
        ["git", "init", "--initial-branch=main"],
        cwd=package_dir,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "add", "-A"], cwd=package_dir, check=True, capture_output=True
    )
    subprocess.run(
        ["git", "commit", "-m", "feat: initial package setup", "--no-verify"],
        cwd=package_dir,
        check=True,
        capture_output=True,
    )
    print("  Git initialized with initial commit (branch: main)")


def _create_github_and_submodule(
    name: str, package_dir: Path, github_user: str, github_url: str
) -> bool:
    """Create GitHub repo and register as submodule."""
    print("\nCreating GitHub repository...")
    result = subprocess.run(
        [
            "gh",
            "repo",
            "create",
            f"{github_user}/{name}",
            "--public",
            "--source=.",
            "--push",
        ],
        cwd=package_dir,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  Warning: Could not create GitHub repo: {result.stderr}")
        print("  Package created locally without submodule registration")
        return False

    print(f"  GitHub repository created: {github_url}")

    # Ensure default branch is 'main' on GitHub
    subprocess.run(
        ["gh", "repo", "edit", f"{github_user}/{name}", "--default-branch", "main"],
        cwd=package_dir,
        capture_output=True,
    )
    print("  Default branch set to 'main'")

    # Remove local .git and re-add as submodule
    print("\nRegistering as git submodule...")
    git_dir = package_dir / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)
    shutil.rmtree(package_dir)

    # Add as submodule from parent repo
    subprocess.run(
        ["git", "submodule", "add", github_url, f"packages/{name}"],
        cwd=ROOT_DIR,
        check=True,
        capture_output=True,
    )
    print(f"  Submodule registered: packages/{name}")

    # Commit submodule addition
    subprocess.run(
        ["git", "add", ".gitmodules", f"packages/{name}"],
        cwd=ROOT_DIR,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            f"feat: add {name} package as submodule",
            "--no-verify",
        ],
        cwd=ROOT_DIR,
        check=True,
        capture_output=True,
    )
    print("  Submodule committed to main repository")
    return True


def create_package(
    name: str,
    description: str,
    *,
    init_git: bool = True,
    create_remote: bool = False,
    github_user: str = "pavel-lezhenin",
) -> Path:
    """Create a new package with all configurations.

    Args:
        name: Package name (e.g., 'openai-template').
        description: Short package description.
        init_git: Initialize git repository.
        create_remote: Create GitHub repository and add as submodule.
        github_user: GitHub username for repository URL.

    Returns:
        Path to created package.
    """
    module_name = name.replace("-", "_")
    module_upper = module_name.upper()
    package_dir = PACKAGES_DIR / name
    github_url = f"https://github.com/{github_user}/{name}.git"

    if package_dir.exists():
        print(f"Error: Package '{name}' already exists at {package_dir}")
        sys.exit(1)

    print(f"Creating package: {name}")
    print(f"  Module name: {module_name}")
    print(f"  Location: {package_dir}")

    _create_directory_structure(package_dir, module_name)

    template_vars = {
        "package_name": name,
        "module_name": module_name,
        "module_upper": module_upper,
        "description": description,
        "python_version": PYTHON_VERSION,
        "python_version_short": PYTHON_VERSION_SHORT,
        "ruff_version": RUFF_VERSION,
    }

    _write_package_files(package_dir, template_vars)

    if init_git:
        _init_git_repo(package_dir)

    submodule_created = False
    if create_remote:
        submodule_created = _create_github_and_submodule(
            name, package_dir, github_user, github_url
        )

    print(f"\n✅ Package '{name}' created successfully!")
    if submodule_created:
        print(f"\nGitHub: {github_url.replace('.git', '')}")
        print("\nNext steps:")
        print(f"  cd packages/{name}")
        print("  pip install -e '.[dev]'")
        print("  pre-commit install")
        print("\n  # Push main repo to update submodule reference:")
        print("  cd ../..")
        print("  git push")
    else:
        print("\nNext steps:")
        print(f"  cd packages/{name}")
        print("  pip install -e '.[dev]'")
        print("  pre-commit install")
        if not create_remote:
            print("\n  # To publish as submodule later:")
            print(f'  python scripts/create_package.py {name} "{description}" --github')

    return package_dir


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Create a new Python package with base configurations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python scripts/create_package.py openai-client "OpenAI API client"
  python scripts/create_package.py anthropic-sdk "Anthropic SDK" --github
  python scripts/create_package.py my-pkg "My package" --github --user myname
        """,
    )
    parser.add_argument(
        "name",
        help="Package name (e.g., 'openai-client')",
    )
    parser.add_argument(
        "description",
        help="Short package description",
    )
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="Skip git initialization",
    )
    parser.add_argument(
        "--github",
        action="store_true",
        help="Create GitHub repository and register as submodule",
    )
    parser.add_argument(
        "--user",
        default="pavel-lezhenin",
        help="GitHub username (default: pavel-lezhenin)",
    )

    args = parser.parse_args()

    create_package(
        args.name,
        args.description,
        init_git=not args.no_git,
        create_remote=args.github,
        github_user=args.user,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
