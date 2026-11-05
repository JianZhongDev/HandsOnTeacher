---
name: create-course
description: Turn what the learner wants to learn plus their sources - one or more codebases (Git URLs or local paths), documents (PDF, DOCX, Markdown, slides, notebooks) and web pages - into a complete hands-on course - survey the sources, design a full curriculum of experiment-sized lessons around transferable skills, set up an isolated environment, build course helpers, and show the course map. Use when the learner asks to learn something with a repository or materials, or when no course exists yet.
---

# Create a course

Goal of this session: the learner sees a short, complete curriculum built top-down around what they want to learn (the big picture first, then the essential parts, then optional bonus depth), the code runs on their machine through a small course helper library, and Module 01 is ready to start. The curriculum method is `method/CURRICULUM_DESIGN.md`; read it first.

## 1. Intake (one message)

Ask only for what the learner has not already said, as a short numbered list. They may reply briefly or "skip" for defaults.

1. What they want to learn or be able to do.
2. Their sources: codebases (Git URLs or local paths), documents (PDF, DOCX, Markdown, slides, notebooks, papers), web pages (docs, tutorials, specs). Several of each are fine. Which one matters most?
3. Their background: languages and tools they know, experience with this topic.
4. Time budget (default: a lightning course of about 4–8 hours).
5. Language for teaching (default: the language they write in).

**No codebase given?** The course still needs runnable code. Propose one or two well-known open-source repositories that implement the topic (say why, and check their licenses), or a small codebase you write into the course's `_shared/`. Confirm before going on.

## 2. Create the course folder

Choose a short course name (lowercase, dashes), then:

```bash
python tools/new_course.py <course> --title "<title>" --source <first> --source <second> ...
```

It records each source in `course.json` (`sources`) with a guessed kind (`repo`, `document`, `web`). Correct the kinds and set each `role`: `primary` (the code most experiments use), `supporting` (other code), or `reference` (concepts, theory, official behavior). Fill `LEARNER.md`. Any Python 3.9+ works for `tools/` (`python3`, `py -3`, `uv run python`).

## 3. Gather the sources (never touch the learner's originals)

- **Code from a Git URL:** clone to `sources/<name>` (shallow is fine). **Local Git repository:** `git clone --local <path> sources/<name>` (committed work only; ask before copying a dirty working tree instead). **Local folder without Git:** copy it to `sources/<name>`.
- **Documents and web pages:** `python tools/extract_text.py <course> <file or URL> ...` copies each into `materials/` and writes searchable text with page or slide markers to `materials/text/`. PDFs need `pypdf` or the `pdftotext` program; some Python builds also need `certifi` for HTTPS downloads: `uv run --with pypdf --with certifi python tools/extract_text.py ...`. Agents that read PDFs or web pages natively may read them directly, but still save the text so later sessions can search it. Pages behind a login: ask the learner to save them as files.
- Record for each source: path, commit or retrieval date, and license or terms of use (`course.json`, and `materials/INDEX.md` for documents and web pages). If a license forbids the intended use, stop and tell the learner.

## 4. Survey (time-boxed: read, do not run everything)

Follow `method/CURRICULUM_DESIGN.md` § 2 and fill `SURVEY.md` (one page; the agent's memory of the material): the big picture of the subject in 4–8 boxes (the layers or stages of the knowledge itself, as an expert would draw them, marking which ones the codebase shows), **the key algorithm of every box in 3–6 lines, with its source (paper section, doc page, file)**, the codebase's architecture in 4–8 boxes, concepts (general vs specific), experiment surfaces with run times, design decisions with their reasons, costs and risks.

**Find real data now.** Search the web (use your search and fetch tools) for what the field uses to evaluate this kind of system: the codebase's own example data, the standard public benchmark datasets and sequences, and the published results on them (these become the references labs compare against). List 2–4 candidates in `SURVEY.md` with URL, licence, size, which boxes they exercise, and the published reference numbers. Pick one small primary dataset and, if useful, one harder held-out one. Never plan labs on random or hand-made numbers when real data exists; synthetic data needs a stated reason (rule 5 of `method/TEACHING_RULES.md`). With several sources, also fill the sources map: which source teaches which concept, and which source wins where they disagree (versions, terminology). `method/LAB_PATTERNS.md` lists where experiments usually are.

## 5. Environment

Use `setup-environment`. Present its plan in the same message as the curriculum preview if that saves a round trip, but install nothing before the learner agrees. When it finishes, `course.json` says `"ready": true` and one experiment surface has been timed.

## 6. Course helpers (the course's own kit)

Write a small library in `_shared/` that wraps the primary codebase **and its real data** for labs, so each lab stays 20–60 readable lines. It calls the real codebase; it never re-implements the method as a toy. Include helpers that load the dataset, compute the field's standard metrics against the reference, and draw the standard figures with labelled axes. Typically 3–6 functions: build or load the thing under study, run it with settings, measure the observable behavior, and apply common changes. Example from a robot-learning course: `make_env`, `train(minutes, configure=...)`, `evaluate(policy, test_configure=...) -> falls, speed`, `set_physics(cfg, friction=...)`.

- Document it in `_shared/README.md`: one code block per function with arguments, units and return values, plus measured run times.
- Add `_shared/selftest.py`, which exercises each function on a tiny input in under a minute, and point the launcher's `CHECK` at it. `lab check` must pass.
- Expensive shared artifacts (a trained model, a built index) are made once by a helper and cached under `_shared/`, keyed by what affects them.

## 7. Curriculum

Follow `method/CURRICULUM_DESIGN.md` §§ 1, 3–5. Write `COURSE.md` from its template:

- outcomes (3–6, starting with verbs), split into transferable and codebase-specific;
- course-specific rules: asset licenses, compute facts, domain safety rules (for example "robot renderings stay in `results/`", "runs over 10 minutes need approval");
- the module table in three tracks: Module 01 is the **big picture** (the whole subject, run end to end); **core** modules cover the essential boxes in dependency order and end with the capstone; **bonus** modules hold the deeper or narrower topics, offered after the core;
- one entry per module (track, place in the big picture, big question, primer fundamentals, transferable idea, read, experiments, build task, evidence, outcome, cost, bonus lessons), citing sources;
- the course map: the big picture of the subject, one box per area, plus `figures/pipeline.png` showing what flows between the boxes, labelled with the modules that cover it. Draw `figures/course_map.png` with `handson.layer_diagram` (layered subjects, top to bottom) or `handson.flow_diagram` (pipelines and algorithms, left to right) through `lab run figures/make_course_map.py`, or a Mermaid block if Python plotting is unavailable. Let the script take a box to highlight: `plan-module` redraws it for each module's primer.

Each entry also names the module's **key algorithm** (what the primer will walk through) and its **data** (dataset, excerpt, reference).

Then pilot Module 01's main experiment: **the real system on the real dataset**, end to end (§ 6 of the method). Do not present the course until it ran and its outputs are interpretable. If the real thing cannot run here, resolve it with the learner first (`setup-environment` 6b); do not substitute a toy and continue.

**Prepare just in time.** Write each module's primer and lesson cards when the learner reaches them, so they adapt to the learner's questions. Preparing every lesson up front tends to produce generic cards; if the learner asks for it, still apply the same rules to each.

## 8. Hand over

- `STATE.md`: course created (date), environment summary, next action "plan-module for Module 01".
- Message to the learner (≤ 250 words plus the course map): the promise in one line, a table with one row per core module (module · you will be able to · time), the total time, one line naming the optional bonus modules, the real data and real code the labs use (named, with the setup state), and how the course works (big picture first as a guided tour; each module a primer that explains its algorithm, then experiments on real data: understand, predict, run, read together, tweak).
- **Ask the learner to be an active partner**, in one or two sentences: "Interrupt me any time: ask why, ask what a figure means, say 'explain again' or 'show me a picture', tell me what you want to see. I won't move on while something is unclear."
- End with: `▶ Next: reply "start" to begin Module 01 now, or later open a new session here and type teach-lesson continue.`
- If they reply "start", use `plan-module` for Module 01.

Do not show `SURVEY.md`, the module entries, the reference index or the setup log in chat. Answer questions about them if asked. To share the course later as its own repository, use `export-course`.
