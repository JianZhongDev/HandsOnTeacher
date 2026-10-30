"""Create the folder for a new course. Never overwrites existing files.

    python tools/new_course.py <course> --title "Learn caching with <repo>" \
        --source https://github.com/<owner>/<repo> --source ~/papers/caching.pdf --source https://docs.example.org/guide

<course> is a short folder name: lowercase letters, digits and dashes (for example `caching-with-redis`).
--source may be repeated: Git URLs or local folders (code), local files (PDF, DOCX, Markdown, slides, ...)
and web pages. Each is recorded in course.json with a guessed kind; create-course fills in the rest.

Creates courses/<course>/ with:
    COURSE.md  SURVEY.md  STATE.md  LEARNER.md   from .agents/skills/create-course/assets/
    GLOSSARY.md  FEEDBACK_LOG.md
    course.json                                  sources, runtime and machine facts
    materials/INDEX.md                          the reference library (documents, web pages, notes)
    lab.sh  lab.cmd                              the lab launcher (configured by setup-environment)
    _shared/handson/                             a copy of kit/handson (lab helpers)
    figures/  questions/

Module folders are created later, one at a time, by tools/new_module.py.
Needs only the Python standard library (Python 3.9+).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_ASSETS = ROOT / ".agents" / "skills" / "create-course" / "assets"
LAUNCHER_ASSETS = ROOT / ".agents" / "skills" / "setup-environment" / "assets"
KIT = ROOT / "kit" / "handson"
CODE_HOSTS = r"(github\.com|gitlab\.com|bitbucket\.org|codeberg\.org|huggingface\.co)"


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:48] or "source"


def describe(source: str) -> dict:
    """Guess what a --source is. create-course corrects the guess if needed."""
    s = source.strip()
    if s.startswith("git@") or re.match(r"https?://", s):
        bare = re.sub(r"(\.git)?/?$", "", s)
        is_repo = s.startswith("git@") or s.endswith(".git") or re.fullmatch(rf"https?://(www\.)?{CODE_HOSTS}/[^/]+/[^/]+", bare)
        kind = "repo" if is_repo else "web"
        name = bare.rstrip("/").split("/")[-1] if is_repo else re.sub(r"^https?://(www\.)?", "", bare)
    else:
        path = Path(s).expanduser()
        kind = "repo" if path.is_dir() else "document"
        name = path.stem if kind == "document" else path.name
    return {"name": slug(name), "kind": kind, "role": "", "origin": s, "path": "", "commit": "",
            "license": "", "notes": ""}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("course", help="folder name: lowercase letters, digits and dashes")
    parser.add_argument("--title", required=True, help="course title, for example 'Learn caching with <repo>'")
    parser.add_argument("--source", action="append", default=[],
                        help="a Git URL, local folder, local document or web page; repeat for several")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,48}", args.course):
        raise SystemExit("Course name: 2-49 characters, lowercase letters, digits and dashes.")
    course = ROOT / "courses" / args.course
    today = dt.date.today().isoformat()
    sources = [describe(s) for s in args.source]
    names = [s["name"] for s in sources]
    for i, name in enumerate(names):            # keep names unique
        if names.count(name) > 1:
            sources[i]["name"] = f"{name}-{i + 1}"
    listing = ", ".join(s["origin"] for s in sources) or "(not set)"
    fill = {"<course>": args.course, "<title>": args.title, "<date>": today, "<source>": listing}

    def render(name: str) -> str:
        text = (COURSE_ASSETS / name).read_text(encoding="utf-8")
        for key, value in fill.items():
            text = text.replace(key, value)
        return text

    files = {
        "COURSE.md": render("COURSE_TEMPLATE.md"),
        "SURVEY.md": render("SURVEY_TEMPLATE.md"),
        "STATE.md": render("STATE_TEMPLATE.md"),
        "LEARNER.md": render("LEARNER_TEMPLATE.md"),
        "materials/INDEX.md": render("MATERIALS_TEMPLATE.md"),
        "GLOSSARY.md": f"# Glossary — {args.title}\n\nOne plain line per term, plus the lesson where it was introduced.\n",
        "FEEDBACK_LOG.md": f"# Feedback log — {args.title}\n\nOne dated line per learner correction of the teaching.\n",
        "course.json": json.dumps({
            "schema": 2,
            "course": args.course,
            "title": args.title,
            "created": today,
            "ready": False,
            "sources": sources,
            "runtime": {"kind": "", "env": ".env", "run": "", "lab_file": "lab.py", "check": ""},
            "launcher": {"unix": "./lab.sh", "windows": ".\\lab", "windows_mode": "native"},
            "machine": {"os": "", "arch": "", "accelerator": "", "notes": ""},
            "timings": {},
            "checked": "",
        }, indent=2) + "\n",
    }

    print(("would create " if args.dry_run else "") + str(course))
    for s in sources:
        print(f"  source  {s['kind']:<8} {s['name']:<24} {s['origin']}")
    if args.dry_run:
        return 0
    for sub in ("figures", "questions", "_shared", "materials/text"):
        (course / sub).mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        path = course / name
        if path.exists():
            print(f"keep     {path.relative_to(ROOT).as_posix()}")
            continue
        with path.open("w", encoding="utf-8", newline="\n") as handle:  # LF on every OS
            handle.write(text)
        print(f"create   {path.relative_to(ROOT).as_posix()}")
    for name in ("lab.sh", "lab.cmd"):
        path = course / name
        if path.exists():
            print(f"keep     {path.relative_to(ROOT).as_posix()}")
            continue
        shutil.copyfile(LAUNCHER_ASSETS / name, path)  # byte copy keeps LF (.sh) and CRLF (.cmd)
        path.chmod(0o755)
        print(f"create   {path.relative_to(ROOT).as_posix()}")
    kit = course / "_shared" / "handson"
    if kit.exists():
        print(f"keep     {kit.relative_to(ROOT).as_posix()}")
    else:
        shutil.copytree(KIT, kit, ignore=shutil.ignore_patterns("__pycache__"))
        print(f"create   {kit.relative_to(ROOT).as_posix()}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
