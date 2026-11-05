---
name: session-handoff
description: Record a finished lesson, experiment or pause so the next session can continue without chat history - update the course's STATE.md, the module NOTES.md and MAP.md status, COURSE.md module status, GLOSSARY.md, TODO.md and learner preferences. Use at the end of every lesson or substantive experiment, and when the learner pauses mid-lesson.
---

# Hand off to the next session

Files are the only memory between sessions. Keep them short and accurate.

## 1. `courses/<course>/STATE.md` (rewrite the "Now" section; the file stays under about 40 lines)

- Active module and lesson, whether the module's primer was delivered, and the lesson status (planned / ready / delivered / learner ran lab / finished / skipped). Bonus work: say so, and keep the next core action.
- **Next action:** one concrete sentence, for example "Deliver 03/L02: card and lab are ready and tested", or "plan-module for Module 04".
- Open learner questions, verbatim if short.
- History does not go here; it goes in NOTES.

## 2. `<module>/NOTES.md` (append, never rewrite history; under about 150 words per entry)

```
## YYYY-MM-DD — L<nn> <title>
- Question / ideas / transferable idea:
- Delivered: card, lab, figures; what was verified and how
- Learner did: commands they ran, settings they changed, questions they asked (only what happened)
- Results: key numbers with units, artifact paths
- Source facts used: file:line
- Problems / feedback: what confused the learner and what was changed
```

## 3. Other files

- `<module>/MAP.md`: the lesson's status column. `COURSE.md`: the module's status column.
- `GLOSSARY.md`: new terms, one plain line each, plus the lesson where introduced.
- `<module>/TODO.md`: parked side topics and unfinished work.
- `FEEDBACK_LOG.md`: one dated line if the learner corrected the teaching.
- `LEARNER.md` → Preferences: lasting preferences you learned (one dated line each), such as `faster` or a language change. Also record in the module's `NOTES.md` what the learner predicted, asked and answered (never claim mastery), so the next session can pick up unanswered questions.

## Tell the learner

End with `✅ Progress saved.` and a `▶ Next:` line. After a finished lesson: `close this session, start a new one in this folder, and type teach-lesson continue`. After a pause: `next time, start a new session and type teach-lesson continue; it resumes at <turn>`. After the capstone (the last core module): offer the bonus modules from `COURSE.md` in one line, or the capstone review, or a new course.

## Rules

- Record only what actually happened. A teacher's explanation or a successful command is not learner mastery.
- Plain sentences, not compressed tokens.
- Never paste this record into the chat. The learner sees only `✅ Progress saved.` and the `▶ Next:` line.
