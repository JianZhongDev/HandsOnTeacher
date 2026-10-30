---
name: make-visual
description: Choose and produce the right teaching visual for a hands-on course - course and module maps, process diagrams, pseudocode, side-by-side comparisons, slider pages and result plots that answer one question. Use whenever a lesson or answer explains a process, structure, timing or a measured result.
---

# Make a teaching visual

A visual must save the learner reading. If a paragraph describes how something flows, is arranged, or changes over time, it should be a picture or a code block.

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
- **Set up before showing.** One sentence each: what question this answers, where to look first.
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
