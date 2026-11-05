---
name: ask
description: Answer a learner's question about a course - any module, lesson card, lab result, term, or how the codebase works - without starting or advancing a lesson, using a quick demo when running something answers best; also adds a new document, web page or repository to the course. Use when the learner invokes ask, asks a question outside an active lesson, or offers a new source.
---

# Answer a course question

The learner wants an answer, not a lesson. Do not advance the course and do not change `STATE.md`'s next action.

## Find the context first (quietly)

1. Read the course's `STATE.md` to see where the learner is.
2. Find the material the question refers to: `GLOSSARY.md` for terms; the module's `MAP.md`, the lesson's `LESSON.md` and `NOTES.md` for topics; the learner's `results/` folders for results; `SURVEY.md`, the codebase checkouts in `sources/` (read-only) and the reference texts in `materials/text/` for how things actually work. Cite a document by name and page.
3. If the question depends on a lesson the learner has not reached, answer briefly at their current level and say which upcoming module covers it.

## Answer

- **Lead with the direct answer** in 1–3 plain sentences. Then only the context needed, starting with where it sits in the big picture (which box of the module or course map).
- **Show it.** Default to a picture for anything about a process, structure, geometry or a result: reuse an existing figure or draw a quick diagram (`make-visual`), and show the image in the chat. Add pseudocode or a small worked example with real numbers when it clarifies.
- **Explain, do not just point.** If the question reveals the learner does not understand a result, walk through the figure or table piece by piece (what each axis, line and number is, and why it came out so) before anything else. Do not answer "see the lesson".
- **If running something answers it best**, write a small script with the course kit, save it with its outputs in `courses/<course>/questions/<YYYY-MM-DD>-<topic>/`, run it, show the result, and give the rerun command (`lab run ...`). Keep it to a few minutes.
- If an earlier lesson card was wrong or unclear, say so plainly, fix the card, and note the fix.
- **A new source** (a document, web page or repository the learner wants included): store it (`python tools/extract_text.py <course> <file or URL>`, or clone a repository to `sources/`), add it to `course.json` and `materials/INDEX.md` with its license, and say in one line which modules it affects. Modules not yet planned use it automatically; offer to revise a planned one.
- Be as long as a clear answer needs (usually under about 250 words plus a picture or code block). Offer `math`, `deeper`, `why`, `source` (`explain-deeply`) for more.
- Welcome follow-ups: end by saying what else they may ask.
- End with `▶ Next:`, for example: `ask a follow-up, or start a new session and type teach-lesson continue to resume at <lesson>.`

## Record

Append a short dated entry to the relevant module's `NOTES.md`: the question (verbatim if short), the answer's key point, artifact paths, any card fixes. Add new terms to `GLOSSARY.md`. If the question shows a lesson was confusing, add one line to `FEEDBACK_LOG.md`. Do not record the learner as having understood the answer.
