---
type: config
config: email-template
updated: 2026-10-08
---

# Email Template

This note defines the layout the digest email follows. The task renders HTML from this structure. Placeholders in `{{ }}` are filled at run time. Edit the structure, headings, or intro style and the next run follows it.

## Subject line

`Culture Digest — {{date}}`

## Body structure

Each item separates the **recommendation** from the **read/watch**. The title and one-line "why" come first; the link underneath points to something genuinely worth reading or watching about that item — never a listicle or listings page.

```
# Culture Digest — {{date}}

{{one-line intro summarising the week's highlights}}

## 🎵 Music
- **{{title}}** — {{one or two sentences on why it's worth attention}}
  Listen: [{{album title}} on Spotify]({{open.spotify.com/album/... url}})
  Read/Watch: [{{piece title or description}}]({{url}}){{ (paywall) if applicable}}
- ...

🎧 This week's picks as a Spotify playlist: [Culture Digest — {{date}}]({{open.spotify.com/playlist/... url}}) (open it and tap Add to save it to your library)

## 🎨 Art
- **{{title}}** — {{one or two sentences}}
  Read/Watch: [{{piece title or description}}]({{url}}){{ (paywall) if applicable}}
- ...

## 📚 Books & Writing
- **{{title}}** — {{one or two sentences}}
  Read/Watch: [{{piece title or description}}]({{url}}){{ (paywall) if applicable}}
- ...

## 🎬 Film & TV
- **{{title}}** — {{one or two sentences}}
  Read/Watch: [{{piece title or description}}]({{url}}){{ (paywall) if applicable}}
- ...

---
Generated {{timestamp}} · edit sources in config/trawl-instructions.md
```

## Rendering notes

- Output a clean, skimmable HTML email. Keep it readable in a couple of minutes.
- Bold each item title; keep the "why" to one or two sentences.
- Every Music item has two links: a **Listen** link to the album (or single/EP) on Spotify, then the **Read/Watch** link. The Spotify link never replaces the Read/Watch link. If no Spotify album link can be found, omit the Listen line for that item and note it in the run log.
- The Music section ends with one **playlist line** linking the Spotify playlist created for this week's run. Omit the line if no playlist was created, and note it in the run log.
- Every item has exactly one **Read/Watch** link, and it must be a substantive read or watch about that specific item — a review, interview, profile, feature, essay, video, or podcast. Never a listicle, roundup, listings, ticketing, or homepage link.
- Prefer freely-readable pieces; append "(paywall)" when the best piece is paywalled.
- Omit a section entirely if no worthwhile items were found for it that week (note the omission in the run log).
- Keep the emoji section markers unless this note is edited to remove them.
