---
type: project-readme
project: Culture Vulture
created: 2026-07-06
---

# Culture Vulture

A vault-driven weekly culture digest. Every **Friday at 4am** (Pacific Time) a scheduled Claude task reads the config in this vault, trawls reputable UK and US culture sources (music weighted by `config/music-taste.md`, books by `config/reading-taste.md`), builds a Spotify playlist, saves a versioned copy here, logs the run, and drafts an email to chris.beaumont@gmail.com.

## How it fits together

```
Culture Digest (this vault)
├── config/
│   ├── trawl-instructions.md   ← EDIT THIS to change sources, topics, tone, counts
│   ├── email-template.md       ← EDIT THIS to change the email's layout
│   ├── music-taste.md          ← EDIT THIS to affect music taste
│   └── reading-taste.md        ← EDIT THIS to affect reading taste
├── emails/                     ← one saved markdown copy of each day's email
├── logs/
│   └── run-log.md              ← one row per run: date, status, item count, notes
├── site/
│   ├── build.py                ← renders emails/ into a static site (site/dist/)
│   └── style.css
└── README.md                   ← you are here
```

## The weekly flow

1. **Read config** — the task reads `config/trawl-instructions.md` and `config/email-template.md`.
2. **Trawl** — it searches the sources and topics named in the instructions.
3. **Build** — it renders the digest using the email template.
4. **Version** — it saves the rendered email to `emails/YYYY-MM-DD-culture-vulture.md` - version existing files with v1, v2, v3 etc if they are discovered when writing to this location.
5. **Log** — it appends a row to `logs/run-log.md`.
6. **Send** — it emails the digest via the connected Gmail tool.

## To change how it behaves

You never edit the scheduled task directly. Just edit the two notes in `config/`:

- Want different sources or an extra topic? → `config/trawl-instructions.md`
- Want a different email layout or tone? → `config/email-template.md`
- Want different music recommendations? → `config/music-taste.md`
- Want to fine tune reading recommendations? → `config/reading-taste.md`

The next 4am run picks up your changes automatically.

## The website

Every push to `main` on GitHub builds the site from `emails/` and deploys it to GitHub Pages. Nothing in the weekly flow changes: the task writes markdown, the site renders it.

- Preview locally: `pip install markdown pyyaml` then `python3 site/build.py --serve` and open http://localhost:8000
- Change the look: edit `site/style.css`
- Change what the pages contain: edit `site/build.py`
- Workflow: `.github/workflows/pages.yml`

## Dependencies

- **Gmail connector** must be authorized for the email to actually send. If it isn't connected, the task still saves the versioned email into `emails/` and notes the skipped send in the log — nothing breaks.
- Scheduled tasks run while the Claude app is open. If the app is closed at 4am, the task runs on next launch.
