---
name: start-course
description: Start a learner on a course that already has a curriculum - for example a course exported or shared by someone else - by setting up the environment, recording the learner's profile and language, and showing the course map. Use when a course's STATE.md says it has not started or its LEARNER.md is not filled in, or when the learner invokes start-course.
---

# Start an existing course

Goal: in one short session the environment works, the learner's profile is recorded, they know how the course works, and Module 01 is ready. A welcome, not a lecture.

## 1. Environment

Read `course.json`. If it is not `"ready"`, use `setup-environment`: it gets each codebase from its recorded origin and commit into `sources/`, builds the runtime, configures the launcher, fetches the real datasets (after the learner's yes) and runs `lab check`.

**Audit a course that arrives prepared** (shared, exported, or generated earlier): open Module 01's primer and the first two lesson cards. If they only name boxes without explaining the algorithms, if labs run toy models or random data instead of the real codebase on real data, or if a figure or table has no reading guide, tell the learner and repair those lessons with `plan-module` and `teach-lesson` before teaching them. On a weaker machine than the author's (no GPU, less memory), note what that means for the course in one line.

## 2. Learner profile

Ask in **one** message, as a short numbered list; the learner may answer briefly or reply "skip" for defaults:

1. What language should I teach in?
2. Your background: languages and tools you know, experience with this topic.
3. Does the course goal (the "You will be able to" list in `COURSE.md`) match yours? Anything to add or skip?
4. Time: total hours, and minutes per session.

Write the answers to `LEARNER.md`. If they want to skip modules they already know, confirm with one or two concrete questions about what they have built (not a quiz), then mark those modules "skipped" in `COURSE.md`. If their goal differs a lot, offer to adjust the curriculum (`method/CURRICULUM_DESIGN.md`) before starting.

## 3. How the course works (≤ 250 words plus the course map)

Show `figures/course_map.png` (the big picture) and the module table from `COURSE.md`. Then, in the learner's language:

- The course goes top-down: Module 01 is a guided tour of the whole subject, one stop per part, then the real system runs end to end on real data; each later module zooms into one part, starting with a primer that explains how its key algorithm works. Bonus modules are optional depth after the core.
- Each lesson is one 20–40 minute experiment: I explain the mechanism with a diagram → we look at the real data and how to read the outputs → you predict, run, and we read the result together → you change something → a wrap-up.
- **This works best when you are active.** Interrupt me whenever something is unclear. Ask "why", "what does this plot mean", "explain again", "show me a picture", or say what you want to see. I will not move on while you have an open question, and I would rather answer ten questions than have you guess.
- Depth on request: `math`, `deeper`, `deeper <idea>`, `why`, `source`; pace: `slower`, `faster`; optional extras: `bonus`.
- One agent session per lesson; progress is saved in files. `START_HERE.md` lists what to type.

## 4. Record and hand over

- `STATE.md`: course started (date), environment summary, next action `plan-module` for the first module not skipped.
- End with: `▶ Next: reply "start" to begin Module 01 now, or later open a new session here and type teach-lesson continue.`
