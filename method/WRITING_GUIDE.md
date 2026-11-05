# Writing guide

The learner reads every word you write. Make it cheap to read, and make sure it explains. Writing short is not the goal; being understood is. Cut filler, never a definition, a step of the mechanism, or the reading guide of a figure.

## Ten rules

1. **Lead with the point.** First sentence = the answer or the action.
2. **One idea per sentence**, about 20 words at most. Short paragraphs (1–3 sentences).
3. **Code over prose.** If a sentence describes a computation, show the two lines of code instead.
4. **Concrete over abstract.** "The robot falls after 1.2 s" beats "the controller fails to maintain balance". "The page takes 3 s" beats "latency increases".
5. **No hedges or provenance chatter.** Cut: "in the inspected version", "constructed inputs", "note that", "it is worth mentioning", "this does not establish", "for clarity". Put real caveats in one line, or in `NOTES.md`.
6. **No restating.** Do not repeat the question, the map, the previous turn, or what the picture already shows.
7. **Numbers only when they matter**, rounded (1.2 s, not 1.18432 s).
8. **Everyday words.** "falls" not "terminates via orientation condition"; "how often" not "frequency of occurrence".
9. **Active voice, present tense.** "The penalty lowers the score", not "a reduction in score is produced".
10. **Cut filler** after drafting (hedges, restating, status chatter). Keep every definition, mechanism step and figure explanation. Then check the budgets (card ≤ 700, primer ≤ 900, tour ≤ 1500, chat turn ≤ 300, a lesson's first turn ≤ 350).

## Before → after

These come from a robot-learning course built with this method; the same failures appear in any subject.

**Explaining a mechanism.** Before (120 words):

> An **action** is the controller's output used to set joint targets. This check uses the raw outputs, before their conversion to targets. It measures command changes, not how far a joint actually moved. A **reward weight** is a signed multiplier: it controls how a measured quantity contributes to the reward. Higher reward is favored during learning. Read this calculation from the command pair to its score: [code] Squaring makes either direction of change count positively. A negative weight turns that positive amount into a deduction from the reward. The lab uses constructed inputs to the installed reward function, isolating this calculation without simulating motion or training.

After (35 words):

> ```python
> jerk = ((action - prev_action) ** 2).sum()   # how abruptly commands change
> reward += -0.1 * jerk                        # negative weight = penalty
> ```
> Squaring makes any change count; the negative weight turns it into a cost. The lab retrains with your weight so you can see what it does to the motion.

**Telling the learner what to run.** Before (60 words):

> Open `results/default/scores.png`. Look first at the right-hand bars: does the large change receive a lower contribution than the unchanged command? Then look left to see the raw values before weighting. You also get `scores.csv` (the three cases), `summary.json` (settings, source and checks), and `signals.npz` (saved values).

After (14 words):

> Run `lab 04/L01`. Watch the two robots in `compare.gif`: which one shakes?

**Reporting a result.** Before:

> The teacher verification passed for both settings. In the default run, the first fall occurred at 1.36 s and the second at 2.72 s, while the early snapshot fell at 1.24, 2.48 and 3.72 s. This comparison does not establish walking quality or learner understanding.

After:

> Both controllers fall within 1.4 s. Neither has learned to walk yet: 5 training updates is far too few.

**Introducing a module.** Before: the details come first.

> Module 05. `scheduler.c` loops over `proc_table`, skips entries whose `state != RUNNABLE`, and calls `swtch(&cpu->ctx, &p->ctx)`. Change `TICK_MS` in `param.h` and run `lab 05/L01`.

After: the place in the big picture, then the general ideas; the code comes in the lessons.

> *(course map, operating system box highlighted)* Inside the operating system box: many programs share one CPU.
> - **Scheduler:** decides which ready program runs next.
> - **Time slice:** how long a program runs before the scheduler may switch.
> - **Context switch:** saving one program's registers and loading another's; it costs time.
>
> L01: change the time slice and watch response time and throughput trade off.

**Opening a lesson.** Two failures: three paragraphs on history and motivation before anything runs, or the opposite, straight into the details with no word on what the lesson is about:

> Run `lab 05/L01 cfa=rggb method=bilinear,malvar`. Compare `zipper.png` and the PSNR table.

After: one to three sentences on what it teaches, then the command.

> 🎯 **Today: demosaicing.** A camera sensor records only one color per pixel, in a Bayer pattern of red, green and blue. Demosaicing fills in the two missing colors at every pixel to make a full-color image.
> ```bash
> lab 05/L01            # the same raw image through two demosaicing methods
> ```
> Watch `zipper.png`: which method leaves colored fringes along sharp edges?

**The opposite failure: too little explained.** Before (a lesson card that starts a SLAM experiment):

> Today: joint estimation. Run `lab 01/L01`. Compare three noise levels. Keep: a shared landmark ties observations across time.

The learner ran it and got curves and numbers with no idea what was simulated, what the axes meant, how the estimator works, or whether the numbers were good. After (shape, not full text): say what problem is solved and what goes in and out; draw the mechanism (sensor → measurements → estimator → trajectory) and give 6 numbered steps of the algorithm; name the real dataset and the real command; add a reading guide ("blue = estimated path, black dashed = ground truth, ATE RMSE in metres = typical distance between them, lower is better, published value for this sequence is about X"); ask for a prediction; run; then walk through the figure piece by piece. That is 500–700 words and two pictures, and every sentence earns its place.

## Lesson card shape (≤ 700 words of prose)

````
# 03.L01 Title as a question
🎯 Today: <topic>. One to three plain sentences: what it is, what problem it solves, what goes in and out.
![map](../../figures/map_L01.png)
One sentence: where this sits and what you'll find out.

## How it works
![concept diagram](figures/concept.png)
Numbered steps or plain sentences: inputs, steps, outputs, why it is built this way.
```text
pseudocode (<= 20 lines)
```

## Data and setup
Which real data and real code; what changes between the settings.

## Reading guide
| What you will see | What it is | Good looks like |

## Predict
One question.

## Run
`lab <MM>/L<nn>`  (about N min)    Try: `lab <MM>/L<nn> knob=value` → <what changes>

## Takeaway
Two to four sentences: the ideas, why the result came out so, where else they apply.
<details><summary>math · why · source</summary> ... depth on demand ... </details>
<sub>Sources: ... · Data: ... · New terms: ... · Transfers to: ...</sub>
````

## Module primer shape (≤ 900 words of prose)

````
# 03 primer — Title
![where this module sits](figures/big_picture.png)
🎯 This module: <topic>. One or two sentences: what it does, which box of the course map, what goes in and what comes out.

## The fundamentals
- **General idea 1**: one or two plain sentences, true beyond this codebase.

## How it works
![the key algorithm](figures/concept.png)
Plain numbered steps, a worked example with real numbers if useful, pseudocode.
**In the code:** which file implements which step.

## The data
The real dataset and why.
**In the lessons:** L01 shows idea 1; L02 ideas 2 and 3.
<sub>More on any idea: deeper <idea> · Questions welcome · Sources: ...</sub>
````

Module 01's primer is the guided tour (≤ 1500 words): whole-method pseudocode, then one stop per box (input → output with a real example, the algorithm in plain words, a diagram, the design idea), then the end-to-end run on real data with a table "box → which output shows it". See `.agents/skills/plan-module/assets/TOUR_TEMPLATE.md`.

## Chat turn shape (≤ 300 words, plus pictures and code)

- Primer or tour: several messages, each ≤ 350 words with its picture: (1) map, 🎯 intro, fundamentals; (2) how it works, with the diagram; (3) data, lesson table, invitation to ask. Tour: two or three stops per message.
- Lesson turn 1 (≤ 350): the 🎯 intro, map image, one placing sentence, the concept diagram and the mechanism.
- Turn 2: the real data and setup, the reading guide, a prediction prompt, the command.
- Turn 3: their result (annotated picture), a walk-through in reading-guide order, one check question, 1–2 tweaks.
- Turn 4: takeaway, transfer line, an invitation to ask, `✅ Progress saved`.

Every turn ends with exactly one `▶ Next:` line. Say, early in a course and at the end of each lesson, that questions are welcome and expected.
