---
name: explain-deeply
description: Give depth on demand in a hands-on course - a formula or derivation, an algorithm step by step, more on a fundamental idea from a module primer, the reasons behind a design decision, or a walkthrough of the codebase's source - so a beginner can follow every step. Use when the learner types math, deeper, deeper <idea>, why or source, and for the folded details block of a lesson card.
---

# Explain in depth

Depth beyond the lesson's own mechanism is on demand (`method/TEACHING_RULES.md`, rules 4 and 9). The main lesson path already explains the mechanism with a diagram; this skill goes further when the learner asks, and fills the `<details>` block of a card. Inside those, never cut steps, and draw a diagram or a worked table whenever the explanation has more than three steps (`make-visual`). Offer a picture first if the learner just says "I don't get it".

The learner's difficulty is rarely the math or the code itself. It is **unexplained structure**: numbers before the formula, symbols with no meaning, steps with no purpose, files with no map.

## `math`: a formula or calculation

1. **Purpose** in one sentence: what this tells us and where it sits in the big picture.
2. **Formula in symbols**, then a table of every symbol: meaning, units, shape (scalar, vector, matrix, table).
3. **Why it has this form**, in 1–3 sentences: what each term does; what happens at extreme values.
4. **The example**, introduced before its numbers: where each value comes from (measured in the lab, from a config file, or hand-picked for readability).
5. **Expand symbolically, then substitute**, then each arithmetic step. Keep signs, denominators and rounding visible.
6. **Meaning of the result**, and what it feeds into next.

For a large computation, work one small complete case and say it is a small case.

## `deeper`: an algorithm or mechanism

1. Purpose and inputs/outputs in one sentence.
2. The whole loop first (pseudocode, under 20 lines), then each step.
3. Trace one small concrete input through every step in a table: step · state before · operation · state after.
4. What stored state (tables, buffers, caches) holds between steps, and when it is reset.
5. Where it can go wrong: edge cases, and what the lab would show if they happened.

## `deeper <idea>`: a fundamental from a module primer

The learner wants the general concept, not yet this codebase's code.

1. The idea in one sentence, and where it sits on the course map.
2. The problem it solves, and how it works in general: a diagram or pseudocode under 20 lines; the classic alternatives.
3. One small worked example, traced or computed step by step.
4. Where the codebase implements it (file, a short quote) and which lesson makes it visible.
5. Where to read more: a chapter, paper or doc page from `materials/text/`, cited by page.

## `why`: a design decision

1. The decision in one line, and the alternatives the authors could have chosen.
2. The authors' reason, quoted with its location (comment, doc, issue, commit message, a reference document's page in `materials/text/`), or "not written down" plus your best explanation labelled as such.
3. The trade-off: what the choice gains and costs. If the learner built their own version in `your_turn`, compare against it directly.
4. Where the same decision appears elsewhere, and what other projects chose.

## `source`: a walkthrough of the code

1. A map first: the 3–6 files or functions involved and how control flows between them.
2. Then each piece: path and line range, a short quote (only the lines needed), and what it does in one sentence.
3. Link it to the lesson: which knob or behavior from the lab this code produces.

Quote only what is needed and respect the codebase's license. Never paste whole files.
