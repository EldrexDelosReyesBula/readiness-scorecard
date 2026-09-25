"""
checks/missing_error_handling.py — AST detector for unprotected I/O and network calls.

Detection strategy (per AGENTS.md §7):
  - Walk every function body looking for Call nodes that match dangerous patterns.
  - A call is considered "protected" if it lives inside a Try node that has at least
    one ExceptHandler.
  - Unprotected calls are emitted as CheckIssue objects with the correct severity.

Severity mapping:
  critical  — network calls (requests.*, httpx.*, urllib.request.*)
  warning   — bare file I/O (open())
"""

import ast
from typing import List

from checks.base import CheckIssue, SeverityLevel

# ---------------------------------------------------------------------------
# Dangerous call signatures → (check_id, severity, label)
# ---------------------------------------------------------------------------
_NETWORK_MODULES = {"requests", "httpx"}
_NETWORK_URLLIB   = ("urllib", "request")   # urllib.request.*

_DANGEROUS_CALLS = {
    # (module, attr) tuples for attribute-style calls: requests.get(...)
}


def _classify_call(node: ast.Call):
    """
    Return (check_id, severity, label) if *node* is a dangerous call, else None.

    Handles:
      - requests.get / requests.post / requests.* / httpx.*
      - urllib.request.urlopen / urllib.request.*
      - open()
    """
    func = node.func

    # Attribute call: e.g. requests.get(...)
    if isinstance(func, ast.Attribute):
        # Two-level: module.attr
        if isinstance(func.value, ast.Name):
            module = func.value.id
            if module in _NETWORK_MODULES:
                return (
                    "ERR001",
                    "critical",
                    f"{module}.{func.attr}()",
                )

        # Three-level: urllib.request.urlopen(...)
        if isinstance(func.value, ast.Attribute):
            if (
                isinstance(func.value.value, ast.Name)
                and func.value.value.id == _NETWORK_URLLIB[0]
                and func.value.attr == _NETWORK_URLLIB[1]
            ):
                return (
                    "ERR001",
                    "critical",
                    f"urllib.request.{func.attr}()",
                )

    # Simple name call: open(...)
    if isinstance(func, ast.Name) and func.id == "open":
        return ("ERR002", "warning", "open()")

    return None


def _ancestor_try_nodes(node: ast.AST, parent_map: dict) -> List[ast.Try]:
    """Walk up the parent chain and collect all Try ancestor nodes."""
    ancestors = []
    current = parent_map.get(id(node))
    while current is not None:
        if isinstance(current, ast.Try):
            ancestors.append(current)
        current = parent_map.get(id(current))
    return ancestors


def _is_protected(call_node: ast.AST, parent_map: dict) -> bool:
    """Return True if *call_node* is enclosed in a try/except block."""
    for try_node in _ancestor_try_nodes(call_node, parent_map):
        if try_node.handlers:  # at least one ExceptHandler
            return True
    return False


def _build_parent_map(tree: ast.AST) -> dict:
    """Return a dict mapping id(child) → parent node for the whole AST."""
    parent_map = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parent_map[id(child)] = node
    return parent_map


class MissingErrorHandlingCheck:
    """
    Detects unprotected network and file I/O calls.

    Usage:
        issues = MissingErrorHandlingCheck().run(file_path, source_code)
    """

    CHECK_NAME = "Missing Error Handling"
    CATEGORY   = "Reliability"

    def run(self, file_path: str, source: str) -> List[CheckIssue]:
        """
        Parse *source* into an AST and return all unprotected dangerous calls.

        On SyntaxError or decode failure, returns a single warning-level issue
        rather than crashing (per AGENTS.md §7.5).
        """
        try:
            tree = ast.parse(source, filename=file_path)
        except SyntaxError as exc:
            return [
                CheckIssue(
                    check_id="PARSE001",
                    check_name="Parse Error",
                    category="Reliability",
                    severity="warning",
                    file_path=file_path,
                    line_number=exc.lineno or 0,
                    message=f"Could not parse file: {exc.msg}",
                    suggested_fix="Fix the syntax error before running the scorecard.",
                )
            ]

        parent_map = _build_parent_map(tree)
        issues: List[CheckIssue] = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            classification = _classify_call(node)
            if classification is None:
                continue

            check_id, severity, label = classification

            if _is_protected(node, parent_map):
                continue

            issues.append(
                CheckIssue(
                    check_id=check_id,
                    check_name=self.CHECK_NAME,
                    category=self.CATEGORY,
                    severity=severity,
                    file_path=file_path,
                    line_number=getattr(node, "lineno", 0),
                    message=f"Unprotected call to `{label}` -- not wrapped in try/except.",
                    suggested_fix=(
                        f"Wrap the `{label}` call in a try/except block and handle "
                        "network errors (e.g. ConnectionError, Timeout) explicitly."
                    ),
                )
            )

        return issues
