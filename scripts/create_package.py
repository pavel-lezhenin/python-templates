#!/usr/bin/env python3
"""CLI tool for creating new packages with base configurations."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from string import Template


ROOT_DIR = Path(__file__).parent.parent
PACKAGES_DIR = ROOT_DIR / "packages"


# =============================================================================
# Templates
# =============================================================================

PYPROJECT_TEMPLATE = Template('''\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "$package_name"
version = "0.1.0"
description = "$description"
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"
authors = [{ name = "Your Name", email = "your@email.com" }]
classifiers = [
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Typing :: Typed",
]

dependencies = [
    "httpx>=0.27.0",
    "pydantic>=2.8.0",
    "pydantic-settings>=2.4.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.5.0",
    "mypy>=1.11.0",
    "pytest>=8.0.0",
    "pytest-cov>=5.0.0",
    "pytest-asyncio>=0.24.0",
    "pytest-httpx>=0.30.0",
    "bandit>=1.7.0",
    "pre-commit>=3.8.0",
]

[tool.hatch.build.targets.wheel]
packages = ["src/$module_name"]

# ==================================================
# RUFF
# ==================================================
[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.format]
quote-style = "double"
docstring-code-format = true

[tool.ruff.lint]
select = [
    "E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM", "TCH", "PTH",
    "ERA", "PL", "RUF", "PERF", "S", "ANN", "D", "N", "ASYNC", "A",
    "DTZ", "T10", "EM", "LOG", "G", "PIE", "T20", "Q", "RSE", "RET",
    "SLF", "SLOT", "TID", "TRY", "FLY",
]
ignore = ["D100", "D104", "D107", "ANN101", "ANN102", "COM812"]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101", "ANN", "D", "PLR2004"]
"**/__init__.py" = ["F401"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.isort]
known-first-party = ["$module_name"]

# ==================================================
# MYPY
# ==================================================
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
show_error_codes = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
no_implicit_optional = true
warn_unreachable = true

[[tool.mypy.overrides]]
module = ["tests.*"]
disallow_untyped_defs = false

# ==================================================
# PYTEST
# ==================================================
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-fail-under=100",
]
asyncio_mode = "auto"

# ==================================================
# COVERAGE
# ==================================================
[tool.coverage.run]
source = ["src"]
branch = true
omit = ["**/tests/*", "**/__init__.py"]

[tool.coverage.report]
fail_under = 100
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "@abstractmethod",
    "raise NotImplementedError",
]

[tool.bandit]
exclude_dirs = ["tests"]
skips = ["B101"]
''')

PRECOMMIT_TEMPLATE = '''\
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-added-large-files
      - id: detect-private-key

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks:
      - id: gitleaks

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.6
    hooks:
      - id: ruff
        args: ['--fix', '--exit-zero']
      - id: ruff-format

  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.28.0
    hooks:
      - id: commitizen
        stages: [commit-msg]
'''

GITIGNORE_TEMPLATE = '''\
__pycache__/
*.py[cod]
.venv/
venv/
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.ruff_cache/
.env
.env.*
!.env.example
*.pem
*.key
.idea/
.vscode/
.DS_Store
Thumbs.db
'''

SECRETS_BASELINE_TEMPLATE = '''\
{
  "version": "1.5.0",
  "plugins_used": [
    {"name": "AWSKeyDetector"},
    {"name": "AzureStorageKeyDetector"},
    {"name": "BasicAuthDetector"},
    {"name": "GitHubTokenDetector"},
    {"name": "JwtTokenDetector"},
    {"name": "KeywordDetector"},
    {"name": "PrivateKeyDetector"},
    {"name": "SlackDetector"},
    {"name": "StripeDetector"}
  ],
  "filters_used": [
    {"path": "detect_secrets.filters.allowlist.is_line_allowlisted"},
    {"path": "detect_secrets.filters.heuristic.is_likely_id_string"}
  ],
  "results": {},
  "generated_at": "2026-01-17T00:00:00Z"
}
'''

CI_TEMPLATE = '''\
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install ruff
      - run: ruff check .
      - run: ruff format --check .

  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: mypy src

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install bandit
      - run: bandit -r src -c pyproject.toml
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: pytest --cov --cov-fail-under=100
'''

README_TEMPLATE = Template('''\
# $package_name

$description

## 📦 Installation

```bash
# From GitHub
pip install git+https://github.com/yourname/$package_name.git

# For development
git clone https://github.com/yourname/$package_name.git
cd $package_name
pip install -e ".[dev]"
pre-commit install
```

## 🚀 Usage

```python
from $module_name import Client

async with Client() as client:
    result = await client.request()
```

## 🛠️ Development

```bash
ruff check .      # Linting
ruff format .     # Formatting
mypy src          # Type checking
pytest            # Tests
```

## 📋 Standards

- ✅ Strict typing (mypy strict)
- ✅ 100% test coverage
- ✅ Auto-formatting (ruff)
- ✅ Secret detection
''')

INIT_TEMPLATE = Template('''\
"""$description"""

from __future__ import annotations

from typing import Final

__version__: Final[str] = "0.1.0"
''')

CLIENT_TEMPLATE = Template('''\
"""Client implementation for $package_name."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import httpx
from pydantic import BaseModel
from pydantic_settings import BaseSettings

if TYPE_CHECKING:
    from types import TracebackType


logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Configuration from environment variables."""

    api_base_url: str = "https://api.example.com"
    api_timeout: float = 30.0

    model_config = {"env_prefix": "${module_upper}_"}


class Response(BaseModel):
    """Standard API response model."""

    status: str
    data: dict[str, Any]


class Client:
    """HTTP API client with type safety."""

    def __init__(
        self,
        base_url: str | None = None,
        *,
        timeout: float | None = None,
    ) -> None:
        """Initialize the client.

        Args:
            base_url: API base URL. Defaults to env variable.
            timeout: Request timeout in seconds.
        """
        settings = Settings()
        self._base_url = (base_url or settings.api_base_url).rstrip("/")
        self._timeout = timeout or settings.api_timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> Client:
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._timeout,
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    async def get(self, endpoint: str) -> Response:
        """Perform GET request.

        Args:
            endpoint: API endpoint path.

        Returns:
            Parsed API response.

        Raises:
            RuntimeError: If client is not initialized.
        """
        if not self._client:
            msg = "Client not initialized. Use async context manager."
            raise RuntimeError(msg)

        logger.debug("GET %s", endpoint)
        response = await self._client.get(endpoint)
        response.raise_for_status()

        return Response(status="ok", data=response.json())
''')

CONFTEST_TEMPLATE = '''\
"""Pytest configuration and fixtures."""

from __future__ import annotations

import pytest


@pytest.fixture
def base_url() -> str:
    """Provide test base URL."""
    return "https://api.example.com"
'''

TEST_CLIENT_TEMPLATE = Template('''\
"""Tests for client module."""

from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from $module_name.client import Client, Response, Settings


class TestSettings:
    """Tests for Settings."""

    def test_default_values(self):
        """Test default configuration values."""
        settings = Settings()

        assert settings.api_base_url == "https://api.example.com"
        assert settings.api_timeout == 30.0


class TestResponse:
    """Tests for Response model."""

    def test_create_response(self):
        """Test creating a response."""
        response = Response(status="ok", data={"key": "value"})

        assert response.status == "ok"
        assert response.data == {"key": "value"}


class TestClient:
    """Tests for Client."""

    def test_init_defaults(self):
        """Test client initialization with defaults."""
        client = Client()

        assert client._base_url == "https://api.example.com"
        assert client._timeout == 30.0

    def test_init_custom_values(self):
        """Test client initialization with custom values."""
        client = Client("https://custom.api.com/", timeout=60.0)

        assert client._base_url == "https://custom.api.com"
        assert client._timeout == 60.0

    def test_init_strips_trailing_slash(self):
        """Test that trailing slash is stripped."""
        client = Client("https://api.example.com/")

        assert client._base_url == "https://api.example.com"

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager."""
        async with Client() as client:
            assert client._client is not None

    @pytest.mark.asyncio
    async def test_get_success(self, httpx_mock: HTTPXMock):
        """Test successful GET request."""
        httpx_mock.add_response(
            url="https://api.example.com/test",
            json={"result": "success"},
        )

        async with Client() as client:
            response = await client.get("/test")

        assert response.status == "ok"
        assert response.data == {"result": "success"}

    @pytest.mark.asyncio
    async def test_get_without_context_manager_raises(self):
        """Test that GET without context manager raises error."""
        client = Client()

        with pytest.raises(RuntimeError, match="Client not initialized"):
            await client.get("/test")
''')

ENV_EXAMPLE_TEMPLATE = Template('''\
# $package_name Configuration
# Copy to .env and fill in values

${module_upper}_API_BASE_URL=https://api.example.com
${module_upper}_API_TIMEOUT=30.0
''')


# =============================================================================
# Package Creation
# =============================================================================

def create_package(
    name: str,
    description: str,
    *,
    init_git: bool = True,
    create_remote: bool = False,
) -> Path:
    """Create a new package with all configurations.

    Args:
        name: Package name (e.g., 'openai-template').
        description: Short package description.
        init_git: Initialize git repository.
        create_remote: Create GitHub repository.

    Returns:
        Path to created package.
    """
    module_name = name.replace("-", "_")
    module_upper = module_name.upper()
    package_dir = PACKAGES_DIR / name

    if package_dir.exists():
        print(f"Error: Package '{name}' already exists at {package_dir}")
        sys.exit(1)

    print(f"Creating package: {name}")
    print(f"  Module name: {module_name}")
    print(f"  Location: {package_dir}")

    # Create directory structure
    dirs = [
        package_dir / "src" / module_name,
        package_dir / "tests",
        package_dir / ".github" / "workflows",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Template variables
    template_vars = {
        "package_name": name,
        "module_name": module_name,
        "module_upper": module_upper,
        "description": description,
    }

    # Create files
    files = {
        "pyproject.toml": PYPROJECT_TEMPLATE.substitute(template_vars),
        ".pre-commit-config.yaml": PRECOMMIT_TEMPLATE,
        ".gitignore": GITIGNORE_TEMPLATE,
        ".secrets.baseline": SECRETS_BASELINE_TEMPLATE,
        ".github/workflows/ci.yml": CI_TEMPLATE,
        "README.md": README_TEMPLATE.substitute(template_vars),
        ".env.example": ENV_EXAMPLE_TEMPLATE.substitute(template_vars),
        f"src/{module_name}/__init__.py": INIT_TEMPLATE.substitute(template_vars),
        f"src/{module_name}/py.typed": "",
        f"src/{module_name}/client.py": CLIENT_TEMPLATE.substitute(template_vars),
        "tests/__init__.py": '"""Tests package."""\n',
        "tests/conftest.py": CONFTEST_TEMPLATE,
        "tests/test_client.py": TEST_CLIENT_TEMPLATE.substitute(template_vars),
    }

    for filepath, content in files.items():
        file_path = package_dir / filepath
        file_path.write_text(content, encoding="utf-8")
        print(f"  Created: {filepath}")

    # Initialize git
    if init_git:
        print("\nInitializing git repository...")
        subprocess.run(["git", "init"], cwd=package_dir, check=True)
        subprocess.run(["git", "add", "-A"], cwd=package_dir, check=True)
        subprocess.run(
            ["git", "commit", "-m", "feat: initial package setup", "--no-verify"],
            cwd=package_dir,
            check=True,
        )
        print("  Git initialized with initial commit")

    # Create GitHub repository
    if create_remote:
        print("\nCreating GitHub repository...")
        result = subprocess.run(
            ["gh", "repo", "create", name, "--public", "--source=.", "--push"],
            cwd=package_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"  GitHub repository created and pushed")
        else:
            print(f"  Warning: Could not create GitHub repo: {result.stderr}")

    print(f"\n✅ Package '{name}' created successfully!")
    print(f"\nNext steps:")
    print(f"  cd packages/{name}")
    print(f"  pip install -e '.[dev]'")
    print(f"  pre-commit install")

    return package_dir


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Create a new Python package with base configurations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python scripts/create_package.py openai-client "OpenAI API client"
  python scripts/create_package.py anthropic-sdk "Anthropic SDK wrapper" --github
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
        help="Create GitHub repository and push",
    )

    args = parser.parse_args()

    create_package(
        args.name,
        args.description,
        init_git=not args.no_git,
        create_remote=args.github,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
