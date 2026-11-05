---
name: review-lesson
description: Check a drafted lesson card, module primer, guided tour or teaching message against the course's teaching rules - that it explains the mechanism with a diagram, runs the real codebase on real data, explains every output, and invites questions - and fix what fails before the learner sees it. Use before delivering every lesson, module primer, course overview or long explanation, and when auditing a lesson that was prepared earlier.
---

# Review before delivery

Do not show this checklist to the learner. Fix every "no" by rewriting or adding the missing piece; remove only filler, never explanation.

## Understanding (check first; these are the failures that ruin a course)

1. **Mechanism explained?** A newcomer reading only the card or primer can say what goes in, what the key steps do, what comes out and why it is designed so. The algorithm is in the main text (pseudocode or numbered steps), not only behind `deeper` or a file name. For Module 01: every box of the course map has a tour stop with an algorithm explanation, not only a name.
2. **Diagram present?** A concept diagram of the mechanism (cards: at least one; primers: map plus at least one; tour: one per stop). Is it labelled, readable, and shown in chat as an image?
3. **Real code on real data?** The experiment runs the course's primary codebase on a named real dataset. A toy, random numbers or invented simulator as the main experiment is a **fail**: replace it, or stop and tell the learner what blocks real data or code. Synthetic data is allowed only after a real run, labelled in the first sentence, with a reason.
4. **Every output explained?** Each metric and figure has a reading guide: what it is, unit, compared with what, what good looks like, what each axis, line and colour is. The lab printed "How to read this" before the results. Metrics are the field's standard ones and are compared with a reference. Could the learner explain the figure back after reading the card?
5. **Setup stated?** The learner knows what the data is, what the lab does with it, what changes between settings and why, before running anything.
6. **Predict and check?** There is a one-sentence prediction prompt before the run and one specific check question after.
7. **Invites questions?** The lesson (and the turn-4 wrap-up) tells the learner to ask when unclear and offers `explain again` / `show me a picture` / `deeper`. At module starts the invitation is explicit.

## Budget (after understanding)

8. `python tools/lesson_stats.py <path to LESSON.md or PRIMER.md>` passes (card ≤ 700 words of prose, primer ≤ 900, Module 01 tour ≤ 1500, required sections and images present).
9. Each chat turn is ≤ 300 words (turn 1 and tour stops ≤ 350), plus pictures and code. Longer material is split into several steppable messages.
10. No restated question, recap, status or verification report, hedge (`method/WRITING_GUIDE.md`). Filler removed, nothing explanatory cut.

## Fit and form

11. **Says what it teaches?** Opens with the 🎯 intro: the topic by its general name, what it does or what problem it solves, input and output, in plain words a newcomer follows without the codebase. "Run `lab 05/L01 cfa=rggb`" is not an intro.
12. **Experiment-sized?** One experiment that teaches 2–4 ideas; nothing stretched from one sentence; not a mere run with no mechanism.
13. **Consequence visible?** The lab compares 2–5 settings side by side with metrics, on real data, and shows the behaviour change, not only a changed value.
14. **Build-first where it fits?** A design topic has a `your_turn` file and a comparison with the codebase's design and its reasons.
15. **Whole before parts?** Lesson: 🎯 intro, map plus one placing sentence, then how it works. Primer: map highlighted, fundamentals, algorithm walkthrough. Detail-level topics are bonus lessons.
16. **Transferable?** The general idea is named and the lesson says where else it applies.
17. **Plain?** New terms defined in one sentence; no invented labels; code instead of prose for computations.
18. **Depth folded correctly?** Only what goes beyond the lesson's mechanism (derivations, arithmetic, source tours) is in `<details>` or held for `math` / `deeper` / `why` / `source`.
19. **Honest and credited?** Claims match real output on this machine; results plausible against the published reference; no learner mastery claimed; sources and dataset licence named in one line; only short quotes of the codebase.
20. **Fits the learner?** Language and level from `LEARNER.md`; preferences honoured; run time and commands fit `course.json`.
21. **Safe?** No credentials, private data, production systems, deploy or destructive commands; runs ≤ 10 minutes unless the learner agreed; dataset downloads approved.
