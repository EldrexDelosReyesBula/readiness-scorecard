# 📅 Day-by-Day Iteration List

**Rule for the whole build:** If it doesn't make the demo better, it doesn't get built.

---

## 🌙 TONIGHT (Day 0) — Setup Only, 8:30 PM–11:00 PM

**Goal:** Repo exists. It runs. Nothing more.

### Checklist

- [ ] Create repo `readiness-scorecard`
- [ ] Pick language: **Python** (one language, no switching)
- [ ] Write `agents.md` with your conventions
- [ ] Ask agent: "Scaffold a Python CLI with `main.py`, `checks/`, `scorer.py`, `reporter.py`"
- [ ] Create `requirements.txt` with just: `rich`
- [ ] Run `python main.py` → prints "Readiness Scorecard v0.1"
- [ ] Commit: `"chore: initial scaffold"`
- [ ] Screenshot agent session

**Stop here. Sleep.** Do not start the file scanner tonight. Tired setup is fine; tired logic is not.

---

## 🗓️ DAY 1 — Core Working Tool (Saturday)

### Block 1: Morning (9:00 AM–12:00 PM)

**Goal:** Tool can find and list files.

- [ ] `scanner.py`: walk a path, return list of `.py` files
- [ ] `main.py`: accept path argument, print file count
- [ ] Test on a real folder (use any Python project on your machine)
- [ ] Commit: `"feat: file scanner"`
- [ ] Screenshot agent session

**Done when:** `python main.py ./some-project` prints "Found 12 Python files."

---

### Block 2: Afternoon (1:00 PM–5:00 PM)

**Goal:** One check works — missing error handling.

- [ ] `checks/missing_error_handling.py`
- [ ] Use Python `ast` to find `try/except` blocks
- [ ] Rule for MVP: flag any function that calls an external function (e.g., `requests.get`, `open()`, API calls) **without** a `try/except`
- [ ] Return a `Check` object per issue: `{file, line, severity, message}`
- [ ] `main.py`: run check, print raw results
- [ ] Test on real code — you should see _some_ flags
- [ ] Commit: `"feat: missing error handling check"`
- [ ] Screenshot agent session

**Done when:** `python main.py ./some-project` lists specific lines with issues.

**⚠️ Over-engineering trap:** Don't build 5 checks. Build **one**. Ship it. Add more only if Day 2 has spare time.

---

### Block 3: Evening (6:00 PM–9:00 PM)

**Goal:** Score + pretty output.

- [ ] `scorer.py`: simple formula
  ```
  score = 100 - (critical × 15) - (warning × 5)
  clamp to 0–100
  ```
- [ ] `reporter.py`: use `rich` to print:

  ```
  Production Readiness: 62%

  ✅ Tests pass (skip for MVP)
  ⚠️ Missing error handling: 3 issues
     - auth.py:42 - requests.post without try/except
     - api.py:18 - open() without try/except
  ```

- [ ] Color: red for critical, yellow for warning, green for pass
- [ ] Commit: `"feat: scorer and reporter"`
- [ ] Screenshot agent session

**Done when:** Running the tool gives a score and a readable list.

**End of Day 1 checkpoint:** You have a working tool. It scans, checks, scores, reports. That's the MVP.

---

## 🗓️ DAY 2 — Polish + Submit (Sunday)

### Block 1: Morning (9:00 AM–12:00 PM)

**Goal:** Test on a real repo, fix obvious breakage.

- [ ] Clone any small public Python repo (e.g., a simple Flask app)
- [ ] Run the tool on it
- [ ] Fix crashes (missing files, weird syntax, etc.)
- [ ] Add ONE more check **only if the first one works perfectly** — suggestion: flag `requests.get/post` without `timeout=`
- [ ] Commit: `"fix: handle edge cases"` or `"feat: timeout check"`
- [ ] Screenshot agent session

**Done when:** Tool runs cleanly on a real repo without crashing.

---

### Block 2: Afternoon (1:00 PM–4:00 PM)

**Goal:** Record demo + write submission.

- [ ] Record 2–3 minute demo video:
  - Show the repo
  - Run tool → "62%"
  - Fix one flagged issue
  - Rerun → "77%"
  - State impact: "This catches production blockers before merge"
- [ ] Write `README.md`:
  - Problem
  - Solution
  - How to run
  - Bob/agent usage evidence
- [ ] Create slide deck (5–7 slides max):
  1. Problem
  2. Solution
  3. Demo screenshot
  4. Bob 2.0 usage
  5. Impact metrics
  6. What's next
- [ ] Commit: `"docs: README and submission"`
- [ ] Screenshot agent session

**Done when:** Video + slides + README exist.

---

### Block 3: Evening (5:00 PM–8:00 PM)

**Goal:** Submit.

- [ ] Fill all submission fields on lablab.ai
- [ ] Upload cover image
- [ ] Upload video
- [ ] Upload slides
- [ ] Add GitHub repo link
- [ ] Verify: "screenshots of IBM Bob task session summaries" — **even if using Gemini/Claude, screenshot your agent sessions and label them clearly**
- [ ] Submit
- [ ] Screenshot the confirmation page

**Done when:** Submission confirmed.

---

## 🚫 Over-Engineering Kill List

Do NOT build these, no matter how tempting:

| Tempting Thing            | Why It Kills You                      |
| ------------------------- | ------------------------------------- |
| Web UI                    | 6+ hours, zero added score value      |
| Multiple languages        | Doubles complexity, same demo         |
| CI/CD integration         | Not demoable in 48 hours              |
| Database                  | No persistence needed                 |
| User auth                 | No users in a hackathon demo          |
| 10 checks                 | 1 great check > 10 broken ones        |
| Config files              | Hardcode thresholds for MVP           |
| Docker                    | It runs on your laptop, that's enough |
| Tests for the tool itself | Nice, but the demo matters more       |

---

## ✅ Solo Discipline Rules

1. **Commit every 90 minutes.** Broken commits are fine. Missing commits are not evidence.
2. **Screenshot every agent session.** You need these for submission.
3. **One feature at a time.** Finish it. Commit it. Then move on.
4. **Stop at Hour 40.** Last 8 hours = demo + submission only.
5. **Sleep 6+ hours.** Tired solo devs ship broken demos.
6. **If stuck > 30 min:** Ask agent, or cut the feature. Don't grind.

---

## 📋 Quick Reference: Your File Structure

```
readiness-scorecard/
├── agents.md
├── main.py
├── scanner.py
├── scorer.py
├── reporter.py
├── checks/
│   ├── __init__.py
│   └── missing_error_handling.py
├── requirements.txt
└── README.md
```

That's it. Six Python files. One check. One score. One demo.
