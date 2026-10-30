# Writing guide

The learner reads every word you write. Make it cheap to read.

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
10. **Cut 40%** after drafting. Then check the word budget (card ≤ 200, chat turn ≤ 120).

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

**Opening a lesson.** Before: three paragraphs on the history and motivation of caching, then the lab command at the end.

After:

> ```bash
> lab 03/L01            # same 1,000 requests with no cache, LRU, and your policy
> ```
> Watch `latency.png`: which policy keeps the slow requests rare? Then open `your_turn.py`.

## Lesson card shape (≤ 200 words of prose)

````
# 03.L01 Title as a question
![map](../../figures/map_L01.png)
One sentence: where this sits and what you'll find out.

```python
# the experiment, 5-15 lines the learner can read and edit
```

🔧 Run: `lab <MM>/L<nn>`  (about N min)   Watch: <one thing>
Try:   `lab <MM>/L<nn> knob=value` → <what changes>

**Takeaway:** one or two sentences.
<details><summary>math · why · source</summary> ... depth on demand ... </details>
<sub>Sources: ... · New terms: ... · Transfers to: ...</sub>
````

## Chat turn shape (≤ 120 words)

- Turn 1: map image, one sentence of context, the command, what to watch.
- Turn 2: their result (picture), 2–3 sentences on what it shows, 1–2 things to try.
- Turn 3: two-bullet takeaway, one transfer line, `✅ Progress saved`.

Every turn ends with exactly one `▶ Next:` line.
