# Designing a course from a codebase

How to turn "here is a repository (and maybe some papers, docs or other repositories), I want to learn X" into a short, complete curriculum of hands-on experiments. The `create-course` skill follows this document; `plan-module` uses the module entries it produces.

The result is a **lightning course**: the fewest experiments that give the learner working knowledge of the goal, ordered so each one builds on the last. The full curriculum is written up front; each module's lessons are built later, when the learner reaches them, so they can adapt to how the learner is doing.

## 1. Pin down the goal

Turn the learner's request into **3–6 outcomes**, each starting with a verb the learner could demonstrate:

> "explain why the robot falls when commands arrive late", "design a reward term and show its effect", "add a new API endpoint with a test", "profile a slow query and fix it".

Split outcomes into **transferable** (useful beyond this codebase) and **codebase-specific** (useful for working on this codebase). Lead with transferable ones unless the learner's goal is to contribute to this codebase.

If the goal is vague ("learn this repo"), propose outcomes and confirm them in one line.

## 2. Survey the sources (time-boxed)

Courses can draw on several sources. Give each a role:

- **Primary codebase:** the code most experiments run. One per course where possible; the course helpers wrap it.
- **Supporting codebases:** other implementations to compare against, or tools the primary one needs. A second implementation of the same idea makes an excellent build-and-compare lesson.
- **Reference material:** papers, books, official docs, specs, slides, tutorials, the learner's own notes. They supply concepts, vocabulary, theory and the "why"; they decide the order of ideas and settle what correct behavior is. They are not where the learner spends time: lessons cite the page and keep the experiment central.

Read, do not run everything. For code: README and docs, the dependency file (`pyproject.toml`, `package.json`, `Cargo.toml`, …), the CI workflow (the most reliable recipe for building and testing), entry points, examples, tests, configuration. For documents: table of contents first, then the sections that match the learner's outcomes. Where sources disagree (versions, terminology, recommended practice), record which one wins and why: newer, official, or matches the code that runs. Write the findings to the course's `SURVEY.md` (one page, from the template):

- **Architecture in 4–8 boxes**: the main flow of data or control, in plain words. This becomes the course map.
- **Concepts it embodies**: the general ideas the code implements, each tagged *general* or *specific*. Example: "domain randomization (general) via `vin_range` in the actuator config (specific)".
- **Experiment surfaces**: places where a learner can change one thing and quickly see a different behavior. For each: what to change, what you observe, how long one run takes. See `method/LAB_PATTERNS.md`. This list decides what the course can teach hands-on.
- **Design decisions worth comparing**: places where the authors chose one approach among several, with their reasons when written down (comments, docs, issues, commit messages). These become build-first tasks.
- **Costs and risks**: slow steps, GPU needs, network access, credentials, destructive commands to avoid.

## 3. Choose and order the modules

1. **List candidate modules.** One module answers one **big question** in plain words ("Why does the trained robot fall on ice?", "Where does a request spend its time?"). Each module teaches one general concept or skill, shown through one part of the architecture.
2. **Keep only modules that can be hands-on.** Each needs at least two experiment surfaces with a visible behavior change. A topic with no surface becomes a bullet inside another module, or is cut.
3. **Rank by value to the outcomes × how widely it transfers.** Cut from the bottom until the course fits the time budget.
4. **Order by dependency**, following this arc:
   - **Orient:** run the whole thing end to end and change one knob. The learner sees the full loop in the first module.
   - **Mechanisms:** one module per core mechanism, simplest first, each showing one box of the architecture working.
   - **Design:** change and extend: the learner builds their own version of a component and compares it with the codebase's (build track).
   - **Evaluate and debug:** measure fairly, find failure modes, profile, test.
   - **Capstone:** the learner makes one small, real improvement or extension and shows evidence that it works.
5. **Size it.** One lesson is about 30 minutes; one module is 2–3 lessons. Lessons ≈ time budget (hours) × 2. Default lightning course: **5–8 modules, about 4–8 hours.** If the learner gave no budget, propose this and say so.

## 4. Write each module entry

In `COURSE.md`, one entry per module, about 80–120 words, using these fields:

```
### 03 — <title>
**Big question:** <plain words>
**Transferable idea:** <general concept or skill> — also seen in <2 other places>
**Read (agent):** <code paths; document sections or pages; URLs>
**Experiments (2–3):** <what the learner changes> → <what they see>; ...
**Build task:** <what they write in your_turn.py, or "none">
**Evidence:** <what the learner produces that shows the outcome>
**After this module you can:** <one demonstrable outcome>
**Cost:** <run time per experiment, hardware or network needs>
```

These entries are raw material for `plan-module`, not text to show the learner.

## 5. Check before showing it

- Every module has a big question, a transferable idea and at least two experiments with a visible behavior change.
- The first module puts something running in front of the learner within 10 minutes of starting.
- No module is reading-only. No lesson is a single idea.
- The course reaches every outcome from step 1, and the capstone uses most modules.
- The total fits the time budget, and every experiment fits the run-time budget on this machine.
- Nothing requires credentials, paid services or real devices unless the learner agreed.

## 6. Pilot the first experiment

Before presenting the course, run the first module's main experiment surface once (a minute or two). If it does not show a visible change, fix the plan now: a course whose first experiment fails loses the learner.

## 7. A complete course: checklist

A finished course has everything an agent needs to teach it the way Learn RL with MicroDuck is taught. Check before the first lesson:

| Part | Where | Made by |
|---|---|---|
| Outcomes, course-specific rules, module table and entries | `COURSE.md` | create-course |
| Course map | `figures/course_map.png` | create-course |
| Survey of the codebases and the sources map | `SURVEY.md` | create-course |
| Reference library with licenses and extracted text | `materials/` | create-course, `tools/extract_text.py` |
| Codebase checkouts at recorded commits | `sources/`, `course.json` | create-course, setup-environment |
| Isolated runtime and a working launcher | `.env/`, `lab.sh`, `lab.cmd`, `lab check` | setup-environment |
| Course helpers wrapping the primary codebase, documented and self-tested | `_shared/`, `_shared/README.md`, `_shared/selftest.py` | create-course |
| Learner profile, state, glossary, feedback log | `LEARNER.md`, `STATE.md`, `GLOSSARY.md`, `FEEDBACK_LOG.md` | create-course, then every session |
| Module maps, lesson cards, labs, notes | `NN-<module>/` | plan-module, teach-lesson, session-handoff (just in time) |
| Teaching procedures and rules | `.agents/skills/`, `method/` (shared by all courses; exported with the course) | this repository |
| A standalone repository others can clone | `tools/export_course.py` | export-course |

## Worked example

`examples/microduck-rl/` shows a curriculum built this way for the MicroDuck robot-learning codebase: the course outline, one module map and one lesson card, with the reasoning behind each choice.
