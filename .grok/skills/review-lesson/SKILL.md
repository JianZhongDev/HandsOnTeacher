---
name: review-lesson
description: Check a drafted lesson card, module overview or teaching message against the course's reading budget and teaching rules, and cut or rewrite what fails, before the learner sees it. Use before delivering every lesson, module overview, course overview or long explanation.
---

# Review before delivery

Do not show this checklist to the learner. Fix every "no" by cutting or rewriting; never by adding text.

## Budget (check first)

1. `python tools/lesson_stats.py <path to LESSON.md>` passes (≤ 200 words of prose).
2. Each chat turn is ≤ 120 words, plus one picture or code block.
3. Did you cut about 40% after drafting? No restated question, no recap, no status or verification report, no hedges (`method/WRITING_GUIDE.md`).

## Substance

4. **Experiment-sized?** One experiment that teaches 2–4 ideas. Nothing that is "just one sentence" stretched into a section.
5. **Doing first?** The learner runs, edits or drags something before reading much. Is the result shown before the explanation?
6. **Consequence visible?** Does the lab show what the change does to observable behavior (side by side, with metrics), not only a changed value?
7. **Build-first where it fits?** For a design topic: is there a `your_turn` file and a comparison with the codebase's design and its reasons?
8. **Transferable?** Is the general idea named, and does the lesson say where else it applies?
9. **Map in one glance?** Map image plus one placing sentence. No long process recap.
10. **Plain?** New terms defined in one sentence where they appear; no invented labels; code instead of prose for computations.
11. **Depth folded?** Derivations, symbol tables, arithmetic and source details are inside `<details>` or held for `math` / `deeper` / `why` / `source`.
12. **Honest and credited?** Claims match the real output on this machine; toys are labelled; no learner mastery claimed; sources named in one line; only short quotes of the codebase.
13. **Fits the learner?** Written in the language in `LEARNER.md`, at their level, honoring their preferences; run time and commands fit `course.json`.
14. **Safe?** No credentials, real user data, production systems, deploy or destructive commands; runs ≤ 10 minutes unless the learner agreed.
15. **Next step?** One `▶ Next:` line with the exact command or reply, matching `START_HERE.md`.
