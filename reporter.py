"""
reporter.py — Rich-based terminal visualizer for the Production Readiness Scorecard.

Renders:
  - Header panel with tool name and version
  - Score bar (color-coded green / yellow / red)
  - Issue table grouped by severity
  - Remediation summary panel
  - Final pass / fail banner
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text

from checks.base import ScoreResult

console = Console()

# Score thresholds for colour coding
_GREEN_FLOOR  = 85
_YELLOW_FLOOR = 60


def _score_color(score: int) -> str:
    if score >= _GREEN_FLOOR:
        return "bold green"
    if score >= _YELLOW_FLOOR:
        return "bold yellow"
    return "bold red"


def _severity_color(severity: str) -> str:
    return {"critical": "red", "warning": "yellow", "info": "cyan"}.get(severity, "white")


def render_report(result: ScoreResult) -> None:
    """Print the full scorecard report to the terminal."""
    _render_score_panel(result)
    if result.issues:
        _render_issue_table(result)
    _render_remediation_panel(result)
    _render_verdict_banner(result)


def _render_score_panel(result: ScoreResult) -> None:
    color = _score_color(result.total_score)
    score_text = Text(f"{result.total_score}/100", style=color)
    threshold_text = Text(f"  (threshold: {result.threshold})", style="dim")
    combined = score_text + threshold_text

    counts = result.counts
    detail = (
        f"[red]Critical: {counts['critical']}[/red]  "
        f"[yellow]Warnings: {counts['warning']}[/yellow]  "
        f"[cyan]Info: {counts['info']}[/cyan]"
    )

    console.print()
    console.print(
        Panel(
            f"[bold]Production Readiness Score:[/bold] {combined.markup}\n{detail}",
            title="[bold blue]Production Readiness Scorecard v0.1.0[/bold blue]",
            border_style="blue",
        )
    )


def _render_issue_table(result: ScoreResult) -> None:
    table = Table(
        title="Issues Found",
        box=box.ROUNDED,
        show_lines=True,
        highlight=True,
    )
    table.add_column("ID",       style="dim",    no_wrap=True)
    table.add_column("Severity", no_wrap=True)
    table.add_column("File",     style="cyan",   no_wrap=False)
    table.add_column("Line",     style="magenta", no_wrap=True, justify="right")
    table.add_column("Message",  no_wrap=False)
    table.add_column("Fix",      style="green",  no_wrap=False)

    # Sort: critical first, then warning, then info
    severity_order = {"critical": 0, "warning": 1, "info": 2}
    sorted_issues = sorted(result.issues, key=lambda i: severity_order.get(i.severity, 9))

    for issue in sorted_issues:
        sev_color = _severity_color(issue.severity)
        table.add_row(
            issue.check_id,
            f"[{sev_color}]{issue.severity.upper()}[/{sev_color}]",
            issue.file_path,
            str(issue.line_number),
            issue.message,
            issue.suggested_fix,
        )

    console.print()
    console.print(table)


def _render_remediation_panel(result: ScoreResult) -> None:
    lines = "\n".join(f"  * {item}" for item in result.remediation_summary)
    console.print()
    console.print(
        Panel(lines, title="[bold yellow]Remediation Steps[/bold yellow]", border_style="yellow")
    )


def _render_verdict_banner(result: ScoreResult) -> None:
    console.print()
    if result.passed:
        console.print(
            Panel(
                "[bold green]PASSED -- Codebase meets the production readiness threshold.[/bold green]",
                border_style="green",
            )
        )
    else:
        console.print(
            Panel(
                "[bold red]FAILED -- Score is below threshold or critical issues remain.[/bold red]",
                border_style="red",
            )
        )
    console.print()
