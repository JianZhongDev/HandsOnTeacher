# HandsOnTeacher

**Turn any codebase into a short, hands-on course, taught by your AI coding agent.**

Tell your agent what you want to learn and what to learn it with: one or more repositories, plus any papers, documents (PDF, Word, Markdown, slides, notebooks) or web pages you trust. It reads them all, designs a compact course around the skills that transfer beyond that repository, sets up an environment on your machine, and teaches you one experiment at a time. You spend your time running, changing and building things, not reading long pages.

```
You:    create-course — I want to understand caching and eviction, using github.com/<someone>/<cache-library>
Agent:  6 modules, about 5 hours. Module 01: run the cache under real load and watch the hit rate…
```

## What learning feels like

- **Big picture first.** Module 01 shows the whole subject as a few boxes and runs it end to end. Each later module zooms into one box: a five-minute primer on the general fundamentals, then experiments with the codebase. Deeper topics come last, as optional bonus modules.
- **One experiment per lesson, 20–40 minutes.** Each teaches 2–4 related ideas. A lesson card opens with what it teaches and has at most 300 words; the rest is doing.
- **You see consequences, not numbers.** One run compares several settings side by side: what the program outputs, how fast it is, when it breaks.
- **You build first, then compare.** For design topics you write your own small version, run it next to the codebase's, then learn why the authors chose theirs.
- **Transferable first.** Each idea is named in general terms, shown in the codebase, and linked to where else it applies.
- **Depth when you ask.** Type `math`, `deeper`, `why` or `source` for derivations and code walkthroughs, `deeper <idea>` for more on a fundamental; `faster` for even shorter messages.
- **Your progress is saved in files**, so you can stop any time and any agent can continue.

## Quick start

1. **Clone this repository** and open the folder in an AI coding agent: Codex, Claude Code, Gemini CLI, Antigravity, Grok Build or Trae load it by themselves. Other agents, such as Doubao Work, work too when your first message points them to `AGENTS.md` (see [START_HERE.md](START_HERE.md)).
2. **Ask for a course.** Type `create-course` with your agent's skill prefix (`$create-course` in Codex, `/create-course` in Claude Code, Grok Build and Antigravity), then say what you want to learn and list your sources: Git URLs or local folders, documents, web pages.
3. **Agree to the setup plan.** The agent proposes how to run the codebase on your machine, in an isolated environment inside the course folder, and asks before installing anything outside it.
4. **Learn.** Each lesson starts in a new session with `teach-lesson continue`. [START_HERE.md](START_HERE.md) lists what to type in every situation.

**You need:** git, Python 3.9+ (or [uv](https://docs.astral.sh/uv/)), an agent that may run terminal commands, and whatever the codebase itself needs. Windows, macOS (Intel or Apple Silicon) and Linux all work. On macOS, git and Python come with Apple's Command Line Tools (`xcode-select --install`), and the command is `python3`. Codebases that need Linux run through WSL on Windows.

## How it works

```
goal + sources ──► create-course: survey ─► environment ─► course helpers ─► curriculum ─► course map
  (repos, docs, URLs)                                                               │
   each module ──► plan-module ──► each lesson ──► teach-lesson ──► session-handoff
               (primer: big picture + fundamentals)   (card + lab + 3 short turns)
```

- **The method is written down.** [method/](method/) holds the teaching rules, the curriculum design process, lab patterns for different kinds of codebases, and a writing guide with before-and-after examples. `.agents/skills/` holds the step-by-step procedures the agent follows.
- **Your repository is never modified.** Each course works on its own checkout in `sources/` and its own runtime in `courses/<course>/.env/`. Labs change behavior through settings, wrappers and patches inside the lab.
- **Top-down curriculum.** Big picture → core modules for the essential parts (ending with a capstone) → optional bonus modules for depth.
- **Lessons are built just in time.** The full curriculum is written at the start; each module's lessons are built and tested when you reach them, so they adapt to how you are doing.
- **Several sources, one course.** Code from one or more repositories drives the experiments; papers, docs and web pages supply concepts and the "why", stored as searchable text with page citations.
- **Shareable.** `export-course` packages a course as its own repository, like [Learn RL with MicroDuck](https://github.com/JianZhongDev/LearnRLWithMicroDuck): anyone can clone it and get the course built fresh for them.
- **Safe by default.** Lab runs up to 10 minutes are fine; the agent asks before longer runs, system-wide installs, paid services, credentials or anything touching real systems.

More detail: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Worked example: [examples/microduck-rl/](examples/microduck-rl/README.md).

## Where it comes from

HandsOnTeacher is the method behind [Learn RL with MicroDuck](https://github.com/JianZhongDev/LearnRLWithMicroDuck), generalized to any codebase. That course's first version was thorough but tedious: long pages, labs that printed numbers, one small idea per lesson. Rebuilding it around short, real experiments made it far more effective, and every rule here comes from that experience.

## Repository layout

```
README.md  START_HERE.md          for you
AGENTS.md  CLAUDE.md  GEMINI.md   for the agent
method/                           teaching rules, curriculum design, lab patterns, writing guide
.agents/skills/                   the procedures (mirrored for Claude Code, Grok Build and Trae)
kit/handson/                      small Python helpers copied into each course's labs
tools/                            course scaffolding and checks (Python standard library only)
examples/                         a worked example course design
courses/                          your courses (personal; ignored by Git; share one with export-course)
sources/                          checkouts of the codebases you learn with (ignored by Git)
```

## Credits and license

MIT License (see [LICENSE](LICENSE)). Sources and acknowledgments: [CREDITS.md](CREDITS.md). AI teachers make mistakes: labs run real code so you can check claims against results; when something looks wrong, ask the agent for its evidence.
