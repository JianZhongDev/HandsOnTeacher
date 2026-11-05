# <MM>.L<nn> <The experiment's question, as a short question>

🎯 **Today: <the topic, by its general name>.** <One to three plain sentences: what it is, what problem it solves, what goes in and what comes out. Define any term it needs on the spot. No file, function or knob names.>

![Module map](../../figures/map_L<nn>.png)

<ONE sentence: where this sits in the module and what you will find out.>

## How it works

![<concept diagram: the mechanism, labelled>](figures/concept.png)

<The mechanism in plain steps, 4-8 short sentences or a numbered list: what goes in, what each step does, what comes out, and why it is built this way. Define each term once.>

```text
# Pseudocode (under ~20 lines, real control flow; comments say why). Delete if no algorithm.
```

## Data and setup

<Which real data (name, source, licence, size, how many seconds/frames/rows are used) and which real part of the codebase the lab runs. What changes between the settings being compared, and why those settings. If any part is synthetic, say so here in the first sentence and why.>

## Reading guide

| What you will see | What it is | Good looks like |
|---|---|---|
| <table column / axis / line / colour> | <meaning, unit, what it is compared with> | <direction or value range that means "works">  |

## Predict

<One question: "What do you expect to happen to <metric> when <change>?" Answer in a sentence in chat; no grading.>

## Run

```bash
lab <MM>/L<nn>      # about <N> min; prints a summary table and writes compare.png
```

**Try:**
- `lab <MM>/L<nn> <knob>=<value>` → <what to look for>
- Edit `your_turn.py`: <the design change to try> → <what to look for>

## Takeaway

<Two to four sentences: the 2-4 ideas, said plainly, and why the result came out this way. Then: where the idea appears outside this codebase.>

<details><summary>math · why it is designed this way · source</summary>

<Depth on demand: derivation with a symbols table, worked numbers, the codebase's design rationale, source files, caveats.>

</details>

<sub>Transfers to: <two places outside this codebase>. Sources: <docs / papers / source files, one line>. Data: <dataset and licence>. New terms: <term — plain definition>; added to GLOSSARY.md. `lab` = `./lab.sh`, or `.\lab` on Windows. Questions at any point are welcome: ask, or reply `explain again`.</sub>
