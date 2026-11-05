# Start here

Your AI coding agent is the teacher. You never need to remember lesson numbers or long prompts: each course keeps track of where you are in `courses/<course>/STATE.md`, and every message from the agent ends with a **▶ Next** line that tells you exactly what to do.

Write skill names with your agent's prefix: `$` in Codex, `/` in Claude Code, Grok Build and Antigravity; in Trae and other agents just name it ("use create-course").

## 0. Open this folder in your agent

| Agent | What to do |
|---|---|
| Codex, Claude Code, Gemini CLI, Antigravity, Grok Build | open the folder; the agent finds `AGENTS.md` and the skills by itself |
| Trae (including the former Trae Work) | open the folder as a project; the rule in `.trae/rules/` and the skills in `.trae/skills/` load by themselves |
| Doubao Work, or any other agent | set this folder as the workspace, and start each session with the message below |

```
Read AGENTS.md in this folder and follow it for this whole session. Then: create-course
```

Replace `create-course` with whatever you want to do, for example `teach-lesson continue`. The agent must be allowed to run terminal commands (git, Python, the lab launcher); if it cannot, it will ask you to run them and paste the output.

## 1. Create a course (once per course)

Open this folder in your agent and type:

```
create-course
```

Then say what you want to learn and list your sources: one or more codebases (Git URLs or local folders), and any documents (PDF, Word, Markdown, slides, notebooks) or web pages to draw on. The agent asks a few short questions, proposes a setup plan, and shows you the course map.

Got a course someone shared (or exported)? Open it in your agent and type `start-course` instead.

## 2. The lesson loop

The course runs top-down: Module 01 is a guided tour of the whole subject and runs the real system on real data; each later module zooms into one part, starting with an explanation of its key algorithm; optional bonus modules go deeper after the core. **Your questions are what make this work: interrupt whenever something is unclear.**

```
 new agent session ──► teach-lesson continue
                            │
                            ▼
   Primer  (first lesson of a module) where it sits, the fundamentals, and how its key algorithm works, with diagrams
                            │   reply "start"   (or "deeper <idea>" for more on any idea)
                            ▼
   Turn 1  what it teaches + how it works (diagram)
                            │   reply "go on" or ask anything
                            ▼
   Turn 2  the real data, the reading guide, your prediction, the command
                            │   you run:  ./lab.sh 03/L01   (or edit your_turn.py first)
                            ▼
   Turn 3  read your results together, piece by piece + one or two tweaks
                            │   you run:  ./lab.sh 03/L01 size=5000
                            ▼
   Turn 4  takeaway + where it applies elsewhere   (progress is saved)
                            │
                            ▼
                close the session; next lesson = new session
```

- A lesson is one experiment of 20–40 minutes on real data. Its card (`LESSON.md`) explains the mechanism and every output; further depth is folded, or ask for it.
- Use **one new session per lesson**, opened in this folder. That keeps the agent focused.
- Run labs from the course folder: `./lab.sh` on Linux and macOS, `.\lab` on Windows.

## What to type

| Situation | Type |
|---|---|
| Start a new course | `create-course` |
| Start a course someone shared with you | `start-course` |
| Add a document or web page to a course | `ask add <file or URL> to the course materials` |
| Start or continue the current course | `teach-lesson continue` |
| You ran the lab | `I ran it` (add what you noticed) |
| You want the agent to run it | `run it for me` |
| You tried a different setting | `I ran size=5000` |
| Finish the current lesson | `wrap up` |
| A question about the current lesson | just ask in the same session |
| A question about anything else in the course | new session: `ask <your question>` |
| Slower, or shorter messages | `slower`, `faster` |
| You do not understand something | `explain again`, `show me a picture`, or just ask why |
| You predicted before running | `I ran it, I expected ...` |
| The math, a derivation, the design reasons, the source code | `math`, `deeper`, `why`, `source` |
| More on a fundamental from the module primer | `deeper <idea>` |
| An optional bonus lesson or module | `teach-lesson bonus` |
| Skip a lesson | `skip` |
| You have several courses | name it: `teach-lesson continue <course>` |
| You must stop mid-lesson | `session-handoff pausing mid-lesson` |
| The lesson is finished but the agent did not say "progress saved" | `session-handoff this lesson is finished` |
| The environment broke | `setup-environment repair` |
| Share your course as its own repository | `export-course` |
| The teaching does not suit you | say what is wrong; the agent records it and adapts |

## Lab commands (in the course folder)

```
lab list                  # your labs
lab 03/L01                # run a lab with default settings
lab 03/L01 help           # settings you can change
lab 03/L01 size=5000      # change one thing (results kept per setting)
lab check                 # check the runtime
```

`lab` means `./lab.sh` (Linux, macOS, WSL) or `.\lab` (Windows). Results land in each lesson's `results/<settings>/` folder: open the `.png` files, and `explore.html` in a browser when a lab writes one.
