# 🤖 AGENTS.md — Production Readiness Scorecard

> **Operational Guidelines & Architecture Manifesto for IBM Bob 2.0 & AI Coding Agents**  
> *Project: Production Readiness Scorecard (CLI)*  
> *Target Hackathon: IBM Bob 2.0 Hackathon on lablab.ai*

---

## 1. Project Mission & North Star

**Core Motto:** *"AI helps you write code fast — this tool tells you when it's actually safe to ship."*

### The Problem
Developers using AI coding assistants quickly reach ~80% implementation completion, but the final 20%—comprising unhandled edge cases, missing error boundaries, lack of network timeouts, and resource leaks—frequently leads to production incidents, failed reviews, and costly rework.

### The Solution
A fast, standalone Python CLI tool that parses source code into an Abstract Syntax Tree (AST), executes deterministic readiness checks, and computes an actionable 0–100% Production Readiness Score with exact file and line pointers for remediation.

---

## 2. Agent Persona & Role Directives

When interacting with this codebase as IBM Bob 2.0 or pair-programming agents:
1. **Act as a Principal Developer Tooling Engineer:** Write clean, modular, resilient, and standard-library-first Python code.
2. **Enforce the 48-Hour Hackathon Discipline:** Reject scope creep immediately. Do not propose Web UIs, databases, multi-language transpilation, or complex microservices.
3. **Prioritize the Demo Experience:** Every feature, log message, and terminal printout must enhance the 2–3 minute submission demo (clear before/after contrast: e.g., 62% $\rightarrow$ 85%+).
4. **Document Decisions for Evidence:** Explain the AST traversal logic and algorithm design concisely so that session logs provide undeniable judging evidence of thoughtful human-agent collaboration.

---

## 3. Technology Stack & Constraints

| Dimension | Chosen Standard | Rationale |
| :--- | :--- | :--- |
| **Language** | **Python 3.10+** | Native AST inspection (`ast`), rapid development, universal accessibility. |
| **Parsing Engine** | **Standard Library `ast`** | Zero external dependencies for parsing, deterministic, robust against code variations. |
| **CLI Framework** | **Standard Library `argparse`** | Lightweight, zero-overhead argument parsing. |
| **Terminal UI** | **`rich`** | Beautiful, color-coded tables, status panels, and score bars for high demo impact. |
| **File Traversal** | **`pathlib` / `os.walk`** | Fast directory traversal with automatic exclusion of hidden/virtualenv dirs. |
| **Dependencies** | Minimal (`rich` in `requirements.txt`) | Quick installation, minimal attack surface, rapid test runs. |

---

## 4. Architectural Blueprint

```
readiness-scorecard/
├── AGENTS.md                         # This file: AI agent conventions & architecture
├── README.md                         # Public repository overview & quickstart
├── requirements.txt                  # Minimal dependencies: rich
├── main.py                           # CLI entry point, argument parsing, orchestration
├── scanner.py                        # Path walker & Python file discovery
├── scorer.py                         # Weighted scoring engine & gap aggregator
├── reporter.py                       # Rich-based terminal visualizer
└── checks/                           # Extensible check catalog
    ├── __init__.py                   # Check registry & base interface
    ├── base.py                       # Abstract base class / dataclass definitions
    └── missing_error_handling.py     # AST detector for naked external/I/O calls
```

### High-Level Data Flow
1. **Input:** User executes `python main.py <target_path> [--threshold 85]`.
2. **Scan:** `scanner.py` resolves paths, filtering out `.venv`, `__pycache__`, `.git`, and non-Python files.
3. **Parse & Check:** `checks/` runs AST visitors over scanned files, yielding structured `CheckIssue` objects.
4. **Score:** `scorer.py` evaluates issues against weighted penalties and clamps the result to $[0, 100]$.
5. **Report:** `reporter.py` renders color-coded terminal cards, category breakdown, blockers, and remediation steps.
6. **Exit Code:** Returns `0` if score $\ge$ threshold, `1` if below threshold or critical blockers detected.

---

## 5. Core Data Contracts

Agents must strictly adhere to these shared data contracts:

```python
from dataclasses import dataclass
from typing import List, Literal, Optional

SeverityLevel = Literal["info", "warning", "critical"]

@dataclass
class CheckIssue:
    check_id: str             # e.g., "ERR001"
    check_name: str           # e.g., "Missing Error Handling"
    category: str             # e.g., "Reliability"
    severity: SeverityLevel   # "info" | "warning" | "critical"
    file_path: str            # Relative path to file
    line_number: int          # 1-indexed source line
    message: str              # Actionable issue description
    suggested_fix: str        # Brief recommendation for developer

@dataclass
class ScoreResult:
    total_score: int          # Clamped between 0 and 100
    threshold: int            # Configured target (default: 85)
    passed: bool              # total_score >= threshold and critical == 0
    issues: List[CheckIssue]
    counts: dict              # {"critical": int, "warning": int, "info": int}
    remediation_summary: List[str]
```

---

## 6. Scoring Formula Specification

The scoring engine must be predictable, transparent, and encourage immediate developer action:

$$\text{Raw Score} = 100 - (\text{critical\_count} \times 15) - (\text{warning\_count} \times 5) - (\text{info\_count} \times 1)$$

$$\text{Final Score} = \max(0, \min(100, \text{Raw Score}))$$

* **Critical Failures ($\mathbf{-15}$ pts each):** Unprotected network/API calls (`requests.*`, `urllib.*`, `httpx.*`), naked unhandled database operations, or bare file write locks.
* **Warnings ($\mathbf{-5}$ pts each):** Unhandled generic file I/O (`open()`), broad `except:` without specification, or missing timeouts.
* **Info ($\mathbf{-1}$ pt each):** Debug statements left in production paths or missing function docstrings.

---

## 7. AST Detection Rules (MVP Check: Error Handling)

When inspecting code in `checks/missing_error_handling.py`:
1. Use `ast.NodeVisitor` or `ast.walk` to inspect function definitions.
2. Identify dangerous operations:
   - Network calls: `requests.get`, `requests.post`, `httpx.*`, `urllib.request.*`
   - File I/O: `open()`
3. Verify whether each call is wrapped in a `Try` node containing appropriate `ExceptHandler` blocks.
4. Flag any dangerous call not enclosed within a `try...except` block with line number and offending function signature.
5. Gracefully catch `SyntaxError` or file decoding issues in the target repository—record them as warnings rather than crashing the tool.

---

## 8. Anti-Bloat & Over-Engineering Restrictions

Agents must **NEVER**:
- Propose or generate a Web UI, React/Vue front-end, or Electron shell.
- Add database drivers (SQLite, PostgreSQL, MongoDB, Redis).
- Introduce multi-language support (JavaScript/Go) during the 48-hour window.
- Add external cloud API calls or AI LLM calls during the scan (the tool must operate 100% locally and instantaneously).
- Propose continuous deployment pipelines or heavy Docker containers for the MVP demo.

---

## 9. Git & Evidence Discipline

- **Atomic Commits:** Follow conventional commits (`feat:`, `fix:`, `chore:`, `docs:`).
- **Session Summaries:** After completing each major architectural block, output a clear summary for easy screenshot capture for the hackathon judging portal.
- **Evidence Storage:** Save all relevant session artifacts and screenshots into `evidence/day0/`, `evidence/day1/`, or `evidence/day2/`.
