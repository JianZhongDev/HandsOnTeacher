---
name: start-course
description: Start a learner on a course that already has a curriculum - for example a course exported or shared by someone else - by setting up the environment, recording the learner's profile and language, and showing the course map. Use when a course's STATE.md says it has not started or its LEARNER.md is not filled in, or when the learner invokes start-course.
---

# Start an existing course

Goal: in one short session the environment works, the learner's profile is recorded, they know how the course works, and Module 01 is ready. A welcome, not a lecture.

## 1. Environment

Read `course.json`. If it is not `"ready"`, use `setup-environment`: it gets each codebase from its recorded origin and commit into `sources/`, builds the runtime, configures the launcher and runs `lab check`. On a weaker machine than the author's (no GPU, less memory), note what that means for the course in one line.

## 2. Learner profile

Ask in **one** message, as a short numbered list; the learner may answer briefly or reply "skip" for defaults:

1. What language should I teach in?
2. Your background: languages and tools you know, experience with this topic.
3. Does the course goal (the "You will be able to" list in `COURSE.md`) match yours? Anything to add or skip?
4. Time: total hours, and minutes per session.

Write the answers to `LEARNER.md`. If they want to skip modules they already know, confirm with one or two concrete questions about what they have built (not a quiz), then mark those modules "skipped" in `COURSE.md`. If their goal differs a lot, offer to adjust the curriculum (`method/CURRICULUM_DESIGN.md`) before starting.

## 3. How the course works (≤ 120 words plus the course map)

Show `figures/course_map.png` (the big picture) and the module table from `COURSE.md`. Then, in the learner's language:

- The course goes top-down: Module 01 shows the whole subject running; each later module zooms into one part, starting with a five-minute primer on the fundamentals. Bonus modules are optional depth after the core.

- After the primer, each lesson is one 20–40 minute experiment: a short card and one command → run it → read the results together and try a tweak → a two-line wrap-up. Design topics start with their own version in `your_turn.py`.
- Depth on request: `math`, `deeper`, `deeper <idea>`, `why`, `source`; shorter: `faster`; optional extras: `bonus`.
- One agent session per lesson; progress is saved in files. `START_HERE.md` lists what to type.

## 4. Record and hand over

- `STATE.md`: course started (date), environment summary, next action `plan-module` for the first module not skipped.
- End with: `▶ Next: reply "start" to begin Module 01 now, or later open a new session here and type teach-lesson continue.`
