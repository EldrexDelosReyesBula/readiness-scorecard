"""
scorer.py — Weighted scoring engine for the Production Readiness Scorecard.

Scoring formula (per AGENTS.md §6):
  Raw Score  = 100 - (critical × 15) - (warning × 5) - (info × 1)
  Final Score = max(0, min(100, Raw Score))

Pass condition: total_score >= threshold AND critical_count == 0
"""

from typing import List

from checks.base import CheckIssue, ScoreResult

# Penalty weights by severity
_PENALTIES: dict = {
    "critical": 15,
    "warning":   5,
    "info":      1,
}


def compute_score(issues: List[CheckIssue], threshold: int = 85) -> ScoreResult:
    """
    Compute a ScoreResult from a flat list of CheckIssue objects.

    Args:
        issues:    All findings collected across every scanned file.
        threshold: Minimum acceptable score (default 85, per AGENTS.md §4).

    Returns:
        ScoreResult with total_score, passed flag, counts, and remediation_summary.
    """
    counts = {"critical": 0, "warning": 0, "info": 0}
    for issue in issues:
        counts[issue.severity] += 1

    raw = (
        100
        - counts["critical"] * _PENALTIES["critical"]
        - counts["warning"]  * _PENALTIES["warning"]
        - counts["info"]     * _PENALTIES["info"]
    )
    total_score = max(0, min(100, raw))
    passed = total_score >= threshold and counts["critical"] == 0

    remediation_summary = _build_remediation_summary(issues, counts)

    return ScoreResult(
        total_score=total_score,
        threshold=threshold,
        passed=passed,
        issues=issues,
        counts=counts,
        remediation_summary=remediation_summary,
    )


def _build_remediation_summary(issues: List[CheckIssue], counts: dict) -> List[str]:
    """Return a short prioritised action list for the report header."""
    summary: List[str] = []

    if counts["critical"] > 0:
        summary.append(
            f"Fix {counts['critical']} critical issue(s): wrap network/API calls in try/except."
        )
    if counts["warning"] > 0:
        summary.append(
            f"Address {counts['warning']} warning(s): protect file I/O and narrow broad except clauses."
        )
    if counts["info"] > 0:
        summary.append(
            f"Clean up {counts['info']} info item(s): remove debug statements, add docstrings."
        )
    if not summary:
        summary.append("No issues detected -- codebase looks production-ready!")

    return summary
