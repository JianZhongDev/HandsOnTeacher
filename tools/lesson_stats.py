"""Check lesson cards against the reading budget (200 words of prose per card).

    python tools/lesson_stats.py courses/<course>/03-eviction/lessons/L01-lru/LESSON.md
    python tools/lesson_stats.py courses/<course>      # every card in a course
    python tools/lesson_stats.py --all                 # every card in courses/ and examples/

Counts the words a learner must read: prose outside code blocks, <details> blocks,
images and HTML comments. Exit code 1 if any card is over budget.
Needs only the Python standard library (Python 3.9+).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BUDGET = 200
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


def cards(arg: str) -> list[Path]:
    if arg == "--all":
        return sorted([*ROOT.glob("courses/*/*/lessons/*/LESSON.md"), *ROOT.glob("examples/**/LESSON.md")])
    path = Path(arg)
    if not path.is_absolute() and not path.exists():
        path = ROOT / arg
    return sorted(path.rglob("LESSON.md")) if path.is_dir() else [path]


def main() -> int:
    paths = [p for a in sys.argv[1:] for p in cards(a)]
    if not paths:
        print(__doc__)
        return 2
    over = 0
    for path in paths:
        n = reading_words(path.read_text(encoding="utf-8"))
        flag = "OK  " if n <= BUDGET else "OVER"
        over += n > BUDGET
        try:
            shown = path.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            shown = str(path)
        print(f"{flag} {n:5d} words  {shown}")
    print(f"\nBudget {BUDGET} words of prose per card (code, <details>, images excluded).")
    return 1 if over else 0


if __name__ == "__main__":
    raise SystemExit(main())
