# Lab patterns: where the experiments are

A lab needs an **experiment surface**: something the learner changes, plus an observable behavior that changes as a result, fast enough to compare several settings in one run. This page lists common surfaces by kind of codebase. Use it while surveying a codebase and while building labs.

Every pattern follows the same shape: **one run, 2–5 settings, side by side, a small table of observable metrics, one picture.**

| Kind of codebase | Change | Observe | Typical picture |
|---|---|---|---|
| **Library / API** | arguments, input data, which function or class, a subclass that overrides one method | outputs, errors, run time, memory | table of outputs per setting; timing bar chart |
| **Simulation / physics / robotics** | physical parameters, controller gains, noise, delays | trajectories, failures (falls, crashes), success rate | side-by-side GIFs or trajectory plots; robustness curve |
| **Machine learning / training** | data, loss or reward terms, hyperparameters, model size | learning curves, evaluation metrics, failure cases | training curves on one axis; before/after examples |
| **Web service / backend** | request load, payload, configuration, a middleware or handler | status codes, latency, logs, database queries | latency histogram per setting; request timeline |
| **Frontend / UI** | component props, state, styles, data size | screenshots, render time, accessibility checks | screenshots side by side |
| **CLI / tool** | flags, input files, environment variables | output, exit code, run time, files produced | table of runs; diff of outputs |
| **Data pipeline / database** | input data, schema, indexes, batch size, query | row counts, run time, query plans, memory | table + timing plot; query-plan excerpt |
| **Compiler / interpreter / parser** | source snippets, optimization flags, grammar rules | generated output, errors, speed | input → output pairs side by side |
| **Systems / concurrency / networking** | thread count, buffer sizes, timeouts, injected faults | throughput, latency, deadlocks, error rates | throughput vs setting curve |
| **Algorithms / data structures** | input size and shape, the algorithm variant | operations count, time, correctness | scaling plot (size vs time) |

## Real data first

Experiments use real data that suits the topic, found by searching for the field's standard benchmarks and the codebase's own examples (record source, licence, size, checksum; ask the learner before downloading):

- vision and SLAM: EuRoC MAV, KITTI, TUM RGB-D / TUM-VI sequences; speech and audio: LibriSpeech; NLP: standard corpora on the Hugging Face hub; recommenders: MovieLens; tabular ML: UCI or Kaggle sets; web services: the codebase's own load-test examples and public traces; databases: TPC-H / public sample databases; compilers: the codebase's test suite and real open-source files. These are examples; search for the right one.
- Use a short real excerpt when the whole set is slow (the first 60 seconds of a sequence, 10,000 rows), and say so.
- Compare against a **reference**: ground truth, a published result, or a simple baseline. Metrics use the field's standard names and units.
- **Synthetic data** only for what real data cannot give (known ground truth for a controlled ablation, an injected fault). It comes after a real-data run, is labelled synthetic in the first line, and never stands in for the real system.
- **The real system, not a re-implementation.** If the real codebase is hard to run (old OS or libraries, ROS, GPU), solve that in `setup-environment` (container, WSL, port); do not teach with a toy copy.

## Big-picture labs (Module 01)

Module 01 shows the whole subject working, one box of the course map at a time. Three patterns work in almost any codebase:

- **Trace one input through every box:** capture what each stage receives and hands on, one row per box (a request through router, handler and database; an instruction through fetch, decode and execute).
- **Change or switch off one stage** and watch the effect downstream: no cache, an optimizer pass disabled, a robot without its controller.
- **Time each stage** of one end-to-end run: one bar per box shows where the time goes.

Label every output with the box of the course map it belongs to, and give each a reading guide (what it is, unit, reference, what good looks like). The end-to-end run of the real system on real data is the Module 01 experiment, never a simplified model of it.

## Ways to change behavior without editing the codebase

The codebase is read-only for lessons. In order of preference:

1. **Public knobs:** arguments, configuration objects or files, flags, environment variables.
2. **Composition:** wrap a function or class, subclass and override one method, pass a custom callback or plugin.
3. **Configuration copies:** copy a config file into the lab folder, edit the copy, point the program at it.
4. **Runtime patching inside the lab:** replace one function for the duration of the run (`unittest.mock.patch`, monkeypatching). Say so in the lab's docstring.
5. **A copy of one file** in the lab folder, loaded instead of the original, when nothing else works. Keep the diff small and show it.

## Making it fast

- Use the smallest *real* input that still shows the effect: a 100-row sample of the real table, a 60-second excerpt of the real sequence. Runs of up to 10 minutes are fine.
- Cache slow, unchanged steps (a trained model, a built index) in the course's `_shared/` or the lab's `cache/`, keyed by everything that affects them.
- Run settings in parallel when the codebase supports it (vectorized environments, process pools).
- If an effect only appears after a long run, either pre-compute once and cache it, or ask the learner before a run over 10 minutes.

## Making it visible

- Prefer what a user or operator would notice (the robot falls, the page loads in 3 s, the query returns wrong rows) over internal values.
- Put settings side by side in one picture, with the same axes and scales.
- Mark the moment of the key event (failure, timeout, cache miss) in both the picture and the table.
- If the codebase produces images or animations, keep them in the lab's `results/` folder and check their license before sharing.

## Build-first tasks (`your_turn.py`)

Good build tasks are small (5–30 lines), have a working default, and plug into a real slot of the codebase:

- a reward or loss term, a scoring or ranking function, a cache policy, a retry or backoff rule, a request handler, a validation rule, a parser rule, a scheduling policy, a feature transform.

The lab runs the learner's version next to the codebase's own and shows the difference in behavior. The lesson then explains the codebase's choice and its reasons.
