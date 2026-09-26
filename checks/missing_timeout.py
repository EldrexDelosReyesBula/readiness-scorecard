"""
checks/missing_timeout.py — AST detector for HTTP calls missing a `timeout` argument.

Detection strategy:
  - Walk every Call node in the AST.
  - Match attribute-style calls on `requests` or `httpx` modules:
      requests.get / requests.post / requests.put / requests.delete /
      requests.patch / requests.request / requests.head / requests.options
      httpx.get / httpx.post / httpx.put / httpx.delete /
      httpx.patch / httpx.request / httpx.head / httpx.options
  - If the call does NOT include a `timeout` keyword argument, emit TIME001.
  - Protected-by-try-except is irrelevant here — a missing timeout hangs the
    thread regardless of error handling.

Severity: warning  (per AGENTS.md §6 — missing timeouts)
"""

import ast
from typing import List, Optional, Tuple

from checks.base import CheckIssue

# ---------------------------------------------------------------------------
# Modules and their HTTP-calling method names to inspect.
# ---------------------------------------------------------------------------
_HTTP_MODULES = {"requests", "httpx"}

_HTTP_METHODS = {
    "get", "post", "put", "delete", "patch",
    "request", "head", "options",
}


def _classify_http_call(node: ast.Call) -> Optional[str]:
    """
    Return a human-readable label (e.g. ``requests.get()``) if *node* is an
    HTTP call that should carry a ``timeout`` argument, else ``None``.
    """
    func = node.func

    # Only handle attribute-style calls: module.method(...)
    if not isinstance(func, ast.Attribute):
        return None

    # The receiver must be a plain Name node (e.g. `requests` or `httpx`).
    if not isinstance(func.value, ast.Name):
        return None

    module = func.value.id
    method = func.attr

    if module in _HTTP_MODULES and method in _HTTP_METHODS:
        return f"{module}.{method}()"

    return None


def _has_timeout_kwarg(node: ast.Call) -> bool:
    """Return True if *node* has an explicit ``timeout`` keyword argument."""
    return any(kw.arg == "timeout" for kw in node.keywords)


class MissingTimeoutCheck:
    """
    Detects HTTP calls that omit the ``timeout`` keyword argument.

    Usage:
        issues = MissingTimeoutCheck().run(file_path, source_code)
    """

    CHECK_NAME = "Missing Network Timeout"
    CATEGORY   = "Reliability"

    def run(self, file_path: str, source: str) -> List[CheckIssue]:
        """
        Parse *source* and return a CheckIssue for every HTTP call that lacks
        an explicit ``timeout`` argument.

        On SyntaxError, returns a single warning-level issue rather than
        crashing (per AGENTS.md §7.5).
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

        issues: List[CheckIssue] = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            label = _classify_http_call(node)
            if label is None:
                continue

            if _has_timeout_kwarg(node):
                continue

            issues.append(
                CheckIssue(
                    check_id="TIME001",
                    check_name=self.CHECK_NAME,
                    category=self.CATEGORY,
                    severity="warning",
                    file_path=file_path,
                    line_number=getattr(node, "lineno", 0),
                    message=(
                        f"Network call to `{label}` does not specify a "
                        "`timeout` parameter."
                    ),
                    suggested_fix=(
                        f"Add an explicit timeout (e.g., `{label[:-2]}(..., timeout=10)`) "
                        "to prevent thread hangs in production."
                    ),
                )
            )

        return issues
