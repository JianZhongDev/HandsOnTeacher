"""Check lesson cards and module primers against the reading budget, and that each says what it teaches.

Budgets: 700 words of prose per lesson card (LESSON.md), 900 per module primer (PRIMER.md),
1500 for Module 01's primer (the guided tour). Budgets are generous on purpose: they stop padding,
not explanation. The checks below make sure explanation is actually there.
Structure: a card needs a "How it works" section, a "Data" section, a reading guide, a "Predict" section
and at least one image; a primer needs a "How it works" section and at least two images (map + concept
diagram); the guided tour needs at least one "Stop" per box.
Intro: each card and primer opens, before its first code block, with a line starting with
the target emoji (U+1F3AF) that says in plain words what it teaches ("**Today: demosaicing.** ...").

    python tools/lesson_stats.py courses/<course>/03-eviction/lessons/L01-lru/LESSON.md
    python tools/lesson_stats.py courses/<course>/03-eviction/PRIMER.md
    python tools/lesson_stats.py courses/<course>      # every card and primer in a course
    python tools/lesson_stats.py --all                 # every card and primer in courses/ and examples/

Counts the words a learner must read: prose outside code blocks, <details> blocks,
images and HTML comments. Exit code 1 if any card is over budget or has no intro line.
Needs only the Python standard library (Python 3.9+).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BUDGETS = {"LESSON.md": 700, "PRIMER.md": 900}   # anything else: the lesson card budget
TOUR_BUDGET = 1500   # Module 01 (folder name starts with "01") primer: the guided tour
INTRO = "\N{DIRECT HIT}"   # 🎯 starts the line that says what the lesson or module teaches
ROOT = Path(__file__).resolve().parents[1]
# Chinese, Japanese and Korean scripts (code-point ranges): text without spaces between words.
CJK_RANGES = [(0x3040, 0x30FF), (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xAC00, 0xD7AF), (0xF900, 0xFAFF)]
CJK = re.compile("[" + "".join(f"{chr(a)}-{chr(b)}" for a, b in CJK_RANGES) + "]")


def reading_words(text: str) -> int:
    text = re.sub(r"<details>.*?</details>", " ", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"[#>*|`_\-]+", " ", text)
    cjk = len(CJK.findall(text))  # about 2 characters per word
    text = CJK.sub(" ", text)
    return len(re.findall(r"[^\W_][\w'’.,%°/+=-]*", text)) + (cjk + 1) // 2


def has_intro(text: str) -> bool:
    """True if a line starting with 🎯 comes before the first code block."""
    head = re.sub(r"<!--.*?-->", " ", text.split("```")[0], flags=re.S)
    return any(line.lstrip("> ").startswith(INTRO) for line in head.splitlines())


def images(text: str) -> int:
    return len(re.findall(r"!\[[^\]]*\]\([^)]*\)", re.sub(r"<!--.*?-->", " ", text, flags=re.S)))


def missing_parts(path: Path, text: str) -> list[str]:
    """Structural requirements: the explanation, data, reading guide and pictures must exist."""
    plain = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    heads = [h.lower() for h in re.findall(r"^#{2,4}\s+(.+)$", plain, flags=re.M)]

    def has(*words: str) -> bool:
        return any(any(w in h for w in words) for h in heads)

    missing = []
    if path.name == "LESSON.md":
        if not has("how it works", "mechanism", "the idea"):
            missing.append('a "How it works" section (the mechanism, with a diagram)')
        if not has("data", "setup"):
            missing.append('a "Data and setup" section (which real data and code)')
        if not has("reading guide", "how to read", "read the"):
            missing.append('a "Reading guide" section (what every number and curve means)')
        if not has("predict"):
            missing.append('a "Predict" section')
        if images(text) < 2:
            missing.append("a map image and a concept diagram (at least 2 images)")
    elif path.name == "PRIMER.md":
        tour = path.resolve().parent.name.startswith("01")
        if not has("how it works", "mechanism", "stop", "tour"):
            missing.append('a "How it works" section (the key algorithm, walked through)')
        if tour and sum(1 for h in heads if h.startswith("stop")) < 3:
            missing.append('guided tour: at least 3 "Stop N" sections, one per box of the course map')
        if images(text) < 2:
            missing.append("the course map plus a concept diagram (at least 2 images)")
    return missing


def cards(arg: str) -> list[Path]:
    if arg == "--all":
        return sorted([*ROOT.glob("courses/*/*/lessons/*/LESSON.md"), *ROOT.glob("courses/*/*/PRIMER.md"),
                       *ROOT.glob("examples/**/LESSON.md"), *ROOT.glob("examples/**/PRIMER.md")])
    path = Path(arg)
    if not path.is_absolute() and not path.exists():
        path = ROOT / arg
    return sorted([*path.rglob("LESSON.md"), *path.rglob("PRIMER.md")]) if path.is_dir() else [path]


def main() -> int:
    paths = [p for a in sys.argv[1:] for p in cards(a)]
    if not paths:
        print(__doc__)
        return 2
    failed = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        n = reading_words(text)
        budget = BUDGETS.get(path.name, BUDGETS["LESSON.md"])
        if path.name == "PRIMER.md" and path.resolve().parent.name.startswith("01"):
            budget = TOUR_BUDGET
        intro = has_intro(text)
        parts = missing_parts(path, text)
        flag = "OVER" if n > budget else "OK  " if intro and not parts else "MISS"
        failed += n > budget or not intro or bool(parts)
        try:
            shown = path.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            shown = str(path)
        note = "" if intro else "  (no intro line saying what it teaches)"
        print(f"{flag} {n:5d}/{budget} words  {shown}{note}")
        for part in parts:
            print(f"       missing: {part}")
    print("\nBudgets: words of prose per lesson card and module primer (code, <details>, images excluded)."
          "\nEach must open, before any code, with an intro line starting with the target emoji (U+1F3AF).")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
