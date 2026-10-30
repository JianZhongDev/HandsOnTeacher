---
name: plan-module
description: Start one module of a hands-on course - a module map and 2-3 experiment-sized lessons, each a lab where a change shows its effect on behavior the learner cares about. Use before the first lesson of any module, or when a module's scope changes.
---

# Plan a module

Output: `courses/<course>/<NN>-<module>/MAP.md` (from [assets/MAP_TEMPLATE.md](assets/MAP_TEMPLATE.md)), map figures, and a short overview message.

## Steps

0. Create the folder: `python tools/new_module.py <course> <NN> <module-name> --title "<title>"`. It never overwrites files.
1. Read the module's entry in `COURSE.md`, the relevant parts of `SURVEY.md`, open items in `STATE.md`, and the previous module's `TODO.md` and last `NOTES.md` entry (how did the learner do?).
2. **Big question** in plain words, and the **process** as 4–6 boxes for the map figure (`handson.flow_diagram`, one image per lesson with that lesson's boxes highlighted; keep the script in `figures/`). If plotting is not available, use a Mermaid flowchart.
3. **Pick the 2–3 experiments** that teach the module. For each:
   - one question the learner answers by running it;
   - the 2–4 ideas it teaches (small ideas become bullets inside a lesson, never lessons of their own);
   - **what the learner changes and what behavior changes as a result** (side-by-side picture and a metric table, not just a printed value);
   - whether it has a `your_turn` design task (a design topic should);
   - its run time **on this machine** (`course.json` timings). Keep each run under 10 minutes.
   If you cannot name a visible behavior change, the experiment is not ready.
4. **Transfer:** name the general idea of each lesson and two places it appears outside this codebase.
5. **Check feasibility:** the knobs exist, the run fits the budget, the effect is large enough to see. If unsure, run a quick pilot.
6. **Send the overview** (≤ 120 words): the module map image, the big question in one line, and a table with one row per lesson (question · what you'll change · what you'll see). End with `▶ Next: reply "start" to begin L01.`

Planning detail (rejected ideas, feasibility notes, deferred topics) goes in `NOTES.md` and `TODO.md`, not in the overview. Update the module's status in `COURSE.md` to "planned".
