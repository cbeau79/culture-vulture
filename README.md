---
type: project-readme
project: Culture Vulture
created: 2026-07-06
---

# Culture Vulture

A weekly culture digest. Every **Friday at 03:54 Pacific**, a scheduled Claude task runs in the cloud. It clones this repo, reads the config, trawls reputable UK and US culture sources (music weighted by `config/music-taste.md`, books by `config/reading-taste.md`), builds a Spotify playlist, drafts an email to chris.beaumont@gmail.com, saves the digest and a log row here, and pushes. The push rebuilds the website.

This repo is the single source of truth. The task does not use the Obsidian vault or any local computer.

## How it fits together

```
culture-vulture (this repo)
├── config/
│   ├── trawl-instructions.md   ← EDIT THIS to change sources, topics, tone, counts
│   ├── email-template.md       ← EDIT THIS to change the email's layout
│   ├── music-taste.md          ← EDIT THIS to affect music taste
│   └── reading-taste.md        ← EDIT THIS to affect reading taste
├── emails/                     ← one saved markdown copy of each week's digest
├── logs/
│   └── run-log.md              ← one row per run: date, status, item count, notes
├── site/
│   ├── build.py                ← renders emails/ into a static site (site/dist/)
│   ├── images.py               ← finds album art / article preview images for picks
│   ├── images.json             ← cache of those lookups (committed; one line per link)
│   └── style.css
└── README.md                   ← you are here
```

## The weekly flow

1. **Clone**: the task clones this repo into its cloud workspace.
2. **Read config**: it reads the four notes in `config/` and the last two digests, to avoid repeats.
3. **Trawl**: it searches the sources and topics named in the instructions.
4. **Build**: it renders the digest using the email template.
5. **Playlist**: it creates a private Spotify playlist from the week's music picks.
6. **Save**: it writes the digest to `emails/YYYY-MM-DD-culture-digest.md`.
7. **Draft**: it creates a Gmail draft of the digest. Nothing sends automatically; `scripts/send-digest.py` is a separate manual send path.
8. **Log**: it appends a row to `logs/run-log.md`.
9. **Publish**: it commits `emails/` and `logs/` and pushes to `main`, which rebuilds the website.

## To change how it behaves

You never edit the scheduled task directly. Edit the notes in `config/` on GitHub, or ask Claude to:

- Want different sources or an extra topic? → `config/trawl-instructions.md`
- Want a different email layout or tone? → `config/email-template.md`
- Want different music recommendations? → `config/music-taste.md`
- Want to fine tune reading recommendations? → `config/reading-taste.md`

The next Friday run picks up your changes automatically.

## The website

Live at https://cbeau79.github.io/culture-vulture/. Every push to `main` builds the site from `emails/` and deploys it to GitHub Pages.

- Preview locally: `pip install markdown pyyaml` then `python3 site/build.py --serve` and open http://localhost:8000
- Change the look: edit `site/style.css`
- Change what the pages contain: edit `site/build.py`
- Images come from Spotify (album art) and each article's own preview image. Lookups are cached in `site/images.json`; run `python3 site/build.py --refresh-images` to retry picks that have none.
- Workflow: `.github/workflows/pages.yml`

## Dependencies

- **Gmail connector** must be authorised for the draft to be created. If it isn't, the task still saves the digest to `emails/` and notes the skipped draft in the log.
- **Spotify connector** for the playlist. If it fails, the digest goes out without the playlist line.
- The task runs in the cloud, so no computer or app needs to be open.
