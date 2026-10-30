---
name: plan-module
description: Start one module of a hands-on course - a primer that places the module in the course's big picture and introduces its general fundamentals, a module map, and 2-3 experiment-sized lessons, each a lab where a change shows its effect on behavior the learner cares about. Use before the first lesson of any module, including a bonus module, or when a module's scope changes.
---

# Plan a module

Output: `courses/<course>/<NN>-<module>/PRIMER.md` (from [assets/PRIMER_TEMPLATE.md](assets/PRIMER_TEMPLATE.md)), `MAP.md` (from [assets/MAP_TEMPLATE.md](assets/MAP_TEMPLATE.md)), map figures, and one short message that delivers the primer.

Every module goes **whole → fundamentals → experiments**: where it sits in the course map, then the general ideas it rests on, then labs on the codebase. Module 01 is the big picture itself (`method/CURRICULUM_DESIGN.md` § 3).

## Steps

0. Create the folder: `python tools/new_module.py <course> <NN> <module-name> --title "<title>"`. It never overwrites files.
1. Read the module's entry in `COURSE.md` (track, place in the big picture, primer ideas), the relevant parts of `SURVEY.md`, open items in `STATE.md`, and the previous module's `TODO.md` and last `NOTES.md` entry (how did the learner do?).
2. **Where it sits.** Redraw the course map with this module's box highlighted into `figures/big_picture.png` (re-run the course's `figures/make_course_map.py` with a highlight; for Module 01, highlight nothing or every box in turn).
3. **Big question** in plain words, and the **process** inside this box as 4–6 boxes for the module map (`handson.flow_diagram`, or `handson.layer_diagram` for layers; one image per lesson with that lesson's boxes highlighted; keep the script in `figures/`). If plotting is not available, use a Mermaid flowchart.
4. **Write the primer** (`PRIMER.md`, ≤ 250 words of prose):
   - one sentence placing the module: which box of the course map, what it receives and what it hands on;
   - **3–5 fundamental ideas** in general, textbook terms, most fundamental first, one or two plain sentences each. They must hold beyond this codebase ("a scheduler decides which ready program runs next"), not describe it ("`sched.c` picks from `runq`");
   - one concept picture when it saves reading: a layer stack, a timeline, a data layout (`make-visual`), labelled as a schematic;
   - optionally one command under a minute that shows the mechanism running (`lab run ...`): the doing-first part of the primer;
   - one line linking each idea to the lesson that makes it visible, and one line offering `deeper <idea>`, with sources (textbook chapter, paper, doc page from `materials/text/`).
   Module 01's primer is the course map itself: every box in one line and what flows between them; for a method or algorithm, its summary as pseudocode of under 15 lines.
5. **Pick the 2–3 experiments** that make the primer's ideas visible in the codebase. For each:
   - one question the learner answers by running it;
   - the 2–4 ideas it teaches (small ideas become bullets inside a lesson, never lessons of their own);
   - **what the learner changes and what behavior changes as a result** (side-by-side picture and a metric table, not just a printed value);
   - whether it has a `your_turn` design task (a design topic should);
   - its run time **on this machine** (`course.json` timings). Keep each run under 10 minutes.
   If you cannot name a visible behavior change, the experiment is not ready. Module 01's experiments run the whole thing end to end and make each box visible.
6. **Bonus lessons:** list the module entry's 1–2 deeper experiments as "Bonus" rows in `MAP.md` (status `optional`). Do not build them now; `teach-lesson bonus` builds one on request.
7. **Transfer:** name the general idea of each lesson and two places it appears outside this codebase.
8. **Check feasibility:** the knobs exist, the run fits the budget, the effect is large enough to see. If unsure, run a quick pilot. Run `python tools/lesson_stats.py <module folder>` (checks the primer's budget) and the `review-lesson` checklist on the primer.
9. **Deliver the primer** (≤ 200 words, up to two pictures: `big_picture.png` and the concept picture): one placing sentence, the big question in one line, the fundamentals as bullets, and a table with one row per core lesson (question · what you'll change · what you'll see). End with `▶ Next: reply "start" to begin L01, or type deeper <idea> for more on any idea.`

Planning detail (rejected ideas, feasibility notes, deferred topics) goes in `NOTES.md` and `TODO.md`, not in the primer. Update the module's status in `COURSE.md` to "planned", and record in `STATE.md` that the primer was delivered.
