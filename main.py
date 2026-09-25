"""
main.py — CLI entry point for the Production Readiness Scorecard.

Usage:
    python main.py <target_path> [--threshold 85]

Exit codes:
    0 — score >= threshold and no critical issues
    1 — score below threshold or critical issues detected
"""

import argparse
import sys

from rich.console import Console

console = Console()

VERSION = "0.1.0"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scorecard",
        description="Production Readiness Scorecard -- AI-assisted code ships faster; this tool tells you when it's safe.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="Path to a Python file or directory to scan.",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=85,
        metavar="N",
        help="Minimum passing score [0-100] (default: 85).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"Readiness Scorecard v{VERSION}",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    console.print(f"[bold blue]Readiness Scorecard v{VERSION}[/bold blue]")

    if args.target is None:
        console.print(
            "[yellow]No target specified. Run with a path to scan:[/yellow]\n"
            f"  python main.py <target_path> [--threshold {args.threshold}]"
        )
        return 0

    # --- Imports are deferred here so `python main.py` (no target) is instant ---
    from scanner import discover_files
    from checks import ALL_CHECKS
    from scorer import compute_score
    from reporter import render_report

    # 1. Discover files
    try:
        py_files = list(discover_files(args.target))
    except FileNotFoundError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return 1

    if not py_files:
        console.print("[yellow]No Python files found in the specified target.[/yellow]")
        return 0

    console.print(f"Scanning [cyan]{len(py_files)}[/cyan] file(s) in [cyan]{args.target}[/cyan]...")

    # 2. Run checks
    all_issues = []
    for py_file in py_files:
        try:
            source = py_file.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            console.print(f"[yellow]Warning:[/yellow] Could not read {py_file}: {exc}")
            continue

        relative = str(py_file)
        for check in ALL_CHECKS:
            all_issues.extend(check.run(relative, source))

    # 3. Score
    result = compute_score(all_issues, threshold=args.threshold)

    # 4. Report
    render_report(result)

    # 5. Exit code
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
