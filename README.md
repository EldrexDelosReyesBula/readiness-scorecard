# 🛡️ Production Readiness Scorecard (CLI)

> **"AI helps you write code fast — this tool tells you when it's actually safe to ship."**  
> *Built for the **IBM Bob 2.0 Hackathon** on lablab.ai*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Built with](https://img.shields.io/badge/AI%20Pair--Programmer-IBM%20Bob%202.0-8A2BE2.svg)](https://bob.ibm.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 The Problem: The "Last-Mile" AI Coding Gap

AI coding assistants enable developers to reach 80% feature completion in record time. However, the remaining **20%** is where software engineering failures happen:
* Unprotected network calls without error boundaries
* Naked file and socket I/O operations
* Missing timeouts on external HTTP requests
* Crashes under intermittent connectivity

Developers frequently push code that "works on my machine," only to trigger production incidents, broken merges, and costly rework.

## 💡 The Solution

**Production Readiness Scorecard** is a lightweight, zero-dependency AST (Abstract Syntax Tree) scanner and CLI scoring engine. It inspects Python source code deterministically, evaluates production readiness against rigorous reliability checks, and computes a **0–100% Production Readiness Score** with exact file and line pointers for immediate remediation.

---

## ⚡ Quickstart

### Prerequisites
* Python 3.10 or higher

### Installation
```bash
git clone https://github.com/EldrexDelosReyesBula/readiness-scorecard.git
cd readiness-scorecard
pip install -r requirements.txt
```

### Run the Scorecard
Scan any Python repository, directory, or individual file:

```bash
# Scan a directory against the default 85% readiness threshold
python main.py ./my-project

# Scan with a custom threshold
python main.py ./my-project --threshold 90

# Scan a single file
python main.py ./my-project/api.py
```

### Exit Codes for CI/CD Gating
* **`0`**: Score meets or exceeds threshold and zero critical blockers exist.
* **`1`**: Score is below threshold or critical blockers were detected.

---

## 🧪 Live Demo: Before vs. After Remediation

### 1. Before (Unprotected Code)
Scanning an unhandled API integration script (`evidence/sample_bad.py`):
```bash
python main.py evidence/sample_bad.py
```
```text
Readiness Scorecard v0.1.0
Scanning 1 file(s) in evidence/sample_bad.py...

+-------------------- Production Readiness Scorecard v0.1.0 --------------------+
| Production Readiness Score: 75/100  (threshold: 85)                           |
| Critical: 1  Warnings: 2  Info: 0                                             |
+-------------------------------------------------------------------------------+

                                 Issues Found
+-------------------------------------------------------------------------------+
| ID      | Severity | File              | Line | Message         | Fix          |
|---------+----------+-------------------+------+-----------------+--------------|
| ERR001  | CRITICAL | .../sample_bad.py |    5 | Unprotected     | Wrap call in |
|         |          |                   |      | requests.get()  | try/except   |
| ERR002  | WARNING  | .../sample_bad.py |   10 | Unprotected     | Wrap call in |
|         |          |                   |      | open()          | try/except   |
| TIME001 | WARNING  | .../sample_bad.py |    5 | Missing timeout | Add explicit |
|         |          |                   |      | in requests.get | timeout=10   |
+-------------------------------------------------------------------------------+

+----------------------------- Remediation Steps -------------------------------+
|   * Fix 1 critical issue(s): wrap network/API calls in try/except.            |
|   * Address 2 warning(s): protect file I/O and narrow broad except clauses.   |
+-------------------------------------------------------------------------------+

+-------------------------------------------------------------------------------+
| FAILED -- Score is below threshold or critical issues remain.                 |
+-------------------------------------------------------------------------------+
```

### 2. After (Remediated Code)
After wrapping external calls in appropriate `try...except` exception handlers:
```bash
python main.py evidence/sample_good.py
```
```text
Readiness Scorecard v0.1.0
Scanning 1 file(s) in evidence/sample_good.py...

+-------------------- Production Readiness Scorecard v0.1.0 --------------------+
| Production Readiness Score: 100/100  (threshold: 85)                          |
| Critical: 0  Warnings: 0  Info: 0                                             |
+-------------------------------------------------------------------------------+

+----------------------------- Remediation Steps -------------------------------+
|   * No issues detected -- codebase looks production-ready!                    |
+-------------------------------------------------------------------------------+

+-------------------------------------------------------------------------------+
| PASSED -- Codebase meets the production readiness threshold.                  |
+-------------------------------------------------------------------------------+
```

---

## 🧮 Transparent Scoring Formula

The scorecard uses an explainable penalty formula based on production risk:

$$\text{Raw Score} = 100 - (\text{critical} \times 15) - (\text{warning} \times 5) - (\text{info} \times 1)$$

$$\text{Final Score} = \max(0, \min(100, \text{Raw Score}))$$

| Severity | Penalty | Target Operations |
| :--- | :---: | :--- |
| **Critical** | **-15 pts** | Naked network/API calls (`requests.*`, `httpx.*`, `urllib.request.*`) |
| **Warning** | **-5 pts** | Missing network timeouts (`timeout=...`), unprotected file I/O (`open()`), broad `except:`, syntax warnings |
| **Info** | **-1 pt** | Debug prints left in production code paths, missing docstrings |

---

## 🏗️ Architecture

```
[Target Path] ──> [File Scanner] ──> [AST Check Engine] ──> [Scorer] ──> [Rich Terminal UI]
```

* **`main.py`**: CLI entry point with `argparse`, input validation, and exit code management.
* **`scanner.py`**: Fast directory walker with noise exclusion (`.venv`, `__pycache__`, `.git`, `node_modules`).
* **`checks/base.py`**: Shared dataclasses (`CheckIssue`, `ScoreResult`, `SeverityLevel`).
* **`checks/missing_error_handling.py`**: AST visitor analyzing function bodies and enclosing `Try`/`ExceptHandler` blocks (`ERR001`, `ERR002`).
* **`checks/missing_timeout.py`**: AST visitor verifying explicit `timeout` keyword parameters on HTTP calls (`TIME001`).
* **`scorer.py`**: Deterministic weighted scoring calculator and remediation synthesizer.
* **`reporter.py`**: Terminal visualizer formatted with `rich`, featuring Windows `cp1252` encoding safety.

---

## 🤖 Built With IBM Bob 2.0

This project was built during the **IBM Bob 2.0 Hackathon** on lablab.ai using **IBM Bob Shell 2.0.5** as an active pair-programming engineer.

* **Agent Onboarding via `AGENTS.md`**: Architectural guidelines and strict data contracts were codified in [`AGENTS.md`](AGENTS.md) to steer Bob's generation.
* **Autonomous Scaffolding & Verification**: Bob generated the modular check pipeline, resolved Windows console character-set incompatibilities in real-time, and validated dual execution paths (exit code 0 / 1).
* **Audit Trail**: Full task session logs and execution traces are archived in [`evidence/`](evidence/).

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
