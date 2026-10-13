"""Find a preview image for each pick, with a committed cache.

Music picks: album art via Spotify's oEmbed endpoint (no auth needed).
Everything else: the article's own og:image / twitter:image.

Results live in site/images.json so the normal build makes no network calls
for anything it has seen before. A failed lookup is cached as null and retried
only when you pass --refresh-images to build.py.
"""

import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

CACHE_PATH = Path(__file__).resolve().parent / "images.json"
UA = "Mozilla/5.0 (compatible; CultureVultureBot/1.0; +https://github.com/cbeau79/culture-vulture)"
TIMEOUT = 12

META = re.compile(
    r'<meta\s+(?:[^>]*?\s)?(?:property|name)=["\'](og:image|og:image:secure_url|twitter:image|twitter:image:src)["\'][^>]*?content=["\']([^"\']+)["\']',
    re.I,
)
META_REV = re.compile(
    r'<meta\s+(?:[^>]*?\s)?content=["\']([^"\']+)["\'][^>]*?(?:property|name)=["\'](og:image|og:image:secure_url|twitter:image|twitter:image:src)["\']',
    re.I,
)


class ImageCache:
    def __init__(self, allow_fetch: bool = True, refresh: bool = False):
        self.allow_fetch = allow_fetch
        self.refresh = refresh
        self.data: dict[str, str | None] = {}
        if CACHE_PATH.exists():
            self.data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        self.dirty = False
        self.fetched = 0

    def save(self) -> None:
        if self.dirty:
            CACHE_PATH.write_text(
                json.dumps(dict(sorted(self.data.items())), indent=1, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

    def lookup(self, url: str) -> str | None:
        if url in self.data and not (self.refresh and self.data[url] is None):
            return self.data[url]
        if not self.allow_fetch:
            return None
        try:
            img = self._fetch(url)
        except Exception:
            img = None
        self.data[url] = img
        self.dirty = True
        self.fetched += 1
        return img

    def _get(self, url: str) -> str:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/json;q=0.9,*/*;q=0.8"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.read(600_000).decode("utf-8", "replace")

    def _fetch(self, url: str) -> str | None:
        if "open.spotify.com/" in url:
            q = urllib.parse.quote(url, safe="")
            data = json.loads(self._get(f"https://open.spotify.com/oembed?url={q}"))
            return data.get("thumbnail_url") or None
        page = self._get(url)
        for rx in (META, META_REV):
            for m in rx.finditer(page):
                val = m.group(2) if rx is META else m.group(1)
                val = html.unescape(val).strip()
                if val.startswith("http"):
                    return val
        return None
