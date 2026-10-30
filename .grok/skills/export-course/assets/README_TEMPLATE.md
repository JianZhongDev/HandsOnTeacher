# <title>

**A short, hands-on course taught by your AI coding agent.** You learn by running real experiments, changing them, and building your own versions, not by reading long pages.

<overview>

## Quick start

1. **Clone this repository** and open the folder in an AI coding agent. Codex, Claude Code, Gemini CLI, Antigravity, Grok Build and Trae load it by themselves; with other agents (for example Doubao Work), start with "Read AGENTS.md in this folder and follow it for this whole session."
2. **Type `start-course`** with your agent's skill prefix (`$start-course` in Codex, `/start-course` in Claude Code). The agent gets the codebase, sets up an isolated environment (asking before installing anything outside the course folder), asks a few questions about you, and shows the course map.
3. **Learn.** Each lesson starts in a new session with `teach-lesson continue`. [START_HERE.md](START_HERE.md) lists what to type in every situation.

**You need:** git, Python 3.9+ (or [uv](https://docs.astral.sh/uv/)), an agent that may run terminal commands, and what the codebase itself needs (the agent checks). Windows, macOS and Linux all work; on macOS the command is `python3`.

## What a lesson feels like

- One experiment of 20–40 minutes that teaches 2–4 related ideas; the lesson card has at most 200 words.
- One run compares several settings side by side, so you see what a change does.
- For design topics, you write your own small version first, then compare it with the codebase's.
- Type `math`, `deeper`, `why` or `source` for depth; `faster` for shorter messages.

## Sources

<sources>

The codebases are not copied into this repository: setup fetches them. Each keeps its own license.

## How it is built

The course was designed with [HandsOnTeacher](https://github.com/JianZhongDev/HandsOnTeacher). The curriculum is in `courses/<course>/COURSE.md`; lessons are built for each learner when they reach them. License: see [LICENSE](LICENSE) and [CREDITS.md](CREDITS.md).
