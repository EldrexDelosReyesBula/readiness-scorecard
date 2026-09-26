# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-09-26

### Added
- AST detector `checks/missing_timeout.py` (`MissingTimeoutCheck`) for external HTTP calls (`requests.*`, `httpx.*`) missing the `timeout` parameter (`TIME001`).
- Registered `MissingTimeoutCheck` in `checks/__init__.py`.
- Day 1 evidence screenshots and session logs in `evidence/day1/`.

## [0.1.0] - 2026-09-25

### Added
- Core CLI entrypoint (`main.py`) with `argparse`, target path argument, and `--threshold` flag.
- AST-based check engine in `checks/missing_error_handling.py` detecting unprotected network calls (`requests.*`, `httpx.*`, `urllib.request.*`) and file I/O (`open()`).
- File discovery engine (`scanner.py`) with noise directory filtering (`.venv`, `__pycache__`, `.git`, `node_modules`).
- Deterministic weighted scoring algorithm (`scorer.py`) with risk penalty deduction and pass/fail thresholds.
- Terminal visualization engine (`reporter.py`) built with `rich` and hardened for Windows `cp1252` encoding.
- Operational Agent guidelines and architectural manifesto (`AGENTS.md`).
- Validation test cases (`evidence/sample_bad.py` and `evidence/sample_good.py`).
- Complete documentation (`README.md`) with problem statement, quickstart, demo walkthrough, and IBM Bob 2.0 attribution.
