"""
checks/base.py — Core data contracts for the Production Readiness Scorecard.

All check implementations must produce CheckIssue instances.
ScoreResult is the final output consumed by reporter.py.
"""

from dataclasses import dataclass, field
from typing import List, Literal

# Severity taxonomy — drives penalty weights in scorer.py
SeverityLevel = Literal["info", "warning", "critical"]


@dataclass
class CheckIssue:
    """A single finding raised by an AST check pass."""

    check_id: str           # e.g. "ERR001"
    check_name: str         # e.g. "Missing Error Handling"
    category: str           # e.g. "Reliability"
    severity: SeverityLevel # "info" | "warning" | "critical"
    file_path: str          # Relative path to source file
    line_number: int        # 1-indexed source line
    message: str            # Actionable issue description
    suggested_fix: str      # Brief recommendation for the developer


@dataclass
class ScoreResult:
    """Aggregated scoring output produced by scorer.py."""

    total_score: int                            # Clamped to [0, 100]
    threshold: int                              # Configured target (default: 85)
    passed: bool                                # total_score >= threshold AND critical == 0
    issues: List[CheckIssue]                    # All findings across all files
    counts: dict                                # {"critical": int, "warning": int, "info": int}
    remediation_summary: List[str] = field(default_factory=list)  # Top action items
