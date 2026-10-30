# Courses

Each course the agent creates lives in its own folder here, for example `courses/caching-with-redis/`. The folder holds everything about that course: the curriculum, your progress, labs, results and an isolated runtime. Nothing outside it changes, except the codebase checkouts in `sources/`.

```
courses/<course>/
  COURSE.md       the curriculum: outcomes, modules, status
  STATE.md        where you are and what comes next
  LEARNER.md      your background, goal, time budget, language, preferences
  SURVEY.md       the agent's one-page notes on the codebase
  course.json     sources (codebases, documents, web pages), runtime, launcher, machine
  materials/      documents and web pages you gave, with extracted text in materials/text/
  lab.sh lab.cmd  the lab launcher:  ./lab.sh 03/L01   or   .\lab 03/L01
  GLOSSARY.md  FEEDBACK_LOG.md
  _shared/        lab helpers: the handson kit, plus helpers that wrap the codebase (README.md, selftest.py)
  figures/        the course map
  questions/      small demos made to answer your questions
  NN-<module>/    MAP.md  NOTES.md  TODO.md  figures/  lessons/L<nn>-<name>/
  .env/           the isolated runtime (not in Git)
```

Courses are personal, so Git ignores this folder (see `.gitignore`). To keep a course in Git, for example on your own fork, remove the `courses/*` lines from `.gitignore`. To share a course as its own repository, ask the agent for `export-course`.
