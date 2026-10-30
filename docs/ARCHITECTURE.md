# Architecture

A two-minute orientation for AI agents and for people who want to change the method.

## Three layers

```
 method (how to teach)        courses (memory)                 tools (how to run things)
 ─────────────────────        ─────────────────────────        ──────────────────────────
 AGENTS.md                    courses/<course>/                 tools/new_course.py, new_module.py
 method/TEACHING_RULES.md       COURSE.md  SURVEY.md            tools/lesson_stats.py (budgets)
 method/CURRICULUM_DESIGN.md    STATE.md   LEARNER.md           courses/<course>/lab.sh, lab.cmd
 method/LAB_PATTERNS.md         course.json                     courses/<course>/_shared/handson
 method/WRITING_GUIDE.md        NN-<module>/MAP PRIMER NOTES TODO (copied from kit/handson)
 .agents/skills/                  lessons/L<nn>-<name>/         sources/<repo> (codebase checkout)
```

A session always goes: read the instructions → read the course memory → do one piece of teaching → write the memory back. Nothing depends on chat history, so any agent can continue where another stopped.

## Course lifecycle

```
"teach me X with repos Y, Z and these papers"
   └─ create-course ─ intake ─ new_course.py ─ clone repos to sources/, extract documents to materials/
                     ─ survey (SURVEY.md, sources map) ─ setup-environment (.env/, launcher, course.json)
                     ─ course helpers (_shared/, selftest) ─ curriculum (COURSE.md: big picture, core, bonus)
                     ─ pilot Module 01
                     ─ course map ─ STATE: next = plan-module 01
a shared or exported course
   └─ start-course ─ setup-environment (clones from course.json) ─ learner profile ─ course map
"continue"
   └─ teach-lesson ─ no MAP.md? → plan-module (new_module.py, primer, module map, 2–3 lessons)
                   ─ build-lab (lab.py, your_turn.py) ─ run it ─ LESSON.md ─ lesson_stats + review-lesson
                   ─ deliver in three turns ─ session-handoff (STATE, NOTES, MAP, COURSE status)
questions          └─ ask (answers; demos in questions/; never advances the course)
sharing            └─ export-course (tools/export_course.py: standalone repository, fresh start)
"math / deeper / why / source"
                   └─ explain-deeply
```

## Files and who writes them

| Path | Purpose | Written by |
|---|---|---|
| `AGENTS.md` | Canonical agent instructions, kept short | maintainers |
| `CLAUDE.md`, `GEMINI.md` | Import `AGENTS.md` for agents that look for those names | maintainers |
| `method/*.md` | Teaching rules, curriculum process, lab patterns, writing guide | maintainers |
| `.agents/skills/<name>/` | Procedures, with templates in `assets/` | maintainers |
| `.claude/skills/`, `.grok/skills/`, `.trae/skills/` | Copies of `.agents/skills/` for Claude Code, Grok Build and Trae | `tools/sync_skills.py` |
| `kit/handson/` | Lab helpers; copied into each new course | maintainers |
| `courses/<course>/` | One course: curriculum, progress, labs, runtime | the agent; the learner's runs |
| `sources/<repo>/` | Codebase checkouts courses use (read-only for lessons) | `create-course`, `setup-environment` |
| `courses/<course>/materials/` | Documents and web pages for a course, with extracted text | `tools/extract_text.py` |
| `examples/` | Worked example of a course design | maintainers |

## Design choices worth knowing

- **Whole before parts, parts before details.** Module 01 is the big picture of the subject, run end to end; each core module zooms into one box and opens with a primer of general fundamentals; deeper topics are bonus lessons and modules after the core.
- **Reading time is the scarcest resource.** Cards ≤ 200 words of prose and primers ≤ 250 (checked by `tools/lesson_stats.py`), chat turns ≤ 120. Depth is folded or given on request.
- **Experiments, not ideas.** A lesson is one 20–40 minute experiment that teaches 2–4 ideas, compares settings in one run, and shows behavior. Smaller ideas are bullets.
- **Curriculum up front, lessons just in time.** `COURSE.md` covers the whole course from day one; primers, module maps and labs are built when the learner arrives, using what `NOTES.md` says about how earlier lessons went.
- **Transferable first.** Modules are chosen by value to the learner's goal × how widely the idea transfers; the codebase is the worked example.
- **Short always-loaded instructions, details on demand.** `AGENTS.md` fits on two screens; procedures live in skills that load only when used. Long rule files are forgotten mid-session.
- **Machine differences are data, not prose.** `course.json` holds the runtime, launcher and timings; the launcher hides the OS.
- **The learner's code stays theirs.** Courses use their own checkout and runtime; lessons never edit the codebase.

## Supporting another agent

All agents share `AGENTS.md` and `.agents/skills/` (the Agent Skills layout).

| Agent | Reads instructions from | Finds skills in | Invocation |
|---|---|---|---|
| Codex | `AGENTS.md` | `.agents/skills/` | `$name` |
| Claude Code | `CLAUDE.md` (imports `AGENTS.md`) | `.claude/skills/` | `/name` |
| Gemini CLI | `GEMINI.md` (imports `AGENTS.md`) | `.agents/skills/` | by name or description |
| Antigravity | `AGENTS.md`, `GEMINI.md` | `.agents/skills/` | `/name`, or by name or description |
| Grok Build | `AGENTS.md` (also `CLAUDE.md`) | `.grok/skills/` | `/name` |
| Trae (incl. former Trae Work) | `.trae/rules/handsonteacher.md` (always applied; points to `AGENTS.md`) | `.trae/skills/` | by name |
| Doubao Work | not documented: the learner's first message points it to `AGENTS.md` | reads `SKILL.md` files directly | by name |
| anything else | point it at `AGENTS.md` | reads `SKILL.md` files directly | by name |

To add a mirror for another agent: `python tools/sync_skills.py --also <folder>`.

## Changing the method

- **A skill:** edit it in `.agents/skills/`, then run `python tools/sync_skills.py` (updates the Claude Code, Grok Build and Trae mirrors).
- **A rule:** keep `method/TEACHING_RULES.md` under about 150 lines and `AGENTS.md`'s core list in agreement with it. Merge new rules into existing ones; never stack "strict" sections.
- **The kit:** existing courses keep their own copy in `_shared/handson/`; copy the new kit in by hand if a course needs it.
- **Before committing:** `python tools/check_repo.py` checks skill mirrors and front matter, links, stray personal paths and line endings. CI runs the same check.
