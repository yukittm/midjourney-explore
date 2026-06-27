# caption — reference

Detail tables for the `caption` skill. The method, voice, and rules live in `SKILL.md`;
read this file when a section there points you here (or when you need an exemplar).

## Contents
- Vetted hashtag library
- Alt-text exemplar
- Worked examples (the live grid)
- Caption template menu (T1–T5)
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
  reason the gate's palette-collision STOP exists. Use the two-line explicit shape
  sparingly, to vary.

## Caption template menu (T1–T5)

Rotate; never repeat. **T5 / the one-liner is the live exemplar.** T1–T4 are legacy
multi-line shapes — reach for them rarely, to break monotony, never as the default.

- **T5 — minimalist (live):** `Color, mid-sentence.` 🌊
- **T1 — sensory + save CTA (legacy):** `Teal folding into gold, the moment before it
  spills over.` / `Save this for a grey day. 🌊`
- **T2 — question (legacy):** `[one evocative line]` / `If this were a sound, what would
  it be?`
- **T3 — process (legacy):** `[what I chased]` / `I wanted color to feel like [motion] —
  no subject, just the phenomenon.` / `№[N] in the [series] series.`
- **T4 — series (legacy):** `№[N]. [one sensory line]` / `Part of "[series]" — [the
  through-line].` / `Save the set. 🔖`

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
