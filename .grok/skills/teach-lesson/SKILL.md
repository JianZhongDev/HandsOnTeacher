---
name: teach-lesson
description: Prepare and deliver one hands-on lesson of a course - a short lesson card, a tested lab the learner runs and tweaks (comparing settings side by side, sometimes building their own version first), and three short chat turns. Use when the learner says "continue", "next lesson", "bonus", or asks to learn the next course topic.
---

# Teach one lesson

A lesson is **one experiment** (20–40 minutes of doing) that teaches 2–4 related ideas. The learner should spend most of the time running, tweaking and watching, and little time reading. Rules: `method/TEACHING_RULES.md`. Style: `method/WRITING_GUIDE.md`.

## 1. Prepare (before saying anything)

0. Read the course's `STATE.md`, `LEARNER.md` (level, language, preferences, limits) and `course.json` (launcher, runtime, machine, timings).
1. Read the module's `MAP.md` and `PRIMER.md`. No `MAP.md`, or the primer not yet delivered (`STATE.md`) → use `plan-module` first; it ends by delivering the primer, and the lesson starts when the learner replies "start". If `STATE.md` says a lesson is in progress and its `results/` folders are newer than the last `NOTES.md` entry, ask in one line whether it is finished; if so, record it with `session-handoff`. If this lesson's card and lab already exist (prepared but not delivered), re-run the lab, check the card against the output, and go to section 2.
2. Write in `NOTES.md` (not to the learner): the experiment's question, the 2–4 ideas, the transferable idea, and what you leave out.
3. Design the experiment so a **change shows its consequence in behavior** (rule 4). If the topic is a design choice, include a `your_turn` file (rule 5). Build it with `build-lab`. Check facts in the codebase checkouts (read-only) and in `materials/text/`; cite documents by name and page in the Sources line.
4. **Run it** and look at every output. It must finish within the time stated on the card on this machine.
5. Write `lessons/L<nn>-<name>/LESSON.md` from [assets/LESSON_TEMPLATE.md](assets/LESSON_TEMPLATE.md). Prose ≤ 200 words; derivations and source details go in the folded block.
6. Run `python tools/lesson_stats.py <path to LESSON.md>`, then the `review-lesson` checklist. Fix until both pass.

## 2. Deliver: three short turns (≤ 120 words each, one picture or code block)

Write in the learner's language. `<launcher>` is `./lab.sh` or `.\lab` (from `course.json`), run in the course folder. Write skill names the way the learner's agent expects (`$name` in Codex, `/name` in Claude Code, plain elsewhere).

**Turn 1. Start doing.** Module map image + one sentence of context, naming the primer idea this experiment makes visible + the experiment in one or two lines of code + the command and how long it takes + what to watch.
`▶ Next: run <launcher> <MM>/L<nn> (about N min), then reply "I ran it" (or "run it for me").`

**Turn 2. Read the result together.** Show their result (side-by-side picture or comparison table). Two or three sentences: what it shows and why. Offer 1–2 tweaks, each with what to watch, including an edit to `your_turn` when the lab has one.
`▶ Next: try <tweak> and reply "I ran <tweak>", or reply "wrap up".`

**Turn 3. Wrap up.** Two-bullet takeaway, one line on where the idea applies beyond this codebase, then record progress (section 3).
`✅ Progress saved. ▶ Next: close this session, start a new one in this folder, and type teach-lesson continue.`

Between turns:
- **Questions:** answer only the question, at the same brevity. Then `▶ Next:` restating where the lesson stands.
- **`math` / `deeper` / `why` / `source`:** expand fully on that point with `explain-deeply`, then return. `deeper <idea>` on a primer fundamental works at any time.
- **`faster`:** shorter turns from now on; merge turns 2 and 3. Record it as a preference.
- **`run it for me`**, or "continue" without having run it: run the lab and show the result.
- **`skip`:** confirm in one line, mark the lesson skipped in `MAP.md`, move on.
- **`bonus`:** see section 4.

Do not repeat the card in chat, recap earlier turns, or report verification or status. That goes in `NOTES.md`.

## 3. Finish (in the same turn as turn 3)

Use `session-handoff`: mark the lesson done in `MAP.md`, update `COURSE.md` module status, and set `STATE.md`'s next action to the next core lesson (or `plan-module` for the next core module). A lesson that is not recorded gets repeated. After a module's last core lesson, if `MAP.md` lists bonus lessons, name them in one line in turn 3; the next action stays on the core.

## 4. Bonus lessons and modules (`teach-lesson bonus`, or `bonus`)

Optional depth, offered after the core. List the current module's bonus lessons (`MAP.md`) and the course's bonus modules (`COURSE.md`), one line each, and teach the one the learner picks with this same procedure; a bonus module goes through `plan-module` first, primer included. Bonus work never changes `STATE.md`'s next core action unless the learner asks. After the capstone, the bonus modules are the natural next step.

## References

- `method/WRITING_GUIDE.md`: before → after rewrites; card and turn shapes.
- `examples/microduck-rl/`: a finished lesson card and module map in this format.
