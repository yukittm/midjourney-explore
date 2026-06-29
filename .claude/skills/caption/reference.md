# caption — reference

Detail tables for the `caption` skill. The method, voice, and rules live in `SKILL.md`;
read this file when a section there points you here (or when you need an exemplar).

## Contents
- Variation palette (the two axes: shapes × angles)
- Vetted hashtag library
- Alt-text exemplar
- Worked examples (the live grid)
- Hard constraints (validate.py-owned)
- AI labeling

## Variation palette — the two axes

Variety is structural, built on two dials: **Shape** (the grammatical form) and **Angle**
(the lens of meaning). Use them as a **generation menu** — pick one of each to write *from* —
but judge variety by **reading the recent grid**, not by avoiding the last label. Keep repeats
**non-adjacent** rather than banning them (a batch larger than the 5 shapes *must* repeat
shapes — that's fine; just no two alike adjacent, and no visible rotor across the set). The
recurring trap is letting the angle default to plain subject-description — keep that rare and
lead with the human/playful angles instead.

### Axis 1 — Shapes (5 peers; rotate, no default)

Each is a different grammatical form, so rotating them makes variety structural. Keep each
**short (~6–14 words)** with a keyword in the first line.

- **S1 — fragment** (noun phrase, no verb): `A hot spring, ringed in color. One to keep.`
- **S2 — full sentence** (has a verb): `Color runs downhill through the saguaro desert.`
- **S3 — quiet question** (a line + one genuine question; doubles as a reach beat):
  `A green river in a red canyon. Too calm to be real?`
- **S4 — first-person** (low-key maker's voice): `I kept the coast road moving and the
  cyclist still.`
- **S5 — two-line axis-signature** (line 2 names Geometry / Wavelength / Objects — the ~20%
  axis-stated quota): `Low sun strung across the dunes.` / `Objects, learning to flow.`

### Axis 2 — Angles (the lens; rotate, favor human/playful)

The angle decides *whose view it is and what it's really about*. Spread these across a
batch. Tiers below are how often to reach for each — not a ranking of quality.

**Favor (lead here — human + playful; these cut the pretension):**
- **Character's inner voice** — give the figure a thought: `He's pretty sure this is a shortcut.`
- **Relatable / daily hook** — tie it to the viewer's life: `Some Mondays need a road like this.`
- **Genuine question** — invite imagination, NOT bait: `Where would you point this road?`
- **Deadpan travelogue** — treat the impossible place as a real destination:
  `Found this arch on the color coast. Not real, sadly.`
- **Dry juxtaposition** — set two truths against each other: `Extreme sport, gentlest palette.`
- **Light wordplay** — a small pun (e.g. on the grainy texture): `Going against the grain.`

**Keep in the mix (don't over-rely):** meta — illusion / medium / the viewer's eye
(`The arch is real; the river is only light.`); the figure's obliviousness (`He rides like
the hills aren't melting.`); quiet feeling / mood; a wry aside; and **plain description —
sparingly**, never the default.

**Occasional (a sprinkle, not every batch):** synesthetic (`Looks the way a held chord
sounds.`); scale-awe (`One small rider, an enormous idea.`); ultra-short punch
(`Color, finding the sea.`).

**Rare:** the "generative wink" (`No drone reached this one.`) — only once in a long while;
the account leads with its OWN style, not "this is AI."

**Save/send overlay (optional, ~1 in 5 max):** any caption may append ONE short save/send
line (`one to keep for a grey day`). It's the only reach CTA besides the S3 question — never
use both in one caption, never make it baity.

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

The live set changes — **step 2's scan finds the real current baseline at runtime**; treat
these as illustrations of shape/angle, not a fixed list.

- **`long-way-home`** — S1 fragment, plain-description angle, axis absorbed: `Home, the long
  way.` *(Posted with `surrealart` + an unordered tag set — superseded by the Hashtags rules.)*
- **`sphere-in-the-air`** — S1 fragment, plain-description: `A coral moon, low over a
  restless sea.`
- **`ringed-hot-spring`** — S5 two-line, axis stated (Wavelength): `A hot spring, ringed in
  quiet color.` / `Wavelength, holding still.`
- **`color-window`** (published 2026-06-25, **deleted 2026-06-27**) — S5 two-line: `A quiet
  valley, and a window the color won't sit still in.` / `Geometry, holding a wavelength. 🌊`
  **Deleted because its color read too close to `long-way-home`** — the reason the gate's
  palette-collision STOP exists.

> ⚠️ Notice these early posts cluster on **shape (mostly fragment / two-line) and angle
> (plain description)** — that clustering IS the monotony to beat. They are the historical
> record, **NOT the variety target**: generate from the full palette above, and check by
> reading the recent grid (not by matching a label).

## Hard constraints (owned by `automation/igpub/validate.py`)

- **Caption + hashtags ≤ 2200 combined** — `validate.py` budgets the *assembled* string
  (caption + blank line + space-joined `#tags`), not the caption alone. The **first line is
  the hook** (~125 chars show before "more" — front-load the payload, and for two-line shapes
  keep the discoverable noun in line 1, not line 2).
- Hashtags: cap **5** (the platform cap is also 5 as of Dec 2025); **no leading `#`**.
- Image assets JPEG, aspect 4:5 .. 1.91:1; **carousels must be single-aspect-ratio**.

This skill writes text only; the pipeline validates after you write the record.

## AI labeling

- **Manual path:** enable IG's AI-content label where it reads naturally; no disclosure
  text in the caption body (transparency-only, per the strategy doc).
- **Automated path:** pick a deterministic default when that step is built (recommended:
  always enable the toggle). Deferred until then.
