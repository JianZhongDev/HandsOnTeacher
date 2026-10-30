---
name: export-course
description: Package a finished course design as a standalone repository that others can clone and learn from with any AI agent - the curriculum, course helpers, skills, method and tools, reset to a fresh start, with codebases fetched by setup rather than copied. Use when the learner wants to share or publish a course, or turn it into its own repository.
---

# Export a course

Result: a folder that works like `LearnRLWithMicroDuck`: someone clones it, opens it in their agent, types `start-course`, and gets the same course built fresh for them. Publishing it is the learner's decision; never push or publish without their explicit yes.

## 1. Check the course is ready to share

- `COURSE.md` has the full curriculum and the course map; `SURVEY.md` is current.
- The course helpers in `_shared/` work: `lab check` passes.
- Every repo source in `course.json` has a public URL and a commit. A local-only codebase must be published first, or the course cannot be set up elsewhere.
- Licenses: each codebase's license allows the intended use. Reference documents are exported only as an index with links, unless their license allows redistribution.
- No personal data in course files: names, emails, local paths, private notes. `NOTES.md` and the learner's progress are not exported.

## 2. Decide what to include (ask in one message if unclear)

- **Lessons as examples?** Built lessons can be included as a preview in `examples/<course>/` (`--lessons-as-examples`). Learners still get every lesson built fresh; examples are never their progress.
- **Reference documents?** Only with `--include-materials` and permission to redistribute.
- **Large artifacts** (trained models, datasets over 20 MB) are left out: the course should regenerate them, or download them during setup.

## 3. Export

```bash
python tools/export_course.py <course> <destination-folder> [--lessons-as-examples] [--include-materials]
```

Fix every WARNING it prints, then re-run into a new empty folder.

## 4. Review the result

- Edit the generated `README.md` for people: what they will learn, what a lesson feels like (one real picture from the course, if its license allows), quick start, credits. Keep it short.
- `LICENSE`: the method is MIT; the learner adds their own name for the course content. Credit every codebase, document and paper in the README's Sources section and in `CREDITS.md`.
- In the exported folder: `python tools/check_repo.py` and `python tools/lesson_stats.py --all` pass.
- Best test: a fresh start in the exported folder (`start-course`) on a clean machine or a new folder, up to the first lab.

## 5. Hand over

Tell the learner where the folder is, what was left out and why, and the commands to publish it themselves (`git init`, first commit, push to a new repository). End with one `▶ Next:` line.
