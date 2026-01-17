#!/usr/bin/env python3
"""Pre-commit role-based code review script."""

from __future__ import annotations

import ast
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Final


if TYPE_CHECKING:
    from collections.abc import Callable


MAX_FILE_LINES: Final[int] = 200
MAX_FUNCTION_LINES: Final[int] = 30
MAX_FUNCTION_ARGS: Final[int] = 5
MAX_CLASS_METHODS: Final[int] = 10
MAX_IMPORTS: Final[int] = 15
MAX_CLASSES_PER_FILE: Final[int] = 2


@dataclass
class Issue:
    """Review issue found by a role."""

    role: str
    file: str
    line: int
    message: str


def get_changed_files() -> list[Path]:
    """Get list of staged Python files."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [Path(f) for f in result.stdout.strip().split("\n") if f.endswith(".py")]


def check_dev(file: Path, tree: ast.AST, lines: list[str]) -> list[Issue]:
    """Developer role: basic code quality."""
    issues: list[Issue] = []

    if len(lines) > MAX_FILE_LINES:
        issues.append(
            Issue(
                "dev",
                str(file),
                1,
                f"File too long: {len(lines)} > {MAX_FILE_LINES} lines",
            )
        )

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "print"
        ):
            issues.append(
                Issue(
                    "dev",
                    str(file),
                    node.lineno,
                    "Use logging instead of print()",
                )
            )

        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            func_lines = node.end_lineno - node.lineno + 1 if node.end_lineno else 0
            if func_lines > MAX_FUNCTION_LINES:
                issues.append(
                    Issue(
                        "dev",
                        str(file),
                        node.lineno,
                        f"Function '{node.name}' too long: {func_lines} > "
                        f"{MAX_FUNCTION_LINES} lines",
                    )
                )

            if len(node.args.args) > MAX_FUNCTION_ARGS:
                issues.append(
                    Issue(
                        "dev",
                        str(file),
                        node.lineno,
                        f"Function '{node.name}' has {len(node.args.args)} args > "
                        f"{MAX_FUNCTION_ARGS}",
                    )
                )

    return issues


def check_tester(file: Path, tree: ast.AST, _lines: list[str]) -> list[Issue]:
    """Tester role: test-related checks."""
    issues: list[Issue] = []
    is_test_file = file.name.startswith("test_") or "/tests/" in str(file)

    if not is_test_file:
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                issues.append(
                    Issue(
                        "tester",
                        str(file),
                        node.lineno,
                        "Avoid assert in production code, use exceptions",
                    )
                )

    return issues


def check_reviewer(file: Path, tree: ast.AST, lines: list[str]) -> list[Issue]:
    """Reviewer role: code review standards."""
    issues: list[Issue] = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#") and any(
            kw in stripped for kw in ["def ", "class ", "import ", "return "]
        ):
            issues.append(Issue("reviewer", str(file), i, "Remove commented-out code"))

        if "TODO" in line and "TODO(" not in line:
            issues.append(
                Issue(
                    "reviewer",
                    str(file),
                    i,
                    "TODO must have author: TODO(username): message",
                )
            )

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            if node.name.startswith("_"):
                continue
            if node.returns is None and node.name != "__init__":
                issues.append(
                    Issue(
                        "reviewer",
                        str(file),
                        node.lineno,
                        f"Function '{node.name}' missing return type",
                    )
                )

    return issues


def check_best_practice(file: Path, tree: ast.AST, lines: list[str]) -> list[Issue]:
    """Best practice role: security and patterns."""
    issues: list[Issue] = []
    secrets_patterns = [
        "password",
        "secret",
        "api_key",
        "apikey",
        "token",
        "credential",
    ]

    for i, line in enumerate(lines, 1):
        lower = line.lower()
        for pattern in secrets_patterns:
            if (
                pattern in lower
                and "=" in line
                and ('"' in line or "'" in line)
                and "os.getenv" not in line
                and "environ" not in line
            ):
                issues.append(
                    Issue(
                        "best_practice",
                        str(file),
                        i,
                        f"Possible hardcoded secret: {pattern}",
                    )
                )

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append(
                Issue(
                    "best_practice",
                    str(file),
                    node.lineno,
                    "Avoid bare except, catch specific exceptions",
                )
            )

        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in ("eval", "exec")
        ):
            issues.append(
                Issue(
                    "best_practice",
                    str(file),
                    node.lineno,
                    f"Avoid {node.func.id}() — security risk",
                )
            )

    return issues


def check_architect(file: Path, tree: ast.AST, _lines: list[str]) -> list[Issue]:
    """Architect role: structure and design."""
    issues: list[Issue] = []
    classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

    if len(classes) > MAX_CLASSES_PER_FILE:
        issues.append(
            Issue(
                "architect",
                str(file),
                1,
                f"Too many classes in file: {len(classes)} > {MAX_CLASSES_PER_FILE}",
            )
        )

    for cls in classes:
        methods = [
            n for n in cls.body if isinstance(n, ast.FunctionDef | ast.AsyncFunctionDef)
        ]
        if len(methods) > MAX_CLASS_METHODS:
            issues.append(
                Issue(
                    "architect",
                    str(file),
                    cls.lineno,
                    f"Class '{cls.name}' has too many methods: {len(methods)} > "
                    f"{MAX_CLASS_METHODS}",
                )
            )

    imports = [n for n in ast.walk(tree) if isinstance(n, ast.Import | ast.ImportFrom)]
    if len(imports) > MAX_IMPORTS:
        issues.append(
            Issue(
                "architect",
                str(file),
                1,
                f"Too many imports: {len(imports)} > {MAX_IMPORTS} \u2014 consider "
                f"splitting",
            )
        )

    # Check for OpenAPI spec in packages with API routes
    has_api_routes = any(
        "router" in line.lower() or "@app." in line or "APIRouter" in line
        for line in file.read_text(encoding="utf-8").splitlines()
    )
    if has_api_routes:
        package_root = file.parent
        while package_root.name != "packages" and package_root != package_root.parent:
            if (package_root / "pyproject.toml").exists():
                break
            package_root = package_root.parent

        openapi_exists = (
            (package_root / "openapi.yaml").exists()
            or (package_root / "openapi.json").exists()
            or (package_root / "openapi.yml").exists()
        )
        if not openapi_exists and package_root.name != "packages":
            issues.append(
                Issue(
                    "architect",
                    str(file),
                    1,
                    "API routes found but no openapi.yaml/json — architecture error",
                )
            )

    return issues


ROLES: dict[str, Callable[[Path, ast.AST, list[str]], list[Issue]]] = {
    "dev": check_dev,
    "tester": check_tester,
    "reviewer": check_reviewer,
    "best_practice": check_best_practice,
    "architect": check_architect,
}

ROLE_ICONS: dict[str, str] = {
    "dev": "👨‍💻",
    "tester": "🧪",
    "reviewer": "👀",
    "best_practice": "✨",
    "architect": "🏗️",
}


def main() -> int:
    """Run all role checks on staged files."""
    files = get_changed_files()
    if not files:
        return 0

    all_issues: list[Issue] = []

    for file in files:
        if not file.exists():
            continue

        content = file.read_text(encoding="utf-8")
        lines = content.splitlines()

        try:
            tree = ast.parse(content)
        except SyntaxError:
            continue

        for check_func in ROLES.values():
            all_issues.extend(check_func(file, tree, lines))

    if all_issues:
        print("\n❌ Role Review Issues:\n")
        for issue in sorted(all_issues, key=lambda x: (x.role, x.file, x.line)):
            icon = ROLE_ICONS.get(issue.role, "•")
            print(f"  {icon} [{issue.role}] {issue.file}:{issue.line}")
            print(f"      {issue.message}\n")
        print(f"Total: {len(all_issues)} issue(s)\n")
        return 1

    print("✅ All role checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
