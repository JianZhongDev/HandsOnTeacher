---
name: setup-environment
description: Get a course's codebases running on this machine in an isolated environment inside the course folder (cloning them from course.json when needed), then configure and test the course's lab launcher (lab.sh / lab.cmd) and record everything in course.json. Use during create-course, when course.json is missing or not ready, or when a lab fails because of the environment.
---

# Set up the course environment

Result: the codebase's own quickest example runs, `lab check` passes, and `course.json` says `"ready": true` with the facts below. Nothing outside the course folder and `sources/` changes without the learner's yes.

## 0. Get the code

For every `repo` source in `course.json` without a checkout in `sources/<name>`: clone its `origin` there and check out the recorded `commit` (a course received from someone else arrives without checkouts). If an origin is a local path that does not exist on this machine, ask the learner for the code. Never edit the learner's own copies.

## 1. Learn how the codebase is meant to run (read first)

With several codebases, do this for each, starting with the `primary` one. Read, in this order: the CI workflow (`.github/workflows/`, `.gitlab-ci.yml`, …; the most reliable recipe), the dependency file (`pyproject.toml`, `requirements*.txt`, `package.json`, `Cargo.toml`, `go.mod`, `pom.xml`, …), the README's install section, `Makefile` or task runner, `Dockerfile` or devcontainer. Note the language version, system libraries, hardware needs (GPU, CUDA) and services (databases, queues).

## 2. Check this machine

OS and architecture; on Windows, whether WSL is installed and whether the codebase needs Linux; CPU, memory, GPU; available toolchains (`git`, `uv`, `python3`, `node`, `docker`, `cargo`, `go`, `java`, …). Never assume a tool exists: check.

### macOS notes

- `git` and `python3` (3.9) come with the Xcode Command Line Tools; if missing, `xcode-select --install` opens Apple's installer (ask first). There is no `python` command: use `python3` for `tools/`, or `uv run python`.
- System packages come from Homebrew (`brew install ...`): ask before installing Homebrew or any formula.
- Apple Silicon (`arm64`): no NVIDIA CUDA. PyTorch can use the Apple GPU (`mps`); other GPU-only code runs on the CPU, so size labs smaller. Packages that publish only x86_64 wheels may need Rosetta or a source build: check before promising a lab.
- Docker needs Docker Desktop or a similar app: ask first, and prefer an in-process substitute.
- Command-line tools are BSD versions (`sed -i ''`, `stat -f`): write lab scripts in Python, or in shell that works with both.

## 3. Propose a plan (one short message) and wait for a yes

- Where things go: the runtime in `courses/<course>/.env/` (ignored by Git), the codebases in `sources/<name>`. One runtime serves all of a course's codebases when their dependencies are compatible; otherwise say so and propose separate ones.
- What gets installed there, the rough download size, and how long it takes.
- Anything outside the course folder that needs approval: system packages, a global toolchain, Docker images, WSL, paid or cloud services, credentials. Offer an alternative without them when one exists (a smaller model, SQLite instead of a database server, a mock instead of an API key).

## 4. Build the isolated runtime

Prefer the codebase's own tooling, pointed at the course folder:

| Codebase | Runtime in `courses/<course>/.env/` | `run` for the launcher |
|---|---|---|
| Python | `uv venv .env --python <version>`, then install the codebase's locked dependencies (`uv sync --frozen` with `UV_PROJECT_ENVIRONMENT`, or `uv pip install -r ...`); install the codebase itself non-editable or put it on `PYTHONPATH` | `.env/bin/python -B` (Windows: `.env\Scripts\python.exe -B`) |
| Node | `npm ci` in the checkout (its `node_modules/` stays in `sources/`) | `node` |
| Rust, Go, Java, C/C++ | build with the codebase's tool; redirect build output into `.env/` where the tool allows (`CARGO_TARGET_DIR`, `GOCACHE`, …) | the built binary, or the language runner |
| Needs Linux on Windows | do all of the above inside WSL; set the Windows launcher to forward to WSL | as for Linux |
| Needs services | containers only with the learner's yes; otherwise an embedded or in-memory substitute | |

For Python-based labs, also install `matplotlib` and `Pillow` into `.env` (plots, maps and side-by-side pictures). For other languages, labs may still use Python for pictures if a Python runtime is available; otherwise they write tables and Mermaid diagrams.

Keep caches inside the course where the tool allows it (`UV_CACHE_DIR` is fine to share; model downloads and datasets go under `courses/<course>/.env/` or `_shared/`).

## 5. Configure the launcher

`tools/new_course.py` copied two launchers into the course folder. Edit only their marked "set by setup-environment" block:

- `lab.sh` (Linux, macOS, WSL): `RUN=(...)`, `LAB_FILE`, `CHECK=(...)`, and `PYTHONPATH` or the equivalent for the runtime.
- `lab.cmd` (Windows): `MODE=native` with `RUN`, `LAB_FILE` and `CHECK`; or `MODE=wsl` (with `WSL_DISTRO`) to forward every command to `lab.sh` inside WSL.

Once the course helpers exist (`create-course` step 6), point `CHECK` at `_shared/selftest.py`. Then run `lab check` and `lab list` from the course folder.

## 6. Smoke test and timing

1. Run the codebase's quickest own example or test with the course runtime. Fix problems before teaching.
2. Time one run of the first experiment surface from `SURVEY.md`. Record timings in `course.json` (`timings`).
3. If something only works partly (no GPU, no renderer, a missing service), record it in `course.json` (`machine.notes`) so lessons are sized for it.

## 7. Record

`course.json`: `sources` (for each: path, commit, license), `runtime` (kind, env, run, lab_file, check), `launcher` (unix, windows, windows_mode), `machine`, `timings`, `checked` (date), `ready: true`. Add a short "How to run it" section to `SURVEY.md`. Tell the learner the result in at most three lines, then return to the calling skill.

## Repair

When a lab fails for environment reasons: run `lab check`, read the error, fix inside `.env/` (re-create it if needed), and note the cause in the course's current module `NOTES.md`. Never fix it by editing the codebase checkout.
