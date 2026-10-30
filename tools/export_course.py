"""Package one course as a standalone repository that anyone can clone and learn from.

    python tools/export_course.py <course> <destination-folder>
    python tools/export_course.py <course> <destination-folder> --lessons-as-examples --include-materials

The result works like this repository with a single course in it: the same agent instructions,
skills, method, kit and tools, plus courses/<course>/ with the curriculum, survey, course helpers
and figures, reset to a fresh start (no learner profile, no progress, not set up). The codebases are
not copied: setup-environment clones them from the origins recorded in course.json.

Options:
  --lessons-as-examples   copy the built module maps and lessons (without results or caches) to
                          examples/<course>/ as a preview; learners still get every lesson built fresh
  --include-materials    copy reference documents too (only if their licenses allow redistribution);
                          by default only materials/INDEX.md is exported, with links

Needs only the Python standard library (Python 3.9+).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_repo import PERSONAL  # noqa: E402

FRAMEWORK = ["AGENTS.md", "CLAUDE.md", "GEMINI.md", "START_HERE.md", "LICENSE", "CREDITS.md", ".trae",
             ".gitattributes", ".github", ".agents", ".claude", ".grok", "method", "kit", "tools",
             "docs", "examples", "courses/README.md"]
COURSE_FILES = ["COURSE.md", "SURVEY.md", "GLOSSARY.md", "figures", "_shared"]
NEVER = shutil.ignore_patterns("__pycache__", "*.pyc", "results", "cache", ".env", ".venv", "node_modules")
BIG = 20 * 1024 * 1024  # files above this stay out (trained models, datasets): regenerate them instead


def copy(src: Path, dst: Path) -> None:
    if src.is_dir():
        shutil.copytree(src, dst, ignore=NEVER, dirs_exist_ok=True)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("course")
    parser.add_argument("destination")
    parser.add_argument("--lessons-as-examples", action="store_true")
    parser.add_argument("--include-materials", action="store_true")
    args = parser.parse_args()

    course = ROOT / "courses" / args.course
    dest = Path(args.destination).expanduser().resolve()
    if not (course / "COURSE.md").exists():
        raise SystemExit(f"No course at {course}.")
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"{dest} is not empty. Choose a new or empty folder.")
    if ROOT in dest.parents or dest == ROOT:
        raise SystemExit("Export outside this repository.")
    info = json.loads((course / "course.json").read_text(encoding="utf-8"))
    title = info.get("title", args.course)
    target = dest / "courses" / args.course
    warnings: list[str] = []

    # 1. The framework: instructions, skills, method, kit, tools.
    for name in FRAMEWORK:
        if (ROOT / name).exists():
            copy(ROOT / name, dest / name)

    # 2. The course content, reset to a fresh start.
    for name in COURSE_FILES:
        if (course / name).exists():
            copy(course / name, target / name)
    for name in ("lab.sh", "lab.cmd"):   # machine-specific settings: back to the template
        shutil.copyfile(ROOT / ".agents/skills/setup-environment/assets" / name, target / name)
    assets = ROOT / ".agents/skills/create-course/assets"
    fill = {"<title>": title, "<date>": dt.date.today().isoformat(), "<course>": args.course}

    def render(name: str) -> str:
        text = (assets / name).read_text(encoding="utf-8")
        for key, value in fill.items():
            text = text.replace(key, value)
        return text

    write(target / "LEARNER.md", render("LEARNER_TEMPLATE.md"))
    write(target / "FEEDBACK_LOG.md", f"# Feedback log — {title}\n\nOne dated line per learner correction of the teaching.\n")
    write(target / "STATE.md", render("STATE_TEMPLATE.md")
          .replace(f"course created {fill['<date>']}; curriculum in `COURSE.md`.",
                   "the course has **not started**. Curriculum in `COURSE.md`.")
          .replace("finish `create-course` (survey, environment, curriculum), then `plan-module` for Module 01.",
                   "use the `start-course` skill: set up the environment, record the learner profile, show the course map."))
    course_md = (course / "COURSE.md").read_text(encoding="utf-8")
    course_md = re.sub(r"^(\|[ \t]*\d{2}[ \t]*\|.*\|)[^|\n]*\|[ \t]*$", r"\1 not started |", course_md, flags=re.M)
    write(target / "COURSE.md", course_md)

    info.update(ready=False, checked="", timings_note="measured on the author's machine; re-measured by setup",
                machine={"os": "", "arch": "", "accelerator": "", "notes": ""})
    for s in info.get("sources", []):
        s["path"] = ""
        if s.get("kind") == "repo" and not re.match(r"(https?://|git@)", s.get("origin", "")):
            warnings.append(f"source '{s['name']}' comes from a local path ({s['origin']}): publish it and put "
                            "its URL in course.json, or learners cannot get it")
    write(target / "course.json", json.dumps(info, indent=2) + "\n")

    refs = course / "materials"
    if refs.exists():
        if args.include_materials:
            copy(refs, target / "materials")
        elif (refs / "INDEX.md").exists():
            copy(refs / "INDEX.md", target / "materials" / "INDEX.md")

    # 3. Optional preview: built lessons as examples (never as the learner's progress).
    modules = sorted(p for p in course.glob("[0-9][0-9]-*") if p.is_dir())
    if args.lessons_as_examples:
        for module in modules:
            if not any(module.glob("lessons/*/LESSON.md")):   # scaffolded but never built: nothing to show
                continue
            for name in ("MAP.md", "figures", "lessons"):
                if (module / name).exists():
                    copy(module / name, dest / "examples" / args.course / module.name / name)

    # 4. Repository files: README for people, .gitignore that tracks this course.
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    keep = f"!courses/{args.course}/\n"
    if not args.include_materials:
        keep += f"courses/{args.course}/materials/*\n!courses/{args.course}/materials/INDEX.md\n"
    write(dest / ".gitignore", gitignore.replace("!courses/README.md\n", "!courses/README.md\n" + keep))
    # The README shows what learners get: everything above the agent-facing sections, without the status legend.
    overview = re.split(r"^## (?:Course-specific rules|Module entries)", course_md, maxsplit=1, flags=re.M)[0]
    overview = re.sub(r"^Status values:.*\n", "", overview.split("\n", 1)[1], flags=re.M).strip()
    overview = overview.replace("](figures/", f"](courses/{args.course}/figures/")
    sources = "\n".join(f"- **{s['name']}** ({s.get('kind', '')}): {s.get('origin', '')}"
                        + (f" — {s['license']}" if s.get("license") else "") for s in info.get("sources", []))
    readme = (ROOT / ".agents/skills/export-course/assets/README_TEMPLATE.md").read_text(encoding="utf-8")
    write(dest / "README.md", readme.replace("<title>", title).replace("<overview>", overview)
          .replace("<sources>", sources or "- (none recorded)").replace("<course>", args.course))

    # 5. Checks: big files, personal paths.
    for path in dest.rglob("*"):
        if path.is_file() and path.stat().st_size > BIG:
            path.unlink()
            warnings.append(f"left out {path.relative_to(dest).as_posix()} (over 20 MB): regenerate it, "
                            "or host it elsewhere and download it in setup")
        elif path.is_file() and path.suffix in {".md", ".json", ".py", ".sh", ".txt"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern, label in PERSONAL:
                if path.name != "check_repo.py" and pattern.search(text):
                    warnings.append(f"{path.relative_to(dest).as_posix()}: {label} — remove before publishing")
    print(f"exported {args.course} -> {dest}")
    print(f"  modules in curriculum: {len(modules)}; lessons as examples: {'yes' if args.lessons_as_examples else 'no'}")
    for w in warnings:
        print("  WARNING " + w)
    print("Next: review README.md and LICENSE (add your name for the course content), run "
          "python tools/check_repo.py there, then test a fresh start with start-course.")
    return 1 if warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
