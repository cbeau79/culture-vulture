#!/usr/bin/env python3
"""Build the Culture Vulture static site from emails/*.md.

    python3 site/build.py            # writes site/dist/
    python3 site/build.py --serve    # builds, then serves on http://localhost:8000

Each digest becomes one page; the index lists them newest first, grouped by month.
Requires: markdown, pyyaml  (pip install markdown pyyaml)
"""

import argparse
import html
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
EMAILS = ROOT / "emails"
SITE = ROOT / "site"
DIST = SITE / "dist"
SITE_TITLE = "Culture Vulture"

FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


@dataclass
class Edition:
    slug: str
    date: date
    title: str
    standfirst: str
    body_html: str
    playlist_url: str | None
    items: int | None

    @property
    def url(self) -> str:
        return f"{self.slug}/"

    @property
    def pretty_date(self) -> str:
        return f"{self.date.day} {self.date:%B %Y}"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER.match(text)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, text[m.end():]


def inline_md(text: str) -> str:
    """Render a single line of markdown without the wrapping <p>."""
    out = markdown.markdown(text).strip()
    if out.startswith("<p>") and out.endswith("</p>"):
        out = out[3:-4]
    return out


def load_edition(path: Path) -> Edition | None:
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))

    # Date: frontmatter first, filename as fallback.
    d = meta.get("date")
    if not isinstance(d, date):
        m = re.match(r"(\d{4}-\d{2}-\d{2})", path.stem)
        if not m:
            return None
        d = date.fromisoformat(m.group(1))

    # Title = first H1; standfirst = first paragraph after it.
    lines = body.strip().splitlines()
    title = f"Culture Digest, {d.day} {d:%B %Y}"
    standfirst = ""
    rest_start = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            rest_start = i + 1
            break
    for j in range(rest_start, len(lines)):
        s = lines[j].strip()
        if not s:
            continue
        if s.startswith("#"):
            break
        standfirst = s
        rest_start = j + 1
        break

    rest = "\n".join(lines[rest_start:])
    # Drop the trailing "Generated ... edit sources in ..." footer if present.
    rest = re.sub(r"\n---\s*\nGenerated [^\n]*\s*\Z", "\n", rest)

    body_html = markdown.markdown(rest, extensions=["extra", "nl2br", "sane_lists"])
    # The digest writes "**Title** — description". The title is set on its own
    # line, so the joining dash would dangle at the start of the description.
    body_html = re.sub(r"</strong>\s*[—–-]\s*", "</strong> ", body_html)

    standfirst = inline_md(standfirst)

    playlist = meta.get("playlist_url") or meta.get("playlist")
    if not (isinstance(playlist, str) and playlist.startswith("http")):
        playlist = None

    items = meta.get("items") or meta.get("item_count")
    items = int(items) if isinstance(items, int) else None

    return Edition(
        slug=path.stem,
        date=d,
        title=title,
        standfirst=standfirst,
        body_html=body_html,
        playlist_url=playlist,
        items=items,
    )


def page(title: str, body: str, depth: int) -> str:
    base = "../" * depth
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,500;0,7..72,700;1,7..72,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}style.css">
</head>
<body>
<header class="masthead">
  <a class="masthead-title" href="{base}">{SITE_TITLE}</a>
  <span class="masthead-sub">A weekly read, watch and listen digest</span>
</header>
<main>
{body}
</main>
<footer class="colophon">
  <p>Generated every Friday from the sources and taste profiles in the vault. Links go to the original writing.</p>
</footer>
</body>
</html>
"""


def render_index(editions: list[Edition]) -> str:
    out = ["<h1 class=\"index-heading\">All editions</h1>"]
    current_month = None
    for e in editions:
        month = f"{e.date:%B %Y}"
        if month != current_month:
            if current_month is not None:
                out.append("</ol>")
            out.append(f"<h2 class=\"month\">{month}</h2>\n<ol class=\"editions\" reversed>")
            current_month = month
        meta = f"{e.items} picks" if e.items else ""
        out.append(
            f"<li class=\"edition\">"
            f"<a class=\"edition-link\" href=\"{e.url}\">"
            f"<span class=\"edition-date\">{e.pretty_date}</span>"
            f"<span class=\"edition-standfirst\">{e.standfirst}</span>"
            f"</a>"
            + (f"<span class=\"edition-meta\">{meta}</span>" if meta else "")
            + "</li>"
        )
    if current_month is not None:
        out.append("</ol>")
    return page(SITE_TITLE, "\n".join(out), depth=0)


def render_edition(e: Edition, prev_e: Edition | None, next_e: Edition | None) -> str:
    playlist = (
        f"<p class=\"playlist\"><a href=\"{html.escape(e.playlist_url)}\">Listen to this week's playlist on Spotify</a></p>"
        if e.playlist_url
        else ""
    )
    nav_parts = []
    if next_e:  # newer
        nav_parts.append(f"<a href=\"../{next_e.url}\">Newer: {next_e.pretty_date}</a>")
    if prev_e:  # older
        nav_parts.append(f"<a href=\"../{prev_e.url}\">Older: {prev_e.pretty_date}</a>")
    nav = f"<nav class=\"edition-nav\">{''.join(nav_parts)}</nav>" if nav_parts else ""

    body = f"""<article class="digest">
  <p class="digest-date"><time datetime="{e.date.isoformat()}">{e.pretty_date}</time></p>
  <p class="standfirst">{e.standfirst}</p>
  {playlist}
  <div class="digest-body">
{e.body_html}
  </div>
</article>
{nav}
"""
    return page(f"{e.pretty_date}: {SITE_TITLE}", body, depth=1)


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
        import http.server
        import functools
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
        print("Serving on http://localhost:8000 (Ctrl-C to stop)")
        http.server.ThreadingHTTPServer(("", 8000), handler).serve_forever()


if __name__ == "__main__":
    sys.exit(main())
