# Designing a course from a codebase

How to turn "here is a repository (and maybe some papers, docs or other repositories), I want to learn X" into a short, complete curriculum of hands-on experiments. The `create-course` skill follows this document; `plan-module` uses the module entries it produces.

The result is a **lightning course**: the fewest experiments that give the learner working knowledge of the goal. It is built **top-down**, in three tiers:

```
 Big picture  ──────►  Core modules  ──────────►  Bonus modules (optional)
 Module 01: the        one essential box of        deeper or narrower topics,
 whole subject in      the big picture each,       offered after the core
 4–8 boxes, run        ending with the capstone
 end to end
```

Every module, in turn, opens with a short **primer** on the general fundamentals before its experiments. The learner always sees the whole before a part, and a part's fundamentals before its details.

The full curriculum is written up front; each module's primer and lessons are built later, when the learner reaches them, so they can adapt to how the learner is doing.

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

- **Big picture of the subject in 4–8 boxes**: the layers, stages or components of the *knowledge itself*, as a textbook or an expert would draw them, whether or not the codebase implements them all. For "how a computer works": applications → operating system → drivers and hardware abstraction layer → hardware (CPU, memory, storage, devices). For an algorithm or method: its main steps as short pseudocode. Mark which boxes the codebase demonstrates. This becomes the course map.
- **Architecture of the primary codebase in 4–8 boxes**: the main flow of data or control, in plain words, and which big-picture box each part implements.
- **Concepts it embodies**: the general ideas the code implements, each tagged *general* or *specific*, and the big-picture box it belongs to. Example: "domain randomization (general) via `vin_range` in the actuator config (specific)".
- **Experiment surfaces**: places where a learner can change one thing and quickly see a different behavior. For each: what to change, what you observe, how long one run takes. See `method/LAB_PATTERNS.md`. This list decides what the course can teach hands-on.
- **Design decisions worth comparing**: places where the authors chose one approach among several, with their reasons when written down (comments, docs, issues, commit messages). These become build-first tasks.
- **Costs and risks**: slow steps, GPU needs, network access, credentials, destructive commands to avoid.

## 3. Choose and order the modules

1. **Big picture module (always Module 01).** It answers "what are the parts, and how do they work together?" Its primer is the course map: each box in one plain line, and what flows between them. For a method or algorithm, the primer is its summary as short pseudocode. Its experiments run the whole thing end to end and make each box visible: trace one request, input or instruction through every box, or switch one stage off or change it and watch what happens downstream. The learner sees the full loop running within 10 minutes of starting.
2. **Core modules: one per essential box.** List the boxes of the big picture the learner needs for their outcomes. Each becomes a core module that answers one **big question** in plain words ("How does the OS share one CPU among many programs?", "Why does the trained robot fall on ice?") and teaches one general concept, shown through that part of the codebase. A large box may split into several modules (the OS box: scheduling, virtual memory, file systems); small boxes merge, or become primer ideas inside a neighbor.
3. **Keep only modules that can be hands-on.** Each needs at least two experiment surfaces with a visible behavior change. A topic with no surface becomes a primer idea or a bullet inside another module.
4. **Rank by value to the outcomes × how widely it transfers.** Keep the essentials as core until the course fits the time budget. Topics below the line become **bonus modules**, not cuts.
5. **Order the core by dependency**, following the big picture: usually the flow of data or control, or bottom-up through layers when upper layers rest on lower ones. Within that order:
   - **Mechanisms:** one module per essential box, the most depended-on first, each showing one box of the big picture working.
   - **Design:** the learner builds their own version of a component and compares it with the codebase's (build track). Usually a lesson inside a mechanism module; a module of its own when design is the goal.
   - **Evaluate and debug:** measure fairly, find failure modes, profile, test.
   - **Capstone (the last core module):** the learner makes one small, real improvement or extension and shows evidence that it works.
6. **Bonus modules** come after the capstone: deeper or narrower topics (a second scheduling algorithm, the math behind an optimizer, the hardware under a driver, a rarely used feature of the codebase). Each has a short entry and a box or note on the course map. They are built only when the learner asks, and are not counted in the time budget.
7. **Size it.** One lesson is about 30 minutes; one module is a 5–10 minute primer plus 2–3 lessons. Core lessons ≈ time budget (hours) × 2. Default lightning course: **the big picture module plus 4–7 core modules, about 4–8 hours, with 2–4 bonus modules listed.** If the learner gave no budget, propose this and say so.

## 4. Write each module entry

In `COURSE.md`, one entry per module, about 100–150 words, using these fields:

```
### 03 — <title>
**Track:** big picture / core / bonus
**Place in the big picture:** <which box of the course map; what it receives and what it hands on>
**Big question:** <plain words>
**Primer (3–5 fundamentals):** <the general ideas needed before the experiments, in textbook terms, not codebase terms>
**Transferable idea:** <general concept or skill> — also seen in <2 other places>
**Read (agent):** <code paths; document sections or pages; URLs>
**Experiments (2–3):** <what the learner changes> → <what they see>; ...
**Build task:** <what they write in your_turn.py, or "none">
**Evidence:** <what the learner produces that shows the outcome>
**After this module you can:** <one demonstrable outcome>
**Cost:** <run time per experiment, hardware or network needs>
**Bonus lessons:** <1–2 deeper experiments offered after this module's core lessons, or "none">
```

Bonus module entries may stop after **Experiments** and **Cost**; `plan-module` completes them if the learner takes one. These entries are raw material for `plan-module`, not text to show the learner.

## 5. Check before showing it

- Module 01 is the big picture: the whole subject in 4–8 boxes, and an end-to-end run that shows each box. Something runs in front of the learner within 10 minutes of starting.
- Every core module has a place on the course map, a primer of general fundamentals, a big question, a transferable idea and at least two experiments with a visible behavior change.
- Top-down order: no core module depends on an idea taught later, and no detail-level topic appears before the module that introduces its box. Details and side topics are bonus lessons or bonus modules, after the core.
- No module is reading-only. No lesson is a single idea.
- The course reaches every outcome from step 1, and the capstone uses most core modules.
- The core fits the time budget, and every experiment fits the run-time budget on this machine.
- Nothing requires credentials, paid services or real devices unless the learner agreed.

## 6. Pilot the first experiment

Before presenting the course, run the first module's main experiment surface once (a minute or two). If it does not show a visible change, fix the plan now: a course whose first experiment fails loses the learner.

## 7. A complete course: checklist

A finished course has everything an agent needs to teach it the way Learn RL with MicroDuck is taught. Check before the first lesson:

| Part | Where | Made by |
|---|---|---|
| Outcomes, course-specific rules, module table (big picture, core, bonus) and entries | `COURSE.md` | create-course |
| Course map: the big picture of the subject, with the modules that cover each box | `figures/course_map.png` and the script that draws it | create-course |
| Survey of the codebases and the sources map | `SURVEY.md` | create-course |
| Reference library with licenses and extracted text | `materials/` | create-course, `tools/extract_text.py` |
| Codebase checkouts at recorded commits | `sources/`, `course.json` | create-course, setup-environment |
| Isolated runtime and a working launcher | `.env/`, `lab.sh`, `lab.cmd`, `lab check` | setup-environment |
| Course helpers wrapping the primary codebase, documented and self-tested | `_shared/`, `_shared/README.md`, `_shared/selftest.py` | create-course |
| Learner profile, state, glossary, feedback log | `LEARNER.md`, `STATE.md`, `GLOSSARY.md`, `FEEDBACK_LOG.md` | create-course, then every session |
| Module maps, primers, lesson cards, labs, notes | `NN-<module>/` | plan-module, teach-lesson, session-handoff (just in time) |
| Teaching procedures and rules | `.agents/skills/`, `method/` (shared by all courses; exported with the course) | this repository |
| A standalone repository others can clone | `tools/export_course.py` | export-course |

## Worked example

`examples/microduck-rl/` shows a curriculum built this way for the MicroDuck robot-learning codebase: the course outline, one module map and one lesson card, with the reasoning behind each choice.
