---
name: plan-module
description: Start one module of a hands-on course - a primer that places the module in the course's big picture, introduces its general fundamentals and walks through its key algorithm with diagrams, a module map, and 2-3 experiment-sized lessons that run the real codebase on real data. Module 01 is a guided tour of the whole method. Use before the first lesson of any module, including a bonus module, or when a module's scope changes.
---

# Plan a module

Output: `courses/<course>/<NN>-<module>/PRIMER.md` (from [assets/PRIMER_TEMPLATE.md](assets/PRIMER_TEMPLATE.md); Module 01 uses [assets/TOUR_TEMPLATE.md](assets/TOUR_TEMPLATE.md)), `MAP.md` (from [assets/MAP_TEMPLATE.md](assets/MAP_TEMPLATE.md)), map and concept figures, and the messages that deliver the primer.

Every module goes **whole → fundamentals and mechanism → experiments**: where it sits in the course map, the general ideas it rests on, **how its key algorithm works (with a diagram)**, then labs on the real codebase and real data. Module 01 is the big picture itself: the guided tour (`method/CURRICULUM_DESIGN.md` § 3).

A primer that only names ideas and offers `deeper` is a failure: the learner then meets lab results with no idea what produced them. The primer teaches the mechanism.

## Steps

0. Create the folder: `python tools/new_module.py <course> <NN> <module-name> --title "<title>"`. It never overwrites files.
1. Read the module's entry in `COURSE.md` (track, place in the big picture, primer ideas, key algorithm, data), the relevant parts of `SURVEY.md`, open items in `STATE.md`, and the previous module's `TODO.md` and last `NOTES.md` entry (how did the learner do? what did they ask?).
2. **Where it sits.** Redraw the course map with this module's box highlighted into `figures/big_picture.png` (re-run the course's `figures/make_course_map.py` with a highlight; for Module 01, show the whole map).
3. **Big question** in plain words, and the **process** inside this box as 4–6 boxes for the module map (`handson.flow_diagram`, or `handson.layer_diagram` for layers; one image per lesson with that lesson's boxes highlighted; keep the script in `figures/`).
4. **Write the primer** (≤ 900 words of prose; Module 01 tour ≤ 1500). Read the algorithm in the paper or documentation and in the code before writing; do not paraphrase from memory.
   - the 🎯 **This module** intro: the topic by its general name, what it does, which box of the course map, what it receives and what it hands on;
   - **3–5 fundamental ideas** in general, textbook terms, most fundamental first, one or two plain sentences each. They hold beyond this codebase;
   - **How it works**: the module's key algorithm or mechanism, step by step, in plain words, with **a concept diagram** (made with `make-visual`: geometry, data flow, state over time) and short pseudocode. Say what each step takes in and gives out and why the design is that way. Use a small worked example with real numbers when it helps. Cite the paper section or doc page;
   - **In the code**: one short paragraph mapping the steps to the real codebase (file and function names allowed here);
   - **The data**: which real dataset the experiments use and why it suits the topic;
   - optionally a command under a minute that shows the mechanism on real data;
   - one line linking each idea to the lesson that makes it visible, and a line offering `deeper <idea>`, with sources from `materials/text/`.
   **Module 01 (the tour)**: whole-method pseudocode, then one stop per box of the course map (input → output with a real example, the core algorithm in plain words, a diagram, one design idea), then how to run the real system end to end and where each stop shows up in its outputs. No box is skipped or reduced to a name.
5. **Pick the 2–3 experiments** that make the primer's ideas visible on the real codebase and real data. For each:
   - one question the learner answers by running it;
   - the 2–4 ideas it teaches;
   - **what the learner changes, which metric answers the question, and what it is compared with** (ground truth, baseline or published result);
   - the dataset and excerpt, and its run time **on this machine** (`course.json` timings, 10 minutes at most);
   - whether it has a `your_turn` design task (a design topic should).
   If you cannot name a visible, meaningful change on real data, the experiment is not ready. **A toy simulation or random data is not a substitute.** Module 01's experiment runs the whole real system end to end and makes each box visible in its outputs.
6. **Bonus lessons:** list the module entry's 1–2 deeper experiments as "Bonus" rows in `MAP.md` (status `optional`). Do not build them now.
7. **Transfer:** name the general idea of each lesson and two places it appears outside this codebase.
8. **Check feasibility:** the knobs exist, the data is present, the run fits the budget, the effect is large enough to see. Pilot it on the real data. Run `python tools/lesson_stats.py <module folder>` and the `review-lesson` checklist on the primer.
9. **Deliver the primer as a short sequence of messages, each ≤ 350 words with its picture**, not one compressed block:
   1. the course map (this box highlighted), the 🎯 intro, the big question and the fundamentals as bullets;
   2. **How it works**: the concept diagram and the walkthrough of the key algorithm (Module 01: one message per two or three tour stops);
   3. the data, the lesson table (question · what you'll change · what you'll see), and an invitation: "Ask anything as we go; I would rather you interrupt than guess."
   End each message with `▶ Next: reply "go on"` (or ask a question), and the last with `▶ Next: reply "start" to begin L01, or type deeper <idea>.`

Planning detail (rejected ideas, feasibility notes, deferred topics) goes in `NOTES.md` and `TODO.md`, not in the primer. Update the module's status in `COURSE.md` to "planned", and record in `STATE.md` that the primer was delivered.
