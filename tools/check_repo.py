"""Repository self-check for maintainers and CI. Needs only the Python standard library (3.9+).

    python tools/check_repo.py

Checks:
  1. skill mirrors (.claude/skills) match .agents/skills
  2. every skill has valid front matter (name = folder name, a real description)
  3. no personal or machine-specific absolute paths in tracked text files
  4. relative links and images in Markdown files resolve
  5. line endings: LF for .sh/.py/.md, CRLF for .cmd (Windows batch files misbehave with LF)
  6. courses/ and sources/ hold nothing that would be published (they are personal)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import sync_skills  # noqa: E402

SKIP_DIRS = {".git", "courses", "sources", ".env", ".venv", "results", "cache", "__pycache__", "node_modules"}
TEXT_SUFFIXES = {".md", ".py", ".sh", ".cmd", ".json", ".yml", ".yaml", ".toml", ".txt"}
PERSONAL = [
    (re.compile(r"/home/[a-z0-9_.-]+/", re.I), "absolute home path"),
    (re.compile(r"/Users/[A-Za-z0-9_.-]+/"), "absolute home path"),
    (re.compile(r"\b[A-Z]:\\(?:Users|Workspace|GitRepo|Projects)\\", re.I), "absolute Windows path"),
    (re.compile(r"/mnt/[a-z]/(?:Users|Workspace|GitRepo|Projects)/", re.I), "absolute WSL path"),
]
ALLOW_PERSONAL = {"tools/check_repo.py"}
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

problems: list[str] = []


def tracked_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and not (set(path.relative_to(ROOT).parts) & SKIP_DIRS):
            yield path


def check_skills() -> None:
    for mirror in sync_skills.DEFAULT_MIRRORS:
        for line in sync_skills.differences(mirror):
            problems.append(f"skill mirror {mirror.relative_to(ROOT).as_posix()}: {line} (run tools/sync_skills.py)")
    for skill in sorted((ROOT / ".agents" / "skills").iterdir()):
        md = skill / "SKILL.md"
        if not md.exists():
            problems.append(f"{skill.relative_to(ROOT).as_posix()}: missing SKILL.md")
            continue
        text = md.read_text(encoding="utf-8")
        match = re.match(r"---\n(.*?)\n---\n", text, re.S)
        front = match.group(1) if match else ""
        name = re.search(r"^name:\s*(.+)$", front, re.M)
        desc = re.search(r"^description:\s*(.+)$", front, re.M)
        if not name or name.group(1).strip() != skill.name:
            problems.append(f"{md.relative_to(ROOT).as_posix()}: front matter 'name' must equal '{skill.name}'")
        if not desc or not 20 <= len(desc.group(1).strip()) <= 1024:
            problems.append(f"{md.relative_to(ROOT).as_posix()}: front matter needs a 'description' of 20-1024 characters")


def check_text() -> None:
    for path in tracked_files():
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        raw = path.read_bytes()
        if path.suffix in {".sh", ".py", ".md"} and b"\r\n" in raw:
            problems.append(f"{rel}: CRLF line endings (use LF)")
        if path.suffix == ".cmd" and re.search(rb"(?<!\r)\n", raw):
            problems.append(f"{rel}: Windows batch file needs CRLF line endings")
        text = raw.decode("utf-8", errors="replace")
        if rel not in ALLOW_PERSONAL:
            for pattern, label in PERSONAL:
                for m in pattern.finditer(text):
                    line = text.count("\n", 0, m.start()) + 1
                    problems.append(f"{rel}:{line}: {label}: {m.group(0)}")
        if path.suffix == ".md" and not path.name.endswith("_TEMPLATE.md"):
            in_code = False
            for number, line in enumerate(text.splitlines(), 1):
                if line.lstrip().startswith("```"):
                    in_code = not in_code
                if in_code:
                    continue
                for target in LINK.findall(re.sub(r"`[^`]*`", "", line)):
                    if re.match(r"[a-z]+:", target) or target.startswith("#") or "<" in target:
                        continue
                    target = target.split("#")[0]
                    # normpath drops "..", which keeps deep Windows paths under the 260-character limit
                    if target and not Path(os.path.normpath(path.parent / target)).exists():
                        problems.append(f"{rel}:{number}: broken link: {target}")


def check_personal_folders() -> None:
    """courses/ and sources/ are ignored by Git; only their README may be committed."""
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for needed in ("courses/*", "!courses/README.md", "sources/"):
        if needed not in gitignore.splitlines():
            problems.append(f".gitignore: missing '{needed}' (courses and checkouts are personal)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.parse_args()
    check_skills()
    check_text()
    check_personal_folders()
    if problems:
        print(f"{len(problems)} problem(s):")
        for line in problems:
            print("  " + line)
        return 1
    print("check_repo: all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
