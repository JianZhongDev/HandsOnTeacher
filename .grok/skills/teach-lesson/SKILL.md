---
name: teach-lesson
description: Prepare and deliver one hands-on lesson of a course - a lesson card that first explains the mechanism with a diagram, a tested lab that runs the real codebase on real data with a reading guide for every output, and four conversational turns that invite the learner's questions. Use when the learner says "continue", "next lesson", "bonus", or asks to learn the next course topic.
---

# Teach one lesson

A lesson is **one experiment** (20–40 minutes) built on **one mechanism the learner first understands**. Order: what and why → how it works (diagram) → data and reading guide → predict → run → read the result together → change and rerun → takeaway. Rules: `method/TEACHING_RULES.md` (rules 1, 4, 5 and 12 matter most). Style: `method/WRITING_GUIDE.md`.

The failure to avoid: a learner who runs a command, receives numbers and plots they cannot interpret, and has to guess what the teacher wanted.

## 1. Prepare (before saying anything)

0. Read the course's `STATE.md`, `LEARNER.md` (level, language, preferences, limits) and `course.json` (launcher, runtime, machine, datasets, timings).
1. Read the module's `MAP.md` and `PRIMER.md`. No `MAP.md`, or the primer not yet delivered (`STATE.md`) → use `plan-module` first; the lesson starts when the learner replies "start". If `STATE.md` says a lesson is in progress and its `results/` folders are newer than the last `NOTES.md` entry, ask in one line whether it is finished; if so, record it with `session-handoff`. If this lesson's card and lab already exist (prepared but not delivered), **re-audit them against sections 1.3–1.6 before delivering**: a prepared lesson that breaks the rules is rewritten, not delivered.
2. Write in `NOTES.md` (not to the learner): the question, the mechanism to teach, the 2–4 ideas, the transfer idea, the **dataset** used (name, source, licence), the **reference** results are compared with (ground truth, baseline, published numbers), and what you leave out.
3. **Plan the explanation first.** Which mechanism must the learner understand to read the result? Write its steps, its inputs and outputs, why it is built that way. Draw it (`make-visual`): a concept diagram with labelled boxes or geometry, plus pseudocode if it is an algorithm. Check the facts in the codebase checkout (read-only), in `materials/text/` and in the cited paper or doc; cite by name and page.
4. **Design the experiment on real code and real data** (rule 5). Use the course's primary codebase and the dataset recorded in `course.json` or a short excerpt of it. A change must show its consequence on a metric the field uses, against a reference. Do not use a toy model or random numbers as the experiment; if the real thing cannot run, stop and use `setup-environment` or ask the learner (see `build-lab`). A design topic gets a `your_turn` file. Build with `build-lab`, including the lab's printed **reading guide**.
5. **Run it** and look at every output and picture. It must finish within the time stated on the card on this machine. Annotate the result figure for the walkthrough in turn 3 (arrows, regions, a takeaway title).
6. Write `lessons/L<nn>-<name>/LESSON.md` from [assets/LESSON_TEMPLATE.md](assets/LESSON_TEMPLATE.md), with these sections, in this order: 🎯 Today · placing map · **How it works** (concept diagram, pseudocode or key formula in words, the design reason) · **Data and setup** (what real data, what the lab runs, what changes between settings) · **Reading guide** (each table column, axis, line and colour; what good looks like) · **Predict** · **Run** · **Try** · **Takeaway** · folded depth. Prose ≤ 700 words.
7. Run `python tools/lesson_stats.py <LESSON.md>`, then the `review-lesson` checklist. Fix until both pass.

## 2. Deliver: four turns, each a conversation step

Write in the learner's language. `<launcher>` is `./lab.sh` or `.\lab` (from `course.json`), run in the course folder. Write skill names the way the learner's agent expects. Show images in the chat, not only their paths. Turn lengths: `method/TEACHING_RULES.md` rule 3.

**Turn 1. What it teaches, and how it works.** The 🎯 Today intro + module map with today highlighted + one placing sentence + the concept diagram + the mechanism in plain steps (or pseudocode) and the design reason. Check that a newcomer could redraw the idea afterwards.
`▶ Next: reply "go on" when this makes sense, or ask anything (for example "why ...?", "explain again", "show me a picture").`

**Turn 2. The data, the setup and the reading guide.** Name the real data and where it came from, in one or two sentences, and what the lab runs on it. Say what changes between the settings, then the reading guide: each metric (name, unit, what it is compared with, what good looks like) and what each axis, line and colour of the figure will be. Ask for a one-sentence prediction. Give the command and its duration.
`▶ Next: run <launcher> <MM>/L<nn> (about N min), then reply "I ran it" with your prediction, or "run it for me".`

**Turn 3. Read the result together.** Show the (annotated) figure and the table. Walk through it in the order of the reading guide: what each curve or number is, what stands out, and **why**, tied back to the mechanism from turn 1. Compare with their prediction without grading. End with one specific check question about the result, and 1–2 tweaks (what to change, what to watch).
`▶ Next: answer in a few words (or reply "explain again"), then try <tweak> and reply "I ran <tweak>", or reply "wrap up".`

**Turn 4. Wrap up.** Two- or three-bullet takeaway, one line on where the idea applies beyond this codebase, an invitation to ask about anything unclear before moving on ("Anything still fuzzy? Ask now; the next lesson builds on this."), then record progress (section 3).
`✅ Progress saved. ▶ Next: close this session, start a new one in this folder, and type teach-lesson continue.`

Between turns:
- **Questions:** answer fully and plainly, with a diagram or small demo when it helps (`ask` and `explain-deeply` give the manner). Then restate where the lesson stands in `▶ Next:`. Never rush past a question to keep the schedule.
- **`math` / `deeper` / `why` / `source`:** expand fully on that point with `explain-deeply`, then return. `deeper <idea>` on a primer fundamental works at any time.
- **`slower` / `explain again` / `show me a picture`:** re-explain differently (an analogy, a worked example with real numbers from the lab, a new diagram), not the same words.
- **`faster`:** shorter turns from now on; merge turns 2 and 3. Record it. Never drop the reading guide or the mechanism.
- **`run it for me`**, or "continue" without having run it: run the lab and show the result.
- **`skip`:** confirm in one line, mark the lesson skipped in `MAP.md`, move on.
- **`bonus`:** see section 4.

Do not report verification or status in chat. That goes in `NOTES.md`.

## 3. Finish (in the same turn as turn 4)

Use `session-handoff`: mark the lesson done in `MAP.md`, update `COURSE.md` module status, set `STATE.md`'s next action to the next core lesson (or `plan-module` for the next core module). Record what the learner actually predicted, asked and answered. A lesson that is not recorded gets repeated. After a module's last core lesson, if `MAP.md` lists bonus lessons, name them in one line in turn 4; the next action stays on the core.

## 4. Bonus lessons and modules (`teach-lesson bonus`, or `bonus`)

Optional depth, offered after the core. List the current module's bonus lessons (`MAP.md`) and the course's bonus modules (`COURSE.md`), one line each, and teach the one the learner picks with this same procedure; a bonus module goes through `plan-module` first, primer included. Bonus work never changes `STATE.md`'s next core action unless the learner asks.

## References

- `method/WRITING_GUIDE.md`: before → after rewrites; card and turn shapes.
- `examples/microduck-rl/`: an example lesson card and module map (written under the older, shorter budgets: follow the section list above, not its length).
