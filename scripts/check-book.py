"""Check all generated HTML links, assets and local fragment identifiers."""

from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / "tmp" / "book"
PREFIX = "/learn-knowledge-graph/"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])


def main():
    pages = {p: Page(p) for p in ROOT.rglob("*.html")}
    if not pages or not (ROOT / "index.html").is_file():
        raise RuntimeError("Book has not been built")
    issues = []
    links = 0
    for path, page in pages.items():
        for target in page.links:
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            links += 1
            local = unquote(url.path)
            if local.startswith(PREFIX):
                destination = ROOT / local[len(PREFIX):]
            elif local.startswith("/"):
                issues.append(f"{path.name}: outside site prefix: {target}")
                continue
            else:
                destination = path.parent / local if local else path
            destination = destination.resolve()
            if not destination.is_relative_to(ROOT):
                issues.append(f"{path.name}: outside site: {target}")
                continue
            if destination.is_dir():
                destination /= "index.html"
            if not destination.is_file():
                issues.append(f"{path.relative_to(ROOT)}: missing {target}")
            elif url.fragment and destination in pages:
                if unquote(url.fragment) not in pages[destination].ids:
                    issues.append(f"{path.relative_to(ROOT)}: missing fragment {target}")
    # Generated sources, old drafts, review assets and PDFs are not website assets.
    forbidden = [p for p in ROOT.rglob("*") if p.is_file() and
                 (p.suffix in {".md", ".pdf", ".py", ".zip", ".exe"} or
                  any(part in {".git", "drafts", "reviews", "output"} for part in p.relative_to(ROOT).parts))]
    issues.extend(f"Unexpected published file: {p.relative_to(ROOT)}" for p in forbidden)
    sections = json.loads((ROOT / "reader-search-index.json").read_text(encoding="utf-8"))
    if not sections:
        issues.append("Empty reader search index")
    for section in sections:
        url = urlsplit(section["url"])
        destination = ROOT / url.path
        if destination not in pages or (url.fragment and unquote(url.fragment) not in pages[destination].ids):
            issues.append(f"Invalid search result: {section['url']}")
    if issues:
        raise RuntimeError("\n".join(issues))
    print(f"Checked {len(pages)} HTML pages, {links} local links/assets and {len(sections)} search sections; no issues")


if __name__ == "__main__":
    main()
