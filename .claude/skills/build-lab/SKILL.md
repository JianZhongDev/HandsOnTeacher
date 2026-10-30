---
name: build-lab
description: Write and test a hands-on lab for a course - a short script that runs the real codebase under 2-5 settings in one run, shows the effect on observable behavior side by side, offers command-line knobs and an editable your_turn design task, and finishes within minutes. Use when preparing a lesson's lab or any learner-run experiment.
---

# Build a lab

A lab lives at `courses/<course>/<NN>-<module>/lessons/L<nn>-<name>/lab.py` (or the lab file in `course.json`) and runs with `lab <MM>/L<nn> [key=value ...]` from the course folder.

## What a good lab does

1. **Uses the real codebase.** Import it, call it, run it. A toy model only when it shows the idea much better, then connect it back in the same lab.
2. **Compares, in one run.** 2–5 settings side by side: a small table of observable metrics (`handson.print_table`), one picture (`handson.side_by_side`, or one plot with all settings on the same axes). The learner should not need to re-run just to compare.
3. **Shows consequences in behavior.** What a user or operator would notice: outputs, errors, failures, speed, quality. Not only an internal value. Patterns by kind of codebase: `method/LAB_PATTERNS.md`.
4. **Lets the learner design.** When the lesson is about a design choice, the part they design is one short function in `your_turn.py` with a clear docstring and a working default ([assets/your_turn_template.py](assets/your_turn_template.py)). The lab runs it next to the codebase's own version.
5. **Lets them explore instantly** when something computes in seconds: `handson.slider_page(...)` writes `explore.html`.
6. **Is short and readable.** `lab.py` is about 20–60 lines: the experiment, not plumbing. Repeated plumbing goes in the course's `_shared/` as a helper module, never copied between labs.

## Rules

- Settings through `handson.lab_config({...}, help={...})`, with units in the help text. Defaults give a clear, typical result.
- Never edit the codebase checkout. Change behavior through knobs, wrappers, subclasses, config copies, or patches applied inside the lab (`method/LAB_PATTERNS.md`, "Ways to change behavior"). Say in the docstring when a lab patches something.
- Outputs go in `run.out` (one folder per setting combination). Comparisons across runs go in `run.lab_dir / "results"`. Slow, reusable artifacts go in the lesson's `cache/` or the course's `_shared/`, keyed by everything that affects them.
- Each run stays under 10 minutes on this machine (`course.json` timings); say the total time in the card. Longer runs need the learner's yes.
- Printed output: one small table with words for column names. No dumps, no verification essays.
- Labs never use real user data, credentials or production systems, and never run the codebase's deploy or destructive commands.
- The docstring names the question, the run command, one tweak, and the design file if there is one.

Template: [assets/lab_template.py](assets/lab_template.py). Kit API and the contract for labs in other languages: [references/handson_kit.md](references/handson_kit.md).

## Test before the lesson

Run the default and one tweak. Open every output, including pictures. Check every claim the card will make against the output. Record timing and checks in `NOTES.md`. Delete test `results/` folders so the learner starts clean (keep `cache/` if the lab reuses it, and say so in `NOTES.md`).
