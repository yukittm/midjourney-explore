# caption — reference

Detail tables for the `caption` skill. The method, voice, and rules live in `SKILL.md`;
read this file when a section there points you here (or when you need an exemplar).

## Contents
- Vetted hashtag library
- Alt-text exemplar
- Worked examples (the live grid)
- Caption archetypes (5 peers — rotate)
- Hard constraints (validate.py-owned)
- AI labeling

## Vetted hashtag library

Neutral medium / technique descriptors, listed **general → specific** (keep this order;
rotate *which* tags, expand the pool as you vet more in-app):

`digitalart`, `abstractart`, `generativeart`, `midjourneyart`, `aiartcommunity`

- **Retired — do not use:** `surrealart` (self-praising / aesthetic-quality claim).
- **Never invent a tag** (e.g. `colorfieldart`); verify it exists in-app before use.

## Alt-text exemplar

Literal, descriptive (subject + colors + composition), one per image:

> "A surreal Mediterranean scene — a small cream villa with a terracotta roof, cypress
> and flowering shrubs on a green islet in a deep blue sea, with a winding path of grainy
> deep-red, green and teal color leading up to the house."

## Worked examples (the live grid)

- **`long-way-home`** (live) — one line, axis absorbed (the default): `Home, the long
  way.` Villa on an islet, winding color path; wavelength/objects felt in "the long way,"
  never named. *(Posted with `surrealart` + an unordered tag set — now superseded by the
  Hashtags rules.)*
- **`color-window`** (published 2026-06-25, deleted 2026-06-27) — two-line, axis explicit:
  `A quiet valley, and a window the color won't sit still in.` / `Geometry, holding a
  wavelength. 🌊` **Deleted because its color read too close to `long-way-home`** — the
  reason the gate's palette-collision STOP exists.

> ⚠️ **Both live captions above are the SAME shape** (a noun-phrase fragment) — they are
> the historical record, **NOT the variety target**. For *shape*, imitate the 5 archetypes
> below, not these two.

## Caption archetypes (5 peers — rotate; no default)

All inherit the Voice; each is a DIFFERENT grammatical shape, so rotating them makes
variety structural. Keep each **short (~6–14 words)** with a **keyword in the first line**.
Use a different archetype each post and across a batch; never the same shape back-to-back.

- **M1 — fragment** (noun phrase, no verb): `A hot spring, ringed in color. One to keep.`
- **M2 — full sentence** (has a verb): `Color runs downhill through the saguaro desert.`
- **M3 — quiet question** (a line + one genuine question; a reach beat): `A green river in a
  red canyon. Too calm to be real?`
- **M4 — first-person "what I chased"** (low-key maker's voice): `I kept the coast road
  moving and the cyclist still.`
- **M5 — two-line axis-signature** (line 2 names Geometry / Wavelength / Objects; the ~20%
  axis-stated quota): `Low sun strung across the dunes.` / `Objects, learning to flow.`

**Overlay (optional, ~1 in 5 posts max):** a short **save / send** line appended to any
archetype (e.g. `One to keep for a grey day.`) — the only reach CTA besides M3's question;
never both in one caption, never baity.

## Hard constraints (owned by `automation/igpub/validate.py`)

- Caption ≤ 2200 chars; the **first line is the hook** (~125 chars show before "more" —
  front-load the payload, which matters for two-line shapes).
- Hashtags: cap **5** (the platform cap is also 5 as of Dec 2025); **no leading `#`**.
- Image assets JPEG, aspect 4:5 .. 1.91:1; **carousels must be single-aspect-ratio**.

This skill writes text only; the pipeline validates after you write the record.

## AI labeling

- **Manual path:** enable IG's AI-content label where it reads naturally; no disclosure
  text in the caption body (transparency-only, per the strategy doc).
- **Automated path:** pick a deterministic default when that step is built (recommended:
  always enable the toggle). Deferred until then.
