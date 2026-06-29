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

## Lens / angle — the SECOND axis (rotate this too)

Archetype = the *shape*. Lens = the *angle of meaning*. The failure mode: every caption is a
straight **description of the subject** ("a cyclist on a road…"), so even with rotated shapes the
batch feels same-y and a bit poemy/pretentious. Fix: vary the LENS across the batch, and keep the
**register** human — mostly calm-observational, but **rotate in warmth, play, and wit** so it
doesn't read as uniformly artsy. The world is surreal color-landscapes with a small figure (or
none); these lenses fit it.

**Favor (lead with these — human + playful, they cut the pretension):**
- **Character's inner voice** — give the figure a thought: `He's pretty sure this is a shortcut.`
- **Relatable / daily hook** — tie to the viewer's life: `Monday could use a road like this.`
- **Genuine question** — invite imagination (NOT bait): `Where would you point this road?`
- **Deadpan travelogue** — treat the impossible place as a real destination: `Postcard from a place that isn't there.`
- **Dry juxtaposition** — contrast two truths: `Extreme sport, gentlest palette.`
- **Light wordplay** — a small pun, e.g. on the grainy texture: `Going against the grain.`

**Keep (already in rotation):** meta-illusion / medium / viewer's-eye (`The arch is real; the river
is only light.`), the figure's obliviousness (`He rides like the hills aren't melting.`),
quiet feeling/mood, wry aside, and plain description — used **sparingly**, not as the default.

**Occasional (sprinkle, not every batch):** synesthetic (`Looks the way a held chord sounds.`),
scale-awe (`One small rider, an enormous idea.`), ultra-short punch (`Downhill, in every color.`).

**Avoid / rare:** stacking more meta than the keep-set; the "generative wink" (`No drone reached
this one.`) only **very rarely** — the account leads with its OWN style, not "this is AI."

**Register rule:** ~1-in-3 captions should land warm/friendly/casual (talk like a person), the rest
calm-observational. If a draft batch is all wistful/poetic, it's wrong — break it with a friendly or
playful one.

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
