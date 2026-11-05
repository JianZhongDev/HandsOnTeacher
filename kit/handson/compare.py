"""Show several settings side by side: a readable table, a combined image, a timer.

    rows = {"no cache": {"p95 latency (ms)": 412, "errors": 0},
            "LRU":      {"p95 latency (ms)": 38,  "errors": 0}}
    print_table(rows)                                   # one small table, words for column names
    side_by_side(["a.png", "b.png"], ["no cache", "LRU"], run.out / "compare.png")
    with timed() as t: do_work()
    print(t.seconds)
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Sequence


def print_table(rows: dict[str, dict[str, object]], digits: int = 3) -> str:
    """Print rows (name -> {column: value}) as an aligned table and return the text."""
    columns: list[str] = []
    for values in rows.values():
        columns += [c for c in values if c not in columns]

    def fmt(v: object) -> str:
        if isinstance(v, float):
            return f"{v:.{digits}g}"
        return "" if v is None else str(v)

    cells = [[name] + [fmt(values.get(c)) for c in columns] for name, values in rows.items()]
    header = [""] + columns
    widths = [max(len(r[i]) for r in [header] + cells) for i in range(len(header))]
    lines = ["  ".join(h.ljust(w) if i == 0 else h.rjust(w) for i, (h, w) in enumerate(zip(header, widths)))]
    for row in cells:
        lines.append("  ".join(c.ljust(w) if i == 0 else c.rjust(w) for i, (c, w) in enumerate(zip(row, widths))))
    text = "\n".join(lines)
    print(text)
    return text


def side_by_side(images: Sequence, labels: Sequence[str], path: str | Path | None = None, gap: int = 8):
    """Place images (paths or PIL images) in one row with a label above each. Needs Pillow.

    Returns the combined PIL image and saves it to `path` if given.
    """
    from PIL import Image, ImageDraw, ImageFont  # optional dependency, imported only when used

    opened = [Image.open(i).convert("RGB") if not hasattr(i, "convert") else i.convert("RGB") for i in images]
    if len(opened) != len(labels):
        raise ValueError("one label per image")
    try:
        font = ImageFont.load_default(size=20)   # Pillow >= 10.1
    except TypeError:
        font = ImageFont.load_default()
    bar = 34
    height = max(im.height for im in opened) + bar
    width = sum(im.width for im in opened) + gap * (len(opened) - 1)
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    x = 0
    for im, label in zip(opened, labels):
        canvas.paste(im, (x, bar))
        draw.text((x + 8, 6), label, fill=(31, 41, 51), font=font)
        x += im.width + gap
    if path is not None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(path)
        print(f"saved comparison: {path}")
    return canvas


class _Timer:
    seconds: float = 0.0


@contextmanager
def timed() -> Iterator[_Timer]:
    """Measure wall-clock time of a block: `with timed() as t: ...; t.seconds`."""
    timer = _Timer()
    start = time.perf_counter()
    try:
        yield timer
    finally:
        timer.seconds = time.perf_counter() - start


def reading_guide(items: dict[str, str], title: str = "How to read this", path: str | Path | None = None) -> str:
    """Print (and optionally save) a short legend before the results: one line per metric, axis, line or colour.

    reading_guide({
        "ATE RMSE (m)": "typical distance between estimated and true position; lower is better; compared with ground truth",
        "blue line": "estimated trajectory; the dashed black line is the ground truth",
    }, path=run.out / "READING_GUIDE.txt")

    Labs call this before print_table so that no number or curve appears unexplained.
    """
    lines = [title, "-" * len(title)] + [f"  {name}: {meaning}" for name, meaning in items.items()] + [""]
    text = "\n".join(lines)
    print(text)
    if path is not None:
        Path(path).write_text(text, encoding="utf-8")
    return text
