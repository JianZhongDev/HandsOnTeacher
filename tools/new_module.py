"""Create the folder for one module of a course. Never overwrites existing files.

    python tools/new_module.py <course> <NN> <module-name> [--title "Why does the cache miss?"]

Example:  python tools/new_module.py caching-with-redis 03 eviction-policies
Creates courses/<course>/<NN>-<module-name>/ with:
    MAP.md     from .agents/skills/plan-module/assets/MAP_TEMPLATE.md
    PRIMER.md  from .agents/skills/plan-module/assets/PRIMER_TEMPLATE.md (place in the big picture + fundamentals)
    NOTES.md   dated history, with a "module started" entry
    TODO.md    parked side topics
    figures/   module map and concept figures, with the script that makes them
    lessons/   one folder per lesson (LESSON.md, lab file, your_turn file), made by teach-lesson

Needs only the Python standard library (Python 3.9+).
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / ".agents" / "skills" / "plan-module" / "assets"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("course")
    parser.add_argument("number", help="two-digit module number, e.g. 03")
    parser.add_argument("name", help="module folder name: lowercase letters, digits and dashes")
    parser.add_argument("--title", default="", help="module title (default: from the folder name)")
    args = parser.parse_args()

    course = ROOT / "courses" / args.course
    if not course.is_dir():
        raise SystemExit(f"No course folder {course}. Create it with tools/new_course.py first.")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.name):
        raise SystemExit("Module name: lowercase letters, digits and dashes.")
    number = f"{int(args.number):02d}"
    others = [p for p in course.glob(f"{number}-*") if p.is_dir() and p.name != f"{number}-{args.name}"]
    if others:
        raise SystemExit(f"Module {number} already exists as {others[0].name}.")
    module = course / f"{number}-{args.name}"
    title = args.title or args.name.replace("-", " ").capitalize()
    today = dt.date.today().isoformat()

    files = {
        "MAP.md": (ASSETS / "MAP_TEMPLATE.md").read_text(encoding="utf-8").replace("<NN>", number).replace("<title>", title),
        "PRIMER.md": (ASSETS / "PRIMER_TEMPLATE.md").read_text(encoding="utf-8").replace("<NN>", number).replace("<title>", title),
        "NOTES.md": (f"# Module {number} notes — {title}\n\n"
                     "Dated history: append entries, never rewrite. Format in the session-handoff skill.\n\n"
                     f"## {today} — module started\n\n- Plan: `PRIMER.md` and `MAP.md` (written by plan-module).\n"
                     "- Learner did: nothing yet in this module.\n"),
        "TODO.md": (f"# Module {number} to-do\n\n"
                    "Parked side topics and unfinished work. One line each, with the date and where it came from.\n"),
    }
    for sub in ("figures", "lessons"):
        (module / sub).mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        path = module / name
        if path.exists():
            print(f"keep     {path.relative_to(ROOT).as_posix()}")
            continue
        with path.open("w", encoding="utf-8", newline="\n") as handle:  # LF on every OS
            handle.write(text)
        print(f"create   {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
