#!/usr/bin/env python3
"""Build the Culture Vulture static site from emails/*.md.

    python3 site/build.py            # writes site/dist/
    python3 site/build.py --serve    # builds, then serves on http://localhost:8000

Each digest becomes one page; the index lists them newest first.
Requires: markdown, pyyaml  (pip install markdown pyyaml)
"""

import argparse
import html
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
EMAILS = ROOT / "emails"
SITE = ROOT / "site"
DIST = SITE / "dist"
SITE_TITLE = "Culture Vulture"
SITE_SUB = "A weekly read, watch and listen digest"

FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
EMOJI = re.compile(r"[\U0001F000-\U0001FAFF☀-➿️]\s*")
ITEM_TITLE = re.compile(r"^\s*[-*]\s+\*\*(.+?)\*\*", re.M)

# Section slug -> (short label, colour token). Matched on the heading text.
SECTIONS = {
    "music": "Music",
    "art": "Art",
    "books": "Books",
    "film": "Film & TV",
}


def section_slug(heading: str) -> str:
    h = heading.lower()
    for key in SECTIONS:
        if key in h:
            return key
    return re.sub(r"[^a-z0-9]+", "-", h).strip("-") or "section"


@dataclass
class Section:
    slug: str
    heading: str
    html: str
    titles: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return SECTIONS.get(self.slug, self.heading)

    @property
    def count(self) -> int:
        return len(self.titles)


@dataclass
class Edition:
    slug: str
    date: date
    standfirst: str
    sections: list[Section]
    playlist_url: str | None

    @property
    def url(self) -> str:
        return f"{self.slug}/"

    @property
    def pretty_date(self) -> str:
        return f"{self.date.day} {self.date:%B %Y}"

    @property
    def short_date(self) -> str:
        return f"{self.date.day} {self.date:%b}"

    @property
    def count(self) -> int:
        return sum(s.count for s in self.sections)


def inline_md(text: str) -> str:
    out = markdown.markdown(text).strip()
    if out.startswith("<p>") and out.endswith("</p>"):
        out = out[3:-4]
    return out


def plain(text: str) -> str:
    """Markdown inline -> plain text (for pick names on the index)."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return re.sub(r"[*_`]", "", text).strip()


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER.match(text)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, text[m.end():]


def render_section_body(src: str) -> str:
    out = markdown.markdown(src, extensions=["extra", "nl2br", "sane_lists"])
    # "**Title** — description": the title is set on its own line, so drop the dash.
    out = re.sub(r"</strong>\s*[—–-]\s*", "</strong> ", out)
    # Label the link lines so they can be styled.
    out = re.sub(r"(?<![\w>])Listen:\s*", '<span class="k">Listen</span> ', out)
    out = re.sub(r"(?<![\w>])Read/Watch:\s*", '<span class="k">Read</span> ', out)
    return out


def load_edition(path: Path) -> Edition | None:
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))

    d = meta.get("date")
    if not isinstance(d, date):
        m = re.match(r"(\d{4}-\d{2}-\d{2})", path.stem)
        if not m:
            return None
        d = date.fromisoformat(m.group(1))

    lines = body.strip().splitlines()
    i = 0
    # Skip the H1.
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    i += 1
    # Standfirst = first non-empty paragraph before the first H2.
    standfirst = ""
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("#"):
            break
        i += 1
        if s:
            standfirst = s
            break

    # Sections split on H2.
    sections: list[Section] = []
    cur_head, cur_lines = None, []
    for line in lines[i:]:
        if line.startswith("## "):
            if cur_head is not None:
                sections.append(make_section(cur_head, cur_lines))
            cur_head, cur_lines = line[3:].strip(), []
        elif cur_head is not None:
            cur_lines.append(line)
    if cur_head is not None:
        sections.append(make_section(cur_head, cur_lines))

    playlist = meta.get("playlist_url") or meta.get("playlist")
    if not (isinstance(playlist, str) and playlist.startswith("http")):
        playlist = None

    return Edition(path.stem, d, inline_md(standfirst), sections, playlist)


def make_section(heading: str, lines: list[str]) -> Section:
    src = "\n".join(lines)
    src = re.sub(r"\n---\s*\nGenerated [^\n]*\s*\Z", "\n", src)
    heading_clean = EMOJI.sub("", heading).strip()
    titles = [plain(t) for t in ITEM_TITLE.findall(src)]
    return Section(section_slug(heading_clean), heading_clean, render_section_body(src), titles)


# ---------------------------------------------------------------- templates

def page(title: str, body: str, depth: int, body_class: str = "") -> str:
    base = "../" * depth
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}style.css">
</head>
<body class="{body_class}">
<header class="masthead">
  <a class="masthead-title" href="{base}">{SITE_TITLE}</a>
  <p class="masthead-sub">{SITE_SUB}</p>
</header>
<main>
{body}
</main>
<footer class="colophon">
  <p>Generated every Friday from the sources and taste profiles in the vault. Every link goes to the original writing.</p>
</footer>
</body>
</html>
"""


def section_strip(e: Edition, link_prefix: str = "") -> str:
    parts = []
    for s in e.sections:
        parts.append(
            f'<a class="strip-item" data-section="{s.slug}" href="{link_prefix}#{s.slug}">'
            f'<span class="dot"></span>{html.escape(s.label)}<span class="n">{s.count}</span></a>'
        )
    return f'<nav class="strip" aria-label="Sections">{"".join(parts)}</nav>'


def picks_block(e: Edition, cls: str) -> str:
    groups = []
    for sec in e.sections:
        if not sec.titles:
            continue
        groups.append(
            f'<p class="{cls}-group" data-section="{sec.slug}"><span class="dot"></span>'
            + html.escape("; ".join(sec.titles))
            + "</p>"
        )
    return f'<div class="{cls}">{"".join(groups)}</div>'


def render_index(editions: list[Edition]) -> str:
    latest, rest = editions[0], editions[1:]

    lead = f"""<section class="lead">
  <div class="lead-main">
    <p class="lead-date"><a href="{latest.url}">Latest edition, {latest.pretty_date}</a></p>
    <h1 class="lead-standfirst"><a href="{latest.url}">{latest.standfirst}</a></h1>
    {section_strip(latest, latest.url)}
  </div>
  <div class="lead-side">
    <p class="lead-side-heading">This week's picks</p>
    {picks_block(latest, "picks")}
    <p class="lead-side-link"><a href="{latest.url}">Read the edition</a></p>
  </div>
</section>"""

    rows = []
    for e in rest:
        rows.append(f"""<li class="row">
  <div class="row-when"><a href="{e.url}"><time datetime="{e.date.isoformat()}">{e.pretty_date}</time></a></div>
  <a class="row-standfirst" href="{e.url}">{e.standfirst}</a>
  {picks_block(e, "picks")}
</li>""")

    archive = f"""<section class="archive">
  <h2 class="archive-heading">Earlier editions</h2>
  <ol class="rows">
{chr(10).join(rows)}
  </ol>
</section>""" if rows else ""

    return page(SITE_TITLE, lead + "\n" + archive, depth=0, body_class="home")


def render_edition(e: Edition, older: Edition | None, newer: Edition | None) -> str:
    playlist = (
        f'<p class="playlist"><a href="{html.escape(e.playlist_url)}">Listen to the week\'s playlist</a></p>'
        if e.playlist_url else ""
    )
    sections = "\n".join(
        f'<section class="sec" id="{s.slug}" data-section="{s.slug}">'
        f'<h2 class="sec-heading">{html.escape(s.heading)}</h2>{s.html}</section>'
        for s in e.sections
    )
    nav = []
    if newer:
        nav.append(f'<a href="../{newer.url}"><span class="k">Newer</span>{newer.pretty_date}</a>')
    if older:
        nav.append(f'<a href="../{older.url}"><span class="k">Older</span>{older.pretty_date}</a>')

    body = f"""<article class="edition">
  <aside class="rail">
    <p class="rail-date"><time datetime="{e.date.isoformat()}">{e.pretty_date}</time></p>
    <p class="rail-count">{e.count} picks</p>
    {section_strip(e)}
    {playlist}
  </aside>
  <div class="content">
    <h1 class="standfirst">{e.standfirst}</h1>
{sections}
    <nav class="edition-nav" aria-label="Other editions">{"".join(nav)}</nav>
  </div>
</article>"""
    return page(f"{e.pretty_date}: {SITE_TITLE}", body, depth=1, body_class="single")


# ---------------------------------------------------------------- build

def build() -> int:
    editions = [ed for ed in (load_edition(p) for p in sorted(EMAILS.glob("*.md"))) if ed]
    editions.sort(key=lambda e: (e.date, e.slug), reverse=True)

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copy(SITE / "style.css", DIST / "style.css")
    (DIST / ".nojekyll").write_text("")

    (DIST / "index.html").write_text(render_index(editions), encoding="utf-8")
    for i, e in enumerate(editions):
        newer = editions[i - 1] if i > 0 else None
        older = editions[i + 1] if i + 1 < len(editions) else None
        d = DIST / e.slug
        d.mkdir()
        (d / "index.html").write_text(render_edition(e, older, newer), encoding="utf-8")

    print(f"Built {len(editions)} editions into {DIST.relative_to(ROOT)}/")
    return len(editions)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--serve", action="store_true", help="serve site/dist on port 8000 after building")
    args = ap.parse_args()
    build()
    if args.serve:
        import functools
        import http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
        print("Serving on http://localhost:8000 (Ctrl-C to stop)")
        http.server.ThreadingHTTPServer(("", 8000), handler).serve_forever()


if __name__ == "__main__":
    sys.exit(main())
