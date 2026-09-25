# 🎯 Production Readiness Scorecard

## 1. Purpose

**One sentence:** AI helps you write code fast — this tool tells you when it's actually safe to ship.

**Why it exists:** AI coding tools get developers to 80% completion quickly, but the last 20% (error handling, security, edge cases, integration safety) is where projects stall. There's no fast, automated way to know if a branch is _production-ready_ before merging.

---

## 2. Problem Statement

**Current state:**

- Developer finishes a feature with AI assistance
- They _think_ it's done because the code runs locally
- They merge, deploy, and discover missing error handling, no timeouts, untested auth paths, etc.
- Rework costs hours or days

**Root cause:** No standardized "readiness check" exists between "code works on my machine" and "safe for production."

**Impact:** Wasted time, production incidents, eroded trust in AI-assisted development.

---

## 3. Solution Overview

A tool that:

1. Takes a **branch or PR** as input
2. Runs a set of **readiness checks** against the code
3. Produces a **Production Readiness Score** (0–100%) with specific, actionable gaps
4. Shows exactly what to fix to raise the score

**Output example:**

```
Production Readiness: 62%

✅ Tests pass
✅ No syntax errors
⚠️ Missing error handling in 3 API calls
⚠️ No timeout on external HTTP request
❌ Auth change has no test for expired tokens
❌ New dependency has known CVE

Fix these 3 items to reach 85%.
```

---

## 4. Scope (Solo, 48 Hours)

### ✅ In Scope (MVP)

- **One check category done extremely well:** Missing error handling detection
- CLI tool: `readiness check <branch-or-path>`
- Score calculation (simple weighted formula)
- Terminal output with color-coded results
- Screenshot of Bob session summaries for submission

### ⏳ Stretch (If Time Allows)

- Second category: Missing timeouts on external calls
- Simple HTML report instead of terminal output

### ❌ Out of Scope (Do NOT Build)

- Web UI
- User accounts / auth
- Multi-language support (pick ONE language — Python or JavaScript)
- CI/CD integration
- Historical tracking / database

**Rule:** If it's not in the MVP, it doesn't exist for 48 hours.

---

## 5. Architecture (EA)

### High-Level Flow

```
[Input: Branch/Path]
        ↓
[File Scanner] → identifies relevant files (.py or .js)
        ↓
[Check Engine] → runs readiness checks
        ↓
[Scorer] → calculates weighted score
        ↓
[Reporter] → outputs terminal report
```

### Component Breakdown

| Component         | Responsibility                             | Tech                                  |
| ----------------- | ------------------------------------------ | ------------------------------------- |
| **Input Handler** | Accept branch name or path                 | Python `argparse` or Node `commander` |
| **File Scanner**  | Find files to analyze, filter by extension | `os.walk` / `glob`                    |
| **Check Engine**  | Run individual readiness checks            | Python functions                      |
| **Scorer**        | Aggregate check results into 0–100 score   | Simple weighted formula               |
| **Reporter**      | Format and print results                   | `rich` (Python) or `chalk` (Node)     |

### Data Model

```
Check {
  id: string
  name: string
  category: string
  severity: "info" | "warning" | "critical"
  passed: boolean
  details: string
  file: string
  line: number
}

Score {
  total: number (0-100)
  by_category: { [category]: number }
  checks: Check[]
  blockers: Check[]  // critical failures
}
```

### EA Considerations

- **Modularity:** Each check is a standalone function. Adding a check = adding a function.
- **Extensibility:** Check registry pattern — new checks register themselves.
- **No external services:** Everything runs locally. No API keys needed (except Bob for development).
- **Stateless:** Run it, get output, done. No database.

---

## 6. BPM (Business Process Model)

### The Workflow This Tool Fits Into

```
[Developer writes code with AI]
        ↓
[Developer thinks "it's done"]
        ↓
[NEW: Run Readiness Scorecard] ←──────┐
        ↓                              │
[Score ≥ 85%?]                         │
   ↓ Yes          ↓ No                 │
[Merge/PR]    [Fix flagged items] ─────┘
```

### Process Steps

| Step | Actor     | Action                          | Output                        |
| ---- | --------- | ------------------------------- | ----------------------------- |
| 1    | Developer | Finishes feature branch         | Code ready for check          |
| 2    | Developer | Runs `readiness check`          | Invokes tool                  |
| 3    | Tool      | Scans files                     | List of files to analyze      |
| 4    | Tool      | Runs checks                     | Raw check results             |
| 5    | Tool      | Calculates score                | 0–100 score + blockers        |
| 6    | Tool      | Reports                         | Terminal output               |
| 7    | Developer | Reviews output                  | Decision: fix or merge        |
| 8a   | Developer | If score < threshold: fix items | Updated code → back to step 2 |
| 8b   | Developer | If score ≥ threshold: merge     | Done                          |

### BPM Metrics

- **Cycle time:** How long from "code done" to "merged"
- **Rework rate:** How often items are flagged post-merge
- **Target:** Reduce rework by catching issues pre-merge

---

## 7. Data Management

### Input Data

- Source code files (`.py` or `.js`)
- Configuration: threshold, enabled checks

### Processing Data

- Parsed AST (Abstract Syntax Tree) for code analysis
- Check results (pass/fail + details)

### Output Data

- Score (JSON for programmatic use, formatted text for humans)
- Report file (optional: `readiness-report.json`)

### Data Rules

- **No PII.** No user data. Only code.
- **No persistence required for MVP.** Generate report, print it, exit.
- **Optional:** Write `readiness-report.json` to disk for evidence in submission.

### Storage

- None for MVP. If stretch: write JSON report to project root.

---

## 8. Discipline Rules (For You, Solo)

These are non-negotiable for 48 hours:

1. **One language only.** Pick Python OR JavaScript. Do not switch.
2. **One check category first.** Error handling detection. Ship it. Then add more.
3. **No refactoring until the core works.** Ugly code that runs beats pretty code that doesn't.
4. **Commit every 90 minutes.** Even if broken. Git history is evidence for submission.
5. **Screenshot Bob sessions as you go.** Required for submission. Don't wait until the end.
6. **Timebox each phase:**
   - Hour 0–2: Setup, file scanner, basic CLI
   - Hour 2–6: Error handling check working
   - Hour 6–8: Scorer + reporter
   - Hour 8–10: Polish, test on real repo
   - Hour 10–12: Record demo video, write submission
7. **Stop adding features at Hour 40.** Last 8 hours = demo prep only.
8. **Sleep.** A tired solo dev makes bad decisions. 6 hours minimum.

---

## 9. Bob 2.0 Integration Plan

| Phase            | How Bob Helps                               | Mode        |
| ---------------- | ------------------------------------------- | ----------- |
| **Setup**        | Generate project scaffolding, CLI structure | Agent       |
| **File Scanner** | Write file walking + filtering logic        | Agent       |
| **Check Engine** | Write AST-based error handling detector     | Agent + Ask |
| **Scorer**       | Write weighted scoring logic                | Agent       |
| **Reporter**     | Write terminal output formatting            | Agent       |
| **Testing**      | Generate test cases for the tool itself     | Agent       |
| **Debugging**    | Explain failures, suggest fixes             | Ask         |
| **Docs**         | Generate README from code                   | Ask         |

**Key move:** Create an `agents.md` file at project root describing your conventions. This "onboards" Bob and shows judges you used it strategically, not just as autocomplete.
