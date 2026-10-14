---
type: config
config: trawl-instructions
updated: 2026-10-12
---

# Trawl Instructions

This note controls what the weekly digest looks for. Edit freely — the next run reads whatever is here.

## What this digest is

A **read / watch / listen** digest, not an events guide. Every pick must be something Chris can enjoy remotely — an album to stream, a book to read, a film or show to watch, a piece of art writing or criticism worth his time. Chris is **not** attending gigs, exhibitions, or theatre in person. Never frame a pick as "go and see it," and never recommend something whose only value is being there.

## Recipient

- chris.beaumont@gmail.com

## Geographic focus

**Light UK lean.** No proximity filter and no location gate — chase the most interesting culture wherever it is. Use UK / British work only as a mild tie-breaker for relevance and voice when picks are otherwise even.

## Recency

WEEKLY digest (sent Friday mornings). Prioritise items published, released, reviewed or reissued in roughly the past week, plus notable releases coming up in the week ahead worth knowing about. Avoid evergreen filler. Do not repeat picks from recent editions (check the latest files in `emails/`).

## Topics and how many items per topic

| Topic | Items | What counts |
|-------|-------|-------------|
| Music | 3–5 | New albums/singles/reissues — weight toward the taste profile in `config/music-taste.md`. No gigs or tours. |
| Art | 2–4 | Interesting artists, works, or art writing/criticism. Include an exhibition only if the *art itself* is genuinely interesting to read about or look at remotely — never as a "go see it" listing. |
| Books & Writing | 3–5 | New releases, reviews, essays, literary news — weight toward the taste profile in `config/reading-taste.md`. |
| Film & TV | 3–5 | New cinema releases (streaming or imminent), streaming picks, reviews. |

## The two-stage trawl (the important bit)

Every item goes through two stages. Discovery and the link are separate jobs.

**Stage 1 — discover and select.** Find what's worth recommending. Fish *first* in the pools that are already in-depth writing (reviews, features, essays, interviews, criticism); use listicles and roundups only as a completeness check ("did I miss anything major?"), never as the recommendation's source. Weight to the taste profiles. Bias selection toward items that already have a genuinely interesting piece attached — quality of the available read is part of what makes something worth picking.

**Stage 2 — attach the read/watch.** For each selected item, find the single best thing to read or watch *about that specific item*, and use that as the source link.

**Stage 2b — Music only: attach the Spotify album link.** For each Music pick, also find the album (or single/EP) on Spotify and include its `open.spotify.com/album/...` link as a **Listen** line above the Read/Watch line. Use the Spotify search tool first; if that is unavailable, search the web for the album's open.spotify.com URL. Confirm the link is the right artist and release (not a compilation, a different edition, or a different artist with the same name). This is in addition to the Read/Watch link, never a substitute. If the release is not on Spotify yet, omit the Listen line for that item and note it in the run log.

### What counts as a valid source link

Acceptable: a review, interview, profile, feature, essay, long-read, video essay or interview (e.g. YouTube), or podcast episode — about that one item.

**Never** use as the source link: any listicle or roundup, a venue listings / ticketing / booking page, a press release, a homepage, or a tag/search/category page.

Rules:
- **Paywalls:** prefer freely-readable pieces. A paywalled but excellent piece is fine — flag it as "(paywall)". **Exception:** Chris subscribes to The Atlantic, so its paywall never counts against a piece and needs no flag.
- **Verify:** confirm each link is actually about that item and is substantive (not a stub, mislabelled aggregator, or dead page) before including it.
- **Fallback when nothing dedicated exists yet** (e.g. an unreleased album): keep the item and attach the best weaker link you can find — an interview or preview, a YouTube video, a podcast, or an acclaimed adjacent piece (e.g. a review of the artist's previous work). A weaker good read beats dropping the pick or linking a listicle.

## Preferred sources

Use these for discovery and for the read/watch. The listings sources are for **discovery only** — never link them as a source.

- **General culture (UK):** The Guardian culture, BBC Culture, The Times / Sunday Times culture, The Telegraph culture, FT arts
- **General culture (US):** The New Yorker, The Atlantic (culture, books, fiction, comedy, photography, film, TV, music — Chris is a subscriber; use every culture section freely), New York Times arts, Vulture / New York Magazine, The Paris Review (Daily), Harper's
- **Music (UK):** The Quietus, NME (reviews and features, not roundups)
- **Music (US):** Pitchfork, Rolling Stone, Stereogum, Aquarium Drunkard, NPR Music, The Atlantic (music)
- **Film (UK):** Sight & Sound / BFI
- **Film (US):** Film Comment, Criterion (Current), IndieWire, RogerEbert.com, The Ringer, The Atlantic (film and TV)
- **Books (UK):** London Review of Books, The TLS, The Guardian books
- **Books (US):** New York Review of Books, The New York Times Book Review, Los Angeles Review of Books, The Millions, Bookforum, The Atlantic (books and fiction)
- **Art (US):** Artforum, Hyperallergic, ARTnews, The Atlantic (photography and visual culture)
- **Video / audio:** YouTube (video essays, interviews, sessions), reputable culture podcasts
- **Discovery-only (never linked):** Time Out, Londonist, venue listings

## Weekly Spotify playlist

Each run creates a private Spotify playlist via the Spotify `generate_playlist` tool. The prompt names only this week's Music picks (one track each, with a specific track where known), then asks for about 20 minus N lesser-known tracks by other artists that sound similar, described in a few words each, and closes with: one track per artist, no David Bowie, favour deep cuts over hits. Do not name artists from `music-taste.md` in the prompt: Spotify already blends in Chris's listening history, and naming them crowds out the week's picks. The digest must link to the playlist: one line at the end of the Music section, with the playlist's `open.spotify.com/playlist/...` URL, as laid out in `config/email-template.md`. Record the URL in the email's frontmatter as `playlist_url`. If the playlist could not be created, omit the line and say so in the run log.

## Tone

Concise, direct, friendly. Each item: a bold title, one or two sentences on why it's worth attention, then the read/watch link (and, for music, the Spotify album link). No filler.

## Editing tips

- To add a topic, add a row to the table above.
- To drop a source, delete it from the list.
- To change volume, edit the Items column.
