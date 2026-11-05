---
name: make-visual
description: Choose and produce the right teaching visual for a hands-on course - course and module maps, process diagrams, pseudocode, side-by-side comparisons, slider pages and result plots that answer one question. Use whenever a lesson or answer explains a process, structure, timing or a measured result.
---

# Make a teaching visual

A visual must save the learner reading **and make the idea clearer than words can**. Draw by default: if a paragraph describes how something flows, is arranged, is shaped (geometry), or changes over time, it should be a picture, usually with a few words of pseudocode beside it. Every lesson has a concept diagram of its mechanism and an annotated result figure; every primer has the course map plus a diagram of its key algorithm; every guided-tour stop has a picture of its box. Show the image in the chat itself, not only a path.

## What to draw for common explanations

| The idea is… | Draw… |
|---|---|
| a pipeline or system | boxes and arrows, each arrow labelled with the data that flows (type, rate, units) |
| an algorithm with a loop or branches | flowchart or state diagram, plus pseudocode; mark where the loop repeats |
| geometry (cameras, frames, projection, vectors, transforms) | a sketch with axes, labelled points, angles and the quantity being computed |
| an optimisation or estimation | the objective as a picture: residual terms as springs or arrows between variables (a factor graph), a window sliding in time, a cost curve with the solver's steps |
| state evolving over time | a timeline with one row per actor and labelled events |
| a trade-off between settings | a curve with the settings marked, or small multiples on the same axes |
| a real result | the real figure, annotated: arrows or boxes on the region to look at, a title that states the takeaway, units on axes, reference (ground truth or baseline) drawn in a distinct style |
| a small worked example | a table with step · state before · operation · state after, using real numbers from the lab |

Make them with matplotlib (patches, arrows, annotations), `handson.flow_diagram` / `layer_diagram`, or a Mermaid block when plotting is unavailable. Generated schematics are labelled "schematic" in the caption.

## Pick the form

| You are explaining | Use | How |
|---|---|---|
| The whole subject (course map) | layer stack for layered systems, flow diagram for pipelines and algorithms | `ho.layer_diagram(...)` or `ho.flow_diagram(...)`, labelled with module numbers; redrawn with one box highlighted for each module's primer |
| Where today's topic fits | module map, today highlighted | `ho.flow_diagram(..., highlight=[i])`, one per lesson (made by `plan-module`) |
| A process or algorithm (steps in order) | flow diagram **or** pseudocode | `ho.flow_diagram`; or a code block with plain names and comments |
| What happens over time | timeline with labelled blocks | matplotlib bars on a time axis, one row per actor or process |
| Data layout (records, buffers, tensors, tables) | labelled grid | matplotlib rectangles; or a small Markdown table with symbolic entries |
| What the system does under 2–5 settings | side by side, same scale | `ho.side_by_side` of screenshots or plots; one plot with all settings on the same axes |
| A measured result | 1–3 panel plot | units on axes, a title that states the takeaway, key events marked |
| Something that computes in seconds | slider page | `ho.slider_page` → `explore.html` |

## Rules

- **Concept before result.** Show how it works before showing what happened.
- **Set up before showing.** One sentence each: what question this answers, what the axes, lines, colours and markers are, where to look first. After showing, walk through it in that order; never post a figure and ask the learner to interpret it.
- **Plot against a reference.** Results include the ground truth, baseline or published value so the learner can see "good" and "bad".
- **Label on the picture**, not only in a legend or the text. Words, not variable names, plus units.
- **One message per figure.** At most 3 panels. Remove colors and decorations that carry no meaning.
- **Same scale for comparisons.** Shared axes, same crop, same order of settings everywhere.
- **Mark the key event** (failure, timeout, cache miss, fall) the same way in every picture and table.
- **Label schematics as schematics.** A drawn illustration is not measured evidence.
- **Look at it** after generating (open the image), and fix overlaps, clipped text and unreadable fonts.
- **Mind licenses.** Screenshots or renders of the codebase's assets may carry its license: keep them in `results/`, and check before putting them anywhere shared.
- Keep the generating script next to the figure: `<module>/figures/` for concept figures, the lab for results.

## Format notes

- PNG renders everywhere: lesson pages, GitHub, and most agent chats as `![alt](path)`. It is the default.
- Mermaid blocks are fine for quick flowcharts when Python plotting is not available; some Markdown previews need an extension to render them.
- Pseudocode beats prose for algorithms: under about 20 lines, real control flow, comments say *why*.
- Plain-text arrows (`request -> router -> handler`) are fine for a one-line chain in chat.
