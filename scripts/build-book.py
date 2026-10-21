"""Stage only the reader-facing Markdown, then build the mdBook website.

Run from any directory with Python 3.11+ and the pinned tools on PATH.
The canonical Markdown is never rewritten; links outside the book point to GitHub.
"""

import os
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "tmp" / "book-src"
ASSETS = ROOT / "tmp" / "mermaid-assets"
REPOSITORY = "https://github.com/d-tsu/learn-knowledge-graph"
LINK = re.compile(r"(!?\[[^\]\n]*\]\()([^\s)]+)(\))")


class SearchSections(HTMLParser):
    """Index the rendered main content and its actual heading IDs."""

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.inside = False
        self.heading = False
        self.chapter = ""
        self.title = []
        self.body = []
        self.anchor = ""
        self.sections = []

    def flush(self):
        if not self.body and not self.title:
            return
        title = "".join(self.title).strip()
        if not self.chapter:
            self.chapter = title
        self.sections.append({
            "title": title if title == self.chapter else f"{self.chapter} / {title}",
            "url": self.url + ("#" + self.anchor if self.anchor else ""),
            "body": re.sub(r"\s+", " ", " ".join(self.body)).strip(),
        })

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.inside = True
        if self.inside and tag in {"h1", "h2", "h3"}:
            self.flush()
            self.title, self.body = [], []
            self.anchor = dict(attrs).get("id", "")
            self.heading = True

    def handle_endtag(self, tag):
        if tag in {"h1", "h2", "h3"}:
            self.heading = False
        if tag == "main":
            self.flush()
            self.inside = False

    def handle_data(self, data):
        if self.inside:
            (self.title if self.heading else self.body).append(data)


def staged_name(name):
    path = Path(name)
    return path.with_name("index.md") if path.name == "README.md" else path


def book_files():
    summary = (ROOT / "site" / "SUMMARY.md").read_text(encoding="utf-8")
    files = [match[1] for match in LINK.findall(summary)]
    if len(files) != len(set(files)):
        raise ValueError("Duplicate chapter in site/SUMMARY.md")
    for name in files:
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file() or path.suffix != ".md":
            raise ValueError(f"Invalid book source: {name}")
    expected = set((ROOT / "docs" / "chapters").glob("*.md"))
    expected.update((ROOT / "docs" / "appendices").glob("*.md"))
    missing = expected - {(ROOT / name).resolve() for name in files}
    if missing:
        raise ValueError(f"Chapters missing from SUMMARY: {sorted(map(str, missing))}")
    return summary, files


def reader_markdown(name, files):
    source = ROOT / name
    text = source.read_text(encoding="utf-8")

    def link(match):
        before, target, after = match.groups()
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path:
            return match[0]
        path = (source.parent / unquote(url.path)).resolve()
        if not path.is_relative_to(ROOT) or not path.exists():
            raise ValueError(f"Missing or out-of-repository link: {name}: {target}")
        relative = path.relative_to(ROOT).as_posix()
        if relative in files:
            target = Path(os.path.relpath(staged_name(relative), staged_name(name).parent)).as_posix()
            if url.fragment:
                target += "#" + url.fragment
            return before + target + after
        kind = "tree" if path.is_dir() else "blob"
        target = f"{REPOSITORY}/{kind}/main/{quote(relative, safe='/')}"
        if url.fragment:
            target += "#" + url.fragment
        return before + target + after

    # Keep links appearing inside code examples unchanged.
    chunks = re.split(r"(^```[^\n]*\n.*?^```[^\n]*$)", text, flags=re.M | re.S)
    return "".join(LINK.sub(link, chunk) if i % 2 == 0 else chunk for i, chunk in enumerate(chunks))


def main():
    tools = ROOT / "tmp" / "mdbook-tools"
    os.environ["PATH"] = str(tools) + os.pathsep + os.environ["PATH"]
    for command, version in [("mdbook", "v0.5.4"), ("mdbook-mermaid", "0.17.1")]:
        actual = subprocess.check_output([command, "--version"], text=True).strip()
        if actual.split()[-1] != version:
            raise RuntimeError(f"Expected {command} {version}; got {actual}")

    summary, files = book_files()
    # These fixed, resolved paths must remain inside the disposable workspace tmp/.
    if STAGING.resolve() != ROOT / "tmp" / "book-src":
        raise ValueError("Unexpected staging path")
    if STAGING.exists():
        shutil.rmtree(STAGING)
    output = ROOT / "tmp" / "book"
    if output.resolve() != ROOT / "tmp" / "book":
        raise ValueError("Unexpected output path")
    if output.exists():
        shutil.rmtree(output)
    STAGING.mkdir(parents=True)
    summary = LINK.sub(lambda m: m[1] + staged_name(m[2]).as_posix() + m[3], summary)
    (STAGING / "SUMMARY.md").write_text(summary, encoding="utf-8")
    for name in files:
        destination = STAGING / staged_name(name)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(reader_markdown(name, files), encoding="utf-8")

    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "book.toml").write_text('[book]\ntitle = "Mermaid assets"\n', encoding="utf-8")
    subprocess.run(["mdbook-mermaid", "install", str(ASSETS)], check=True, cwd=ROOT)
    subprocess.run(["mdbook", "build"], check=True, cwd=ROOT)
    sections = []
    for name in files:
        url = staged_name(name).with_suffix(".html").as_posix()
        parser = SearchSections(url)
        parser.feed((output / url).read_text(encoding="utf-8"))
        sections.extend(parser.sections)
    (output / "reader-search-index.json").write_text(
        json.dumps(sections, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Built {len(files)} reader pages in tmp/book")


if __name__ == "__main__":
    main()
