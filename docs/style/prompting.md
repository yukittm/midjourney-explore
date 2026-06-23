---
updated: 2026-06-23
status: active
type: guide
---

# Prompting — method, registers, idea moves

The single place for **how to write prompts** for this project. The style *model* lives in
[[style-definition]]; current MJ parameter behavior in `../research/2026-06-21_midjourney-v8.1-current.md`;
this is the craft. Pairs with [[reference-accounts]].

**Core method (validated in-app 2026-06-23):** every real subject (person/animal) is rendered **photoreal**
via a fixed **realism kernel** (§1). **Color** comes from one bold **image `--sref`**, not the moodboard (§2).
Because V8.1 realism is **global** (§3), an abstract-feeling background is reached not by mixing styles in one
pass but by **grounding it in a real, photographable phenomenon** — the **bridge** (§4) — expressed through one
of **three background registers** R1/R2/R3 (§5), each lit with **one decisive light** (§5b) and scored against
the **reward gate** (§10) before shipping.

## 1. The realism kernel (foreground invariant — all modes)

**Real subjects (people, animals) are ALWAYS photoreal**, in every register. Lock realism with this fixed
kernel — it does not vary by subject or mood:

- **`--style raw`** — always on (the photographic base, not an A/B option).
- **low `--s` (~90–120)** — `--s` is the realism/literalness knob; keep it low.
- **photographic cues** in the prompt text: a camera/lens (`85mm f/1.8`), a film stock (`Cinestill 800T`,
  `Kodak Portra 400`), and `editorial photograph, sharp realistic skin/texture`.
- **`--no painting, illustration, 3d render, cgi`** — one flag, comma-list.

> Raw mutes *automatic* color, not *specified* color — raw + a bold sref = vivid **and** photographic. Never
> push realism or color with `--s`.

## 2. The color channel (one bold image sref)

Color = a **single bold image `--sref`** (a saturated reference image), **not** the moodboard — a moodboard
*averages* toward a muted centre and **can't be weighted** (`--sw`/`--sv` don't apply to it). Push color with
**`--sw` (~150–250)**. **Do NOT add `--sv`** for an image sref on V8.1 — `--sv 7` is **rejected** ("Unsupported
Style Reference version 7 for --version 8.1") and `--sv 6` is incompatible with `--hd`; let MJ use its default.
To make color more vivid, raise **`--sw`** — **never `--s`**.

    --sref <bold image URL> --sw 180

## 3. Mechanics — V8.1 realism is global

`--style raw` and `--s` act on the **whole frame**; there is **no per-region control**, and `::` is **emphasis,
not placement**. So you **cannot** force "photoreal foreground + abstract background" in one pass by mixing raw
/ no-raw or high/low `--s` per region. The way out is the bridge (§4): make the background itself a real,
photographable thing, so one global raw + low-`--s` render produces both at once.

## 4. The bridge — grounding abstract backgrounds in real phenomena

To get an abstract / flowing-color background **and** a photoreal figure in **one pass**, name a **real,
photographable phenomenon** as the background, not an abstract style word. Raw + low `--s` then render that
flowing color *photographically* — abstract-feeling, but real.

Real flowing/blocked-color phenomena to name (the noun, not "abstract" / "gradient"):
- multicolor crop or **tulip bands**, flower-field strips
- **painted-desert / Zhangye Danxia** rainbow rock strata
- **contour-plowed** or terraced fields
- **salt-evaporation ponds** (color-block grids)
- **aerial color bands** of farmland / coastline

> **Breakpoint:** drone-photographable → one-pass works. Pure paint / gradient / no real referent → not
> one-pass; defer to a 2-step composite (out of the automated path).

## 5. Three background registers (R1 / R2 / R3)

Neutral names — **never put an artist name in the prompt or vocabulary.** Each register pairs the §1 kernel
(always on) with a background recipe and a fixed param band.

### R1 — Color-Block Terrain
Bold color on **real terrain** (a field, a hillside, a plain). Color is in the land, not in a "style".
- **Params:** `--style raw --s 110 --sref <URL> --sw 180 --ar 4:5 --no painting, illustration, 3d render, cgi`
- **Example:**

      a woman in a cobalt coat standing on a vast red-earth plain under a clear deep-blue sky, editorial
      photograph, sharp realistic skin texture, 85mm f/1.8, Cinestill 800T
      --style raw --s 110 --sref <bold URL> --sw 180 --ar 4:5 --no painting, illustration, 3d render, cgi

### R2 — Geometric Landform
Geometry from **real geometric land** — terraced fields, basalt columns, salt-pond grids — **not** the words
"geometric" / "minimalist". Name the real noun.
- **Params:** `--style raw --s 100–120 --sref <URL> --sw 150 --ar 4:5 --no painting, illustration, 3d render, cgi`
- **Example:**

      a lone figure walking across stepped emerald rice terraces at golden hour, hexagonal basalt columns at the
      ridge, editorial photograph, sharp skin texture, 85mm f/1.8, Kodak Portra 400
      --style raw --s 110 --sref <bold URL> --sw 150 --ar 4:5 --no painting, illustration, 3d render, cgi

### R3 — Chromatic Wave  (validated)
Flowing multicolor via the **bridge** (§4) — a real flowing-color phenomenon behind a photoreal figure.
- **Params:** `--style raw --s 100–110 --sref <URL> --sw 220–250 --ar 4:5 --no painting, illustration, 3d render, cgi`
- **Example:**

      a dancer in white mid-turn before sweeping multicolor tulip-field bands stretching to the horizon,
      editorial photograph, sharp realistic skin, 85mm f/1.8, Cinestill 800T
      --style raw --s 105 --sref <bold URL> --sw 240 --ar 4:5 --no painting, illustration, 3d render, cgi

### Deferred — Pure Color-Field
A true paint/gradient field with no real referent → needs a **2-step composite**; **out of the automated
one-pass path** (see the §4 breakpoint).

## 5b. Decisive light (commit to one — both photoreal)

Always **commit to ONE light logic** — never flat/auto. Two on-style treatments, both photoreal:
- **Hard / high-key graphic light** — flat, clean, poster light; large saturated color blocks; pairs with
  heroless / geometric / color-field scenes. Cue: `hard high-key midday light, flat bold color blocks, crisp shadows`.
- **Golden warm-directional light** — low sun, long warm shadows, rich material texture; pairs with a present
  human/animal subject. Cue: `golden low directional light, long warm shadows, rich texture`.

This is a light lever *within* the photoreal kernel — **NOT a second render mode**. (Our early R1/R2 "thin"
outputs had flat/auto light; committing to one decisive light is the fix that makes an image read "finished.")

## 6. Anatomy & slots

    [shot/angle] , [photoreal subject + attributes + action] , [real terrain/phenomenon = the register] ,
    [kernel cues: editorial photograph, lens, film stock]   --style raw --s --sref --sw --ar --no …

Narrow vague → concrete (specify the **few key elements richly**; MJ can't honor many-element micro-layout):
- **who/what + attributes** — `a woman in a long red coat`, not `a figure`
- **count** — fewer = more coherent
- **action / pose**
- **the real background noun** — `a cracked white salt flat` / `stepped rice terraces`, not `a landscape` or
  `an abstract field` (this noun IS the register; §4–5)
- **time / light**, **framing**

## 7. Length is not the lever

Write **as much detail as needed** to pin (a) the real subject/phenomenon and (b) the kernel — no more. V8.1
honors length, so a detailed prompt is fine; but length is **not** the goal and **don't pad**.
In-app (2026-06-23) a ~85-word body and the simple ~20-word originals **both** produced the look — so the
levers are the **kernel + naming the real subject/phenomenon (incl. the bridge) + the sref**, not word count.

- **Do** front-load the load-bearing words; cut filler past ~74 tokens (it loses influence).
- **Don't** ship a lazy 2-word prompt — specify the subject and the real background noun.
- **Don't** chase a word target. A precise short prompt can beat a padded long one.

## 8. Knobs (quick reference — full table in `../research/2026-06-21_midjourney-v8.1-current.md`)

- **`--style raw`** — always on (kernel); the photographic base.
- **`--s` (stylize, ~90–120)** — literalness only. Low = prompt-faithful; high overrides prompt detail and
  re-muddies. Never use it for realism or color.
- **`--sw` (~150–250)** — the color channel; raise `--sw` to push color. **Omit `--sv`** for an image sref (V8.1 rejects `--sv 7`; `--sv 6` is incompatible with `--hd`).
- **`--no painting, illustration, 3d render, cgi`** — one flag, comma-list; each word parsed independently
  (moderation trap: `--no modern clothing` = "no modern" + "no clothing").
- **`--c` (chaos)** — 0 for production; **15–30 for the explore lane** (§9).
- **`--seed`** — repeatable for the **same prompt only**; not a cross-prompt consistency tool.
- **`--iw` (0–3)** — to copy a real reference's composition, use the image as an image prompt (`--iw ~2`); far
  more faithful than words. (`--oref` is **V7-only and invalid on V8.1** — use `--iw`.)

## 9. Explore lane (un-preset discovery)

Separate from the production registers: a discovery lane that drops the fixed sref/params and opens variety
with **`--c 15–30`** to find new looks. Surface candidates here; once something lands, re-express it through the
kernel + a register (R1/R2/R3) for production. Don't mix the explore lane into a production batch.

## 10. The idea engine

### Variation axes (pick one value each = the artistic intention)
- **Shot distance**: extreme-close / close / mid / wide / aerial. *Rotate it; don't default to wide; include close-ups.*
- **Camera angle**: eye-level / low / high / top-down / profile.
- **Focal idea**: name the ONE idea. If there is a hero, give a **subordination lever** (scale / sharpness /
  color-isolation / negative-space). **Heroless-but-device-driven is allowed.**
- **Density**: **≤3 element-types** (a distinct named subject/object class; sky, ground, light don't count).
  Richness = one element's texture, not element count.
- **Compositional device (exactly ONE = the "idea")**: mirroring / scale-tension / leading-line / juxtaposition
  / framing / negative-space / motion-echo.
- **Background register** — pick R1 / R2 / R3 (§5); the subject stays photoreal regardless.
- **Mood**: witty / tender / sublime / melancholy / kinetic. **Light (decisive — pick one, §5b)**: hard high-key graphic OR golden warm-directional. Never flat/auto.

### Conceptual moves (the idea engine)
1. **Scale inversion** — giant / tiny.
2. **Impossible juxtaposition** — right subject, wrong context.
3. **Material swap** — substance becomes something else.
4. **Mundane act on a vast stage** — everyday action made monumental by the setting.
5. **Object as monument** — an everyday object huge / central in a landscape.
6. **Figure-on-animal composite** — a figure fused with an animal as one hero.

> Method: pick a subject × one move → a strong idea. Keep subjects **fresh** (don't recycle a specific prior
> subject; see `.claude/rules/LESSONS.md`).

### Anti-patterns (reject + re-sample)
- **Painterly / illustrated subjects** — a real subject must be photoreal; if it reads painted, the kernel is
  missing or `--s` is too high.
- **Abstract style words for the background** — "geometric", "minimalist", "abstract", "gradient" don't render
  reliably; name a **real noun** (terraces, basalt columns, tulip bands) — §4.
- **Color pushed via `--s`** — re-muddies; push color with `--sw`.
- **Moodboard used as the color channel** — it averages to a muted centre and can't be weighted; use a bold
  image `--sref`.
- **Artist name in the prompt or vocabulary** — never; use the neutral register names.
- **Idea-less inventory** (no device) — this, NOT "heroless", is the real failure (heroless color-field is valid).
- **Element-listing / >3 element-types** — richness = one element's texture, not element count.
- **Lazy 2-word prompt** — name the subject and the real background noun (§7).
- **Flat / auto / ambiguous light** — always commit to ONE decisive light (§5b); flat "auto" light reads thin.
- **Muddy literal in-between** — neither clean-graphic (hard light + flat color blocks) nor warm-rich (golden light + texture). Pick a side and commit.

### Batch diversity (generating N)
- Rotate **shot distance** (≥1 close-up; cap wide).
- **Unique device** per prompt.
- Rotate **hero category** incl. **"landscape (no hero)"**.
- **Hold or rotate the background register** deliberately (one register for batch unity, or rotate for range).
- **Single-lane override**: if the user asks for ONE lane/register, honor it — do **not** force diversity.
- **Color → the `--sref` + `--sw`** (one bold image sref gives unity; never push color via `--s`).

### Output
- N prompts, each = the kernel + a register + **one decisive light** (§5b); **color via `--sref` + `--sw`**.
- For a **photoreal hero**, optionally anchor with a real photo as image prompt (`--iw ~2`).
- Tag each prompt: **register · device · shot · light** (for curation).

### The reward gate (score every output before shipping)
Before surfacing a generation, score it against [[style-definition]] → *The objective & the reward*. **Reject
and re-sample any image that fails a GATE:** ① photoreal subject · ② saturated signature chord (not
washed/muted) · ③ exactly ONE surreal idea + restraint (idea-less = reject; **heroless OK**) · ④ **decisive
light** (not flat/auto). Only gate-passing images reach the user's selection. This gate **is** the definition
of "on-style" — it is the anti-drift check.

## 11. Consistency stack (for automation)

For a stable house look across many images (the IG-automation goal), stack deterministic layers — not per-prompt
`--sref` juggling alone:

- **Trained Personalization `--p`** — the platform's stable-taste layer (trained via the like/dislike loop).
- **Fixed image `--sref --sw`** — pin the exact palette with one bold reference image (omit `--sv` on V8.1).
- **Deterministic post-grade LUT** — a saved Lightroom/Capture One preset or a LUT in `automation/` gives the
  *exact* editorial color reproducibly (MJ color sampling is not deterministic).

Not for consistency: **`/tune`** is **subject-fragile**; **`--seed`** is **same-prompt-only**.

## 12. Per-register base templates

Don't write from scratch. Keep a base template **per register** (R1/R2/R3 — the §5/§6 slots pre-filled, the
kernel + params fixed) and swap only the photoreal subject + the real background noun. Fast, consistent,
on-style.

## 13. Idea seeds (running list — rate, then feed keepers into the `--sref` / `--p` training)

| # | Move | Prompt | Light | Verdict |
|---|------|--------|-------|---------|
| 1 | scale-inversion | `a lone figure beside a single colossal white egg resting on a vast green hill, deep cobalt sky` | hard graphic | ☐ |
| 2 | impossible-juxtaposition | `a small wooden rowboat adrift on a perfectly still mirror lake set into a red flowering field` | golden warm | ☐ |
| 3 | object-as-monument | `a giant brass key half-buried upright in a pale salt flat, tiny figure at its base` | hard graphic | ☐ |
| 4 | material-swap | `a flock of birds turning to drifting white smoke over an ochre badland ridge` | golden warm | ☐ |
| 5 | mundane×vast | `a beekeeper tending a single tall white hive on an immense striped tulip-field slope` | golden warm | ☐ |
| 6 | mirroring | `a lone cypress and its reflection bisecting a turquoise salt pond under a hard noon sun` | hard graphic | ☐ |

_All seeds sit in the surreal-natural world; each names ONE decisive light. Keep subjects fresh — invent new
ones, don't recycle these verbatim._

_Kept / loved:_ (record prompt + frame as favorites are picked)
