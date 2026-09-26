"""
checks/__init__.py — Check registry for the Production Readiness Scorecard.

To register a new check, import its class and append it to ALL_CHECKS.
Each check must expose a `run(file_path: str, source: str) -> List[CheckIssue]` method.
"""

from checks.missing_error_handling import MissingErrorHandlingCheck
from checks.missing_timeout import MissingTimeoutCheck

# Central registry — scanner iterates over this list for every Python file.
ALL_CHECKS = [
    MissingErrorHandlingCheck(),
    MissingTimeoutCheck(),
]
