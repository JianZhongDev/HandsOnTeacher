"""Turn reference documents and web pages into plain Markdown text an agent can search and cite.

    python tools/extract_text.py <course> <file-or-URL> [<file-or-URL> ...] [--name NAME]

Examples:
    python tools/extract_text.py caching-course ~/papers/caching.pdf
    python tools/extract_text.py caching-course https://docs.example.org/guide/eviction --name eviction-guide
    uv run --with pypdf --with certifi python tools/extract_text.py caching-course paper.pdf https://...   # extras

Supported: PDF (needs the pypdf package, or the pdftotext program), DOCX, PPTX, HTML, Markdown, plain
text, reStructuredText, Jupyter notebooks (.ipynb), and http(s) URLs to any of these.

Local files and downloads are copied into courses/<course>/materials/; the text goes to
courses/<course>/materials/text/<name>.md, with page or slide markers so lessons can cite
"p. 12" or "slide 4". Add each source to materials/INDEX.md afterwards. Other formats: convert with
pandoc or the agent's own document reader. Standard library only, apart from optional pypdf.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import shutil
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "source"


# ---------- readers: each returns Markdown text ----------

class _HTMLToMarkdown(HTMLParser):
    SKIP = {"script", "style", "nav", "footer", "header", "noscript", "svg", "form"}
    BLOCK = {"p", "div", "section", "article", "br", "tr", "table", "blockquote"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0
        self.pre = False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif re.fullmatch(r"h[1-6]", tag):
            self.out.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "li":
            self.out.append("\n- ")
        elif tag == "pre":
            self.pre = True
            self.out.append("\n\n```\n")
        elif tag in {"td", "th"}:
            self.out.append(" | ")
        elif tag in self.BLOCK:
            self.out.append("\n\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
        elif tag == "pre":
            self.pre = False
            self.out.append("\n```\n\n")
        elif re.fullmatch(r"h[1-6]", tag) or tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self.skip:
            return
        self.out.append(data if self.pre else re.sub(r"\s+", " ", data))

    def text(self) -> str:
        return re.sub(r"\n{3,}", "\n\n", "".join(self.out)).strip() + "\n"


def read_html(data: bytes) -> str:
    parser = _HTMLToMarkdown()
    parser.feed(data.decode("utf-8", errors="replace"))
    return parser.text()


def read_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        root = ElementTree.fromstring(z.read("word/document.xml"))
    lines = []
    for block in root.iter():
        if block.tag == f"{W}p":
            style = block.find(f"{W}pPr/{W}pStyle")
            text = "".join(t.text or "" for t in block.iter(f"{W}t")).strip()
            if not text:
                continue
            level = re.search(r"(\d)$", style.get(f"{W}val", "")) if style is not None else None
            is_heading = style is not None and "heading" in style.get(f"{W}val", "").lower()
            lines.append(("#" * int(level.group(1)) + " " if is_heading and level else "") + text)
    return "\n\n".join(lines) + "\n"


def read_pptx(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        slides = sorted((n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
                        key=lambda n: int(re.search(r"(\d+)", n.rsplit("/", 1)[1]).group(1)))
        parts = []
        for i, name in enumerate(slides, 1):
            root = ElementTree.fromstring(z.read(name))
            paras = ["".join(t.text or "" for t in p.iter(f"{A}t")).strip() for p in root.iter(f"{A}p")]
            parts.append(f"## Slide {i}\n\n" + "\n".join(p for p in paras if p))
    return "\n\n".join(parts) + "\n"


def read_ipynb(path: Path) -> str:
    nb = json.loads(path.read_text(encoding="utf-8"))
    parts = []
    for cell in nb.get("cells", []):
        source = "".join(cell.get("source", []))
        parts.append(source if cell.get("cell_type") == "markdown" else f"```\n{source}\n```")
    return "\n\n".join(parts) + "\n"


def read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader  # optional dependency
    except ImportError:
        if shutil.which("pdftotext"):
            out = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, check=True)
            pages = out.stdout.decode("utf-8", errors="replace").split("\f")
            return "\n\n".join(f"## Page {i}\n\n{p.strip()}" for i, p in enumerate(pages, 1) if p.strip()) + "\n"
        raise SystemExit("PDF needs pypdf: run  uv run --with pypdf python tools/extract_text.py ...  "
                         "(or install pdftotext).")
    reader = PdfReader(str(path))
    return "\n\n".join(f"## Page {i}\n\n{(page.extract_text() or '').strip()}"
                       for i, page in enumerate(reader.pages, 1)) + "\n"


READERS = {".pdf": read_pdf, ".docx": read_docx, ".pptx": read_pptx, ".ipynb": read_ipynb,
           ".html": lambda p: read_html(p.read_bytes()), ".htm": lambda p: read_html(p.read_bytes())}
PLAIN = {".md", ".markdown", ".txt", ".rst", ".csv", ".json", ".yaml", ".yml", ".toml"}


# ---------- main ----------

def _download(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "HandsOnTeacher/1.0 (study notes)"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read(), response.headers.get_content_type()
    except urllib.error.URLError as error:
        if not isinstance(error.reason, ssl.SSLCertVerificationError):
            raise SystemExit(f"Could not download {url}: {error.reason}")
    # Some Python builds (for example uv's on Windows) do not see the system's certificates.
    try:
        import certifi  # optional
    except ImportError:
        raise SystemExit(f"Could not verify the HTTPS certificate of {url} with this Python. Re-run with "
                         "`uv run --with certifi python tools/extract_text.py ...`, or save the page with a "
                         "browser or the agent's own web tool and pass the file instead.")
    context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(request, timeout=60, context=context) as response:
        return response.read(), response.headers.get_content_type()


def fetch(url: str, refs: Path, name: str) -> Path:
    data, kind = _download(url)
    suffix = {"application/pdf": ".pdf", "text/html": ".html", "text/markdown": ".md",
              "text/plain": ".txt"}.get(kind, Path(url.split("?")[0]).suffix or ".html")
    path = refs / f"{name}{suffix}"
    path.write_bytes(data)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("course")
    parser.add_argument("sources", nargs="+", help="local files or http(s) URLs")
    parser.add_argument("--name", help="output name (only with a single source)")
    args = parser.parse_args()
    course = ROOT / "courses" / args.course
    if not course.is_dir():
        raise SystemExit(f"No course folder {course}.")
    if args.name and len(args.sources) > 1:
        raise SystemExit("--name works with a single source only.")
    refs = course / "materials"
    (refs / "text").mkdir(parents=True, exist_ok=True)

    for source in args.sources:
        is_url = bool(re.match(r"https?://", source))
        name = slug(args.name or (re.sub(r"^https?://(www\.)?", "", source) if is_url else Path(source).stem))
        if is_url:
            path = fetch(source, refs, name)
        else:
            path = Path(source).expanduser().resolve()
            if not path.is_file():
                raise SystemExit(f"No such file: {source}")
            if refs.resolve() not in path.parents:
                shutil.copy2(path, refs / path.name)
        suffix = path.suffix.lower()
        if suffix in READERS:
            text = READERS[suffix](path)
        elif suffix in PLAIN:
            text = path.read_text(encoding="utf-8", errors="replace")
        else:
            print(f"skip  {source}: unsupported format {suffix}; convert it with pandoc or read it directly",
                  file=sys.stderr)
            continue
        header = (f"<!-- source: {html.escape(source)} | extracted: {dt.date.today().isoformat()} "
                  f"| private study copy: quote briefly with a citation, never republish -->\n\n")
        out = refs / "text" / f"{name}.md"
        out.write_text(header + text, encoding="utf-8")
        words = len(text.split())
        print(f"text  {out.relative_to(ROOT).as_posix()}  ({words} words)  <- {source}")
    print("Next: add each source to materials/INDEX.md (kind, role, license, what it covers).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
