# 📋 Official Submission Requirements

Submit through the **lablab.ai platform** before the deadline (Sept 27, 11:00 PM Hong Kong Time).

## 1. Basic Information
- [ ] **Project Title**
- [ ] **Short Description** (1–2 sentences)
- [ ] **Long Description** (problem, solution, how Bob 2.0 was used, impact)
- [ ] **Technology & Category Tags** (e.g., `Python`, `Developer Tools`, `IBM Bob 2.0`, `AI-Assisted Development`)

## 2. Cover Image and Presentation
- [ ] **Cover Image** (thumbnail for your project card)
- [ ] **Video Presentation** (2–3 min demo)
- [ ] **Slide Presentation** (pitch deck, 5–7 slides)

## 3. App Hosting & Code Repository
- [ ] **Demo Application Platform** (e.g., GitHub, local CLI, Replit)
- [ ] **Application URL** (GitHub repo link is fine for a CLI tool)
- [ ] **Code Repository** (public GitHub repo)

## 4. ⚠️ Critical: Bob 2.0 Evidence (Required)
- [ ] **Include any code or files where IBM Bob 2.0 assisted in development**
- [ ] **Screenshots of IBM Bob task session summaries for your project**

**Important note:** You mentioned using Gemini/Claude in your IDE instead of Bob. The hackathon explicitly requires Bob 2.0 evidence. You have two options:
1. **Get Bob access at kickoff** and run at least some sessions through it (recommended — you need this for judging)
2. **If Bob isn't available**, screenshot your agent sessions and clearly label them, but note this may affect your "Application of Technology" score since judges look for *Bob 2.0* specifically

**My advice:** Register for Bob access immediately at kickoff. Even running 3–4 key sessions through Bob (scaffolding, the check engine, debugging) gives you the required screenshots.

---

# 📸 Development Evidence Checklist (Capture As You Go)

Don't wait until Sunday. Screenshot these *when they happen*:

### Day 0 (Tonight)
- [ ] Agent session: project scaffold generation
- [ ] Screenshot of `agents.md` being created
- [ ] Screenshot of first successful `python main.py` run

### Day 1 (Saturday)
- [ ] Agent session: file scanner logic
- [ ] Agent session: error handling check (AST logic)
- [ ] Agent session: scorer formula
- [ ] Agent session: reporter with `rich` formatting
- [ ] Screenshot of tool output showing a real score
- [ ] Screenshot of a bug + the fix

### Day 2 (Sunday)
- [ ] Agent session: edge case fixes
- [ ] Agent session: README generation
- [ ] Screenshot of final tool run on a real repo
- [ ] Screenshot of GitHub repo with commit history
- [ ] Screenshot of submission confirmation page

**Storage tip:** Create a folder `evidence/` in your repo with subfolders `day0/`, `day1/`, `day2/`. Drop screenshots in as you take them.

---

# 📝 Submission Content Templates

## Short Description
> A CLI tool that scores any code branch for production readiness, catching missing error handling, timeouts, and security gaps before merge.

## Long Description (structure)
1. **Problem:** AI gets developers to 80% fast, but the last 20% (error handling, edge cases, security) causes rework and production incidents.
2. **Solution:** A readiness scorecard that scans a branch, runs checks, and outputs a 0–100 score with specific actionable gaps.
3. **How Bob 2.0 was used:** Scaffolding, AST-based check generation, debugging, test generation. (List specific sessions.)
4. **Impact:** Catches production blockers before merge. Demo shows 62% → 94% after fixing 3 flagged items.
5. **Tech stack:** Python, `ast`, `rich`, CLI.

## Slide Deck (5–7 slides)
1. **Title + tagline**
2. **Problem** (the last-mile gap)
3. **Solution** (what the tool does)
4. **Demo** (screenshot of score output)
5. **Bob 2.0 usage** (screenshots of sessions)
6. **Impact metrics** (before/after)
7. **What's next** (future checks, CI integration)

---

# ⏰ Timeline With Submission in Mind

| Time | Task | Submission Artifact |
|------|------|---------------------|
| **Tonight 8:30–11 PM** | Scaffold + `agents.md` | Screenshot session |
| **Sat 9 AM–12 PM** | File scanner | Screenshot session |
| **Sat 1–5 PM** | Error handling check | Screenshot session |
| **Sat 6–9 PM** | Scorer + reporter | Screenshot of working output |
| **Sun 9 AM–12 PM** | Test on real repo + fixes | Screenshot session |
| **Sun 1–4 PM** | Record video, write README, build slides | Video + slides + README |
| **Sun 5–8 PM** | Fill submission form, upload everything | Confirmation screenshot |

---

# ✅ Final Pre-Submit Checklist

Before you hit submit:

- [ ] Project title set
- [ ] Short + long description written
- [ ] Tags added
- [ ] Cover image uploaded
- [ ] Video uploaded (2–3 min)
- [ ] Slides uploaded
- [ ] GitHub repo public + link added
- [ ] Bob 2.0 session screenshots included
- [ ] `agents.md` and Bob-assisted files in repo
- [ ] `README.md` complete
- [ ] Submission confirmed (screenshot it)

---

**Key reminder:** The Bob 2.0 evidence is non-negotiable for scoring. Get Bob access at kickoff, run your key sessions through it, and screenshot everything. Gemini/Claude can help you *think*, but Bob needs to be visible in your submission.