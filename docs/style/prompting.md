---
updated: 2026-06-27
status: active
type: guide
---

# Prompting — method, registers, idea moves

The single place for **how to write prompts** for this project. The style *model* lives in
[[style-definition]]; current MJ parameter behavior in `../research/2026-06-21_midjourney-v8.1-current.md`;
this is the craft. Pairs with [[reference-accounts]].

**Core method (validated in-app 2026-06-23):** **realism is scoped to the subject + hard anchors** — rendered
**photo-textured** via the kernel (§1) or **clean/legible** in the smooth-wave base route. **Color** comes from
one bold **image `--sref`**, not the moodboard (§2). An abstract-feeling background is reached by **grounding it
in a real, photographable phenomenon** — the **bridge** (§4) — across the **base + sibling registers** (BASE =
R3 Flowing Color Waves; SIBLINGS = R1/R2, §5), each with **one decisive light or a clean color-flow** (§5b) and
scored against the **reward gate** (§10) before shipping.

## 1. The realism kernel (realism scoped to subject + anchors)

**The subject + hard anchors read as real** — **photo-textured** via this kernel (the photoreal route), or
**clean/legible** in the smooth-wave base route (profile + higher `--s` + no-raw). The kernel (photoreal route):

- **`--style raw`** — always on (the photographic base, not an A/B option).
- **low `--s` (~90–120)** — `--s` is the realism/literalness knob; keep it low (the project's tightened band inside the web-verified photoreal zone ~50–150).
- **photographic cues** in the prompt text: a camera/lens (`85mm f/1.8`), a film stock (`Cinestill 800T`,
  `Kodak Portra 400`), and `editorial photograph, sharp realistic skin/texture`.
- **`--no painting, illustration, 3d render, cgi`** — one flag, comma-list.

> Raw mutes *automatic* color, not *specified* color — raw + a bold sref = vivid **and** photographic. Never
> push realism or color with `--s`.

## 2. The color channel (one bold image sref)

Color = a **single bold image `--sref`** (a saturated reference image), **not** the moodboard — a moodboard
*averages* toward a muted centre and **can't be weighted** (`--sw`/`--sv` don't apply to it). Push color with
**`--sw` (~150–250)**. **Do NOT write `--sv`** for an image-URL sref on V8.1 → it defaults to **sv7** (the V8.1
default, `--hd`-compatible). Writing `--sv 7` explicitly errored in-app; numeric CODES need sv4/sv6.
To make color more vivid, raise **`--sw`** — **never `--s`**.

**Convention: set the `--sref` IMAGE in the MJ UI** (Style Reference slot) — do **not** paste `--sref <URL>`
into the prompt body (a placeholder URL won't run). When a reference image is needed, state it **separately**
from the prompt body; keep only **`--sw`** in the text:

    --sw 180   (with the bold reference image set in the UI)

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

## 5. Background registers — base + siblings

Neutral names — **never put an artist name in the prompt or vocabulary.** **BASE = R3 Chromatic Wave (Flowing
Color Waves)** — most batches center here; **SIBLINGS = R1 Color-Block Terrain · R2 Geometric Landform**. Each
pairs the §1 kernel (photoreal route) — or, for R3, the smooth-wave route — with a background recipe + param band.

### R1 — Color-Block Terrain (SIBLING)
Bold color on **real terrain** (a field, a hillside, a plain). Color is in the land, not in a "style".
- **Params:** `--style raw --s 110 --sw 180 --ar 4:5 --no painting, illustration, 3d render, cgi`
- **Example:**

      a woman in a cobalt coat standing on a vast red-earth plain under a clear deep-blue sky, editorial
      photograph, sharp realistic skin texture, 85mm f/1.8, Cinestill 800T
      --style raw --s 110 --sw 180 --ar 4:5 --no painting, illustration, 3d render, cgi

### R2 — Geometric Landform (SIBLING)
Geometry from **real geometric land** — terraced fields, basalt columns, salt-pond grids — **not** the words
"geometric" / "minimalist". Name the real noun.
- **Params:** `--style raw --s 100–120 --sw 150 --ar 4:5 --no painting, illustration, 3d render, cgi`
- **Example:**

      a lone figure walking across stepped emerald rice terraces at golden hour, hexagonal basalt columns at the
      ridge, editorial photograph, sharp skin texture, 85mm f/1.8, Kodak Portra 400
      --style raw --s 110 --sw 150 --ar 4:5 --no painting, illustration, 3d render, cgi

### R3 — Chromatic Wave  (BASE — Flowing Color Waves; validated)
The flowing multicolor "wave" world. **Two routes:** **photoreal** (the bridge §4 — a real flowing-color
phenomenon behind a photo-textured subject) or **smooth-painterly** (profile `--p` + higher `--s` + no-raw —
subject clean/legible; this is the keepers' route).
- **Params (photoreal route):** `--style raw --s 100–110 --sw 220–250 --ar 4:5 --no painting, illustration, 3d render, cgi`
- **Params (smooth-wave route):** `--p <profile> --s ~250 --c 10 --ar 4:5` (no raw)
- **Example (photoreal route):**

      a dancer in white mid-turn before sweeping multicolor tulip-field bands stretching to the horizon,
      editorial photograph, sharp realistic skin, 85mm f/1.8, Cinestill 800T
      --style raw --s 105 --sw 240 --ar 4:5 --no painting, illustration, 3d render, cgi

### Deferred — Pure Color-Field
A true paint/gradient field with no real referent → needs a **2-step composite**; **out of the automated
one-pass path** (see the §4 breakpoint).

## 5b. Decisive treatment (commit to one — never flat/auto, never a muddy blur)

For the **photoreal route**, commit to ONE light:
- **Hard / high-key graphic light** — flat, clean, poster light; large saturated color blocks; pairs with
  heroless / geometric / color-field scenes. Cue: `hard high-key midday light, flat bold color blocks, crisp shadows`.
- **Golden warm-directional light** — low sun, long warm shadows, rich material texture; pairs with a present
  human/animal subject. Cue: `golden low directional light, long warm shadows, rich texture`.

These are the photoreal route's lights — **NOT a second render mode**. The **smooth-wave route** instead commits
to a **clean, legible, directional color-flow** (not a muddy smear). Either way the treatment is *decisive*;
flat/auto light or a directionless blur is the "thin" failure.

## 5c. Scale ↔ abstraction (how literal the subject reads)

Tie the subject's *abstraction* to how large it sits in frame:
- **Large / filling the frame** → the subject can become the color itself (made-of-wave, half-dissolved into the
  flowing color); a frame-filling subject also **overrides the sref's native composition**.
- **Small / scattered** → render it **realistic and solid**; small subjects get absorbed by the sref's template,
  so keep them literal and let the flowing color live in the terrain/ground around them.

A subject that's small *and* asked to "be the color" tends to collapse back into the sref's default scene — size
it up, or move the color into the surroundings.

## 6. Anatomy & slots

    [shot/angle] , [photoreal subject + attributes + action] , [real terrain/phenomenon = the register] ,
    [kernel cues: editorial photograph, lens, film stock]   --style raw --s --sw --ar --no …   (sref image set in the UI)

Narrow vague → concrete (specify the **few key elements richly**; MJ can't honor many-element micro-layout):
- **who/what + attributes** — `a woman in a long red coat`, not `a figure`
- **count** — fewer = more coherent
- **action / pose**
- **the real background noun** — `a cracked white salt flat` / `stepped rice terraces`, not `a landscape` or
  `an abstract field` (this noun IS the register; §4–5)
- **time / light**, **framing**

## 6b. Figures — style them on purpose; keep multiples distinct

**Style figures intentionally — anonymous is the default failure.** Left generic ("a skateboarder", "a figure"),
MJ renders a bland, characterless person. Give every figure a **deliberate, of-the-moment wardrobe identity** —
a defined fashion / era / subculture aesthetic — kept **muted** so it never competes with the color chord
(GATE ②). The *specific* aesthetic is a per-piece / per-series art-direction choice (one example among many),
**not** a fixed rule; commit to ONE look per batch for cohesion. At small scale, identity reads from
**silhouette, build, posture and a held prop**, not garment detail — spend the words there (logos / fabric /
brand cues don't survive downscaling, and a literal logo is off-brief).

**Multiple people → de-clone deliberately** (MJ clones repeated same-type figures by default):
- **Enumerate each as a distinct individual** — vary build / height / skin tone / pose — plus the word
  *different*; this (not any param) is the lever. State the **shared wardrobe ONCE** for the group, vary only the
  bodies.
- **`--chaos` / `--weird` / `--no` do NOT de-clone** (chaos = variety *between* the 4 grid images; `--no
  identical` is a weak, split-prone negative). Don't rely on them for this.
- **Keep the count low** — a hard count mildly amplifies cloning, and **small multiple figures also malform**
  (too few pixels). Prefer **one** figure (cleanest, and on-brand for a lone subject); for 2–3, expect to curate.
- **Deterministic fallback:** build the group **one figure at a time** with Pan / Vary-Region, or
  **batch-and-curate** the clean grids. Text alone is probabilistic for multiple distinct people.

## 7. Length & differentiation — rich is the PRODUCTION default

Two different jobs — don't conflate them:
- **Hitting the LOOK** — length is **not** the lever; the **kernel + sref/profile + naming the real
  phenomenon** do that (a short prompt can hit the look). Short prompts are for a quick style-check **only**.
- **DIFFERENTIATION at scale** — **DETAIL is the lever.** Under-specifying hands MJ its *average*, so a mass of
  prompts **collapses to sameness**. For production/variety, write a **rich ~80-word scene spec**: specific
  subject + attributes + action · the **named flowing phenomenon / terrain** · light · composition (fore /
  mid / background) · atmosphere · camera. The detail is what makes each variant genuinely distinct.

**Default to a rich ~80-word prompt for production.** (Short is the exception.) This requires **low `--s`** so
the detail is honored — **high `--s` (the smooth-wave / profile route) overrides prompt detail and re-averages**,
so it is the LOW-differentiation route. For differentiated scenes use the **bridge / photoreal route**
(raw + low `--s` + rich prompt + sref).

- Front-load load-bearing words; the ~74-token influence cap still applies — spend the budget on the *scene*,
  not filler. **Never ship a short, under-specified prompt for production** (it averages → sameness).

## 8. Knobs (quick reference — full table in `../research/2026-06-21_midjourney-v8.1-current.md`)

- **`--style raw`** — always on (kernel); the photographic base.
- **`--s` (stylize, ~90–120)** — literalness only. Low = prompt-faithful; high overrides prompt detail and
  re-muddies. Never use it for realism or color.
- **`--sw` (~150–250)** — the color channel; raise `--sw` to push color. **Omit `--sv`** for an image-URL sref (it defaults to sv7, the V8.1 default; writing `--sv 7` errored in-app; numeric codes need sv4/sv6).
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

## 9b. Remix-Fidelity lane (variation around a keeper)

When a keeper's color/look is good and you want **more of that world** — vary the same subject, or swap to a
new subject while keeping **~the same texture / palette / composition**:

- Put the keeper in **BOTH** the **Image-Prompt (Remix)** slot **and** the **Style Reference** slot.
- `--style raw --s 110 --sw ~220 --ar 4:5 --no painting, illustration, 3d render, cgi` (Personalization /
  moodboard **OFF** — the look comes from the source in both slots).
- **Keep the prompt** → variations of the same subject. **Rewrite the prompt (rich ~80 words)** → a NEW subject,
  same texture/color/world.

Why it works: the source in **both slots** locks the look (color + composition); raw + low `--s` + the rich
prompt render the (new) subject with detail, not averaged → **high source-fidelity + a differentiated subject**.
Validated in-app 2026-06-23 (the dancers / surfer sets: `raw · s110 · sw 220–230 · source in both slots`).

Caveat: it **also inherits the source's composition** — ideal for a subject swap that fits a similar layout. For
a genuinely different composition or a different palette, use §9c (sref-only, the prompt owns composition), the from-scratch route (§5/§7),
or the explore lane (§9). Remix **Subtle** = stay very close to the source; **Strong** = let the new prompt push further.

## 9c. Change the subject (and composition) — keep ONLY the style

The default for moving a fixed style onto a **genuinely new subject/scene** (where §9b's both-slots lane would
drag a keeper's layout in). Carry the **style only**; let the prompt own the subject AND its composition:

- **Image `--sref` ONLY** (the Style-Reference slot) — put **nothing** in the Image-Prompt / Remix slot.
  `--sref` transfers *style* (color / medium / texture), **not** subject or composition; the Remix / image-prompt
  slot is what imports a layout. **Dropping Remix is what frees the new composition** — raising `--sw` will not
  fix a dragged layout (it only moves color).
- **A rich, subject-first prompt** describing the new subject AND the composition you want — give the subject
  enough "mass" that it isn't absorbed into the sref's native scene.
- **Low `--s` (~90–110)** so the prompt's composition is honored; high `--s` re-averages toward the house look
  and the sref's layout (the §7 low-differentiation trap). Tune the *palette* with `--sw`, never the subject.

The §9b both-slots lane is the **opposite** tool — reserve it for a subject swap that keeps ~the same layout.
**Destination (automation):** a trained `--p` profile carries the style as *taste*, compositionally neutral by
construction (§11) — the cleanest long-term version of this once `--p` is locked.

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
- **Register** — BASE R3 (Flowing Color Waves) / SIBLINGS R1, R2 (§5); realism stays scoped to subject + anchors.
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
- **Painterly / illustrated *subject*** — the subject + hard anchors must read real (photo-textured, or clean/legible in the wave route). A smooth painterly *background/world* in the wave route is fine; only a flat/illustrated *subject* fails.
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

### The reward gate (score every output before shipping — positive tests, must PASS all four)
- **GATE ① — Subject & hard anchors read as real.** The subject and the load-bearing real objects/structures it touches are rendered convincingly — **photo-textured** in the kernel route, or **clean/legible** in the smooth-wave route; realism stays SCOPED to subject + anchors. *Fails if* the subject reads flat/illustrated/painted, or an anchor dissolves into the background.
- **GATE ② — Saturated signature chord present.** The bold chord (saturated red/orange + green + deep-blue) is clearly readable — not washed out (`--sw` too high), pastel-faded, or muted/grey.
- **GATE ③ — Exactly ONE surreal idea, with restraint.** One clear idea against generous negative space (≤3 element-types; **heroless is fine**). *Fails if* idea-less (an inventory) OR multi-idea / busy.
- **GATE ④ — Decisive, legible color/light.** Color and light commit to ONE logic; the image reads as a **clean directional color-flow or block** — a legible flow PASSES. *Fails if* a muddy/directionless blur, flat/auto/ambiguous light, OR a muddy literal in-between (neither clean-graphic nor warm-rich).

Only gate-passing images reach the user's selection. This gate **is** the definition of "on-style" — the anti-drift check (full text: [[style-definition]] → *The objective & the reward*).

## 11. Consistency stack (for automation)

For a stable house look across many images (the IG-automation goal), stack deterministic layers — not per-prompt
`--sref` juggling alone:

- **Trained Personalization `--p`** — the platform's stable-taste layer (trained via the like/dislike loop).
- **Fixed image `--sref --sw`** — pin the exact palette with one bold reference image (omit `--sv` on V8.1).
- **Deterministic post-grade LUT** — a saved Lightroom/Capture One preset or a LUT in `automation/` gives the
  *exact* editorial color reproducibly (MJ color sampling is not deterministic).

Not for consistency: **`/tune`** is **subject-fragile**; **`--seed`** is **same-prompt-only**.

## 12. Per-register base templates

Don't write from scratch. Keep a base template **per register** (BASE R3 + SIBLINGS R1/R2 — the §5/§6 slots
pre-filled, the kernel/route + params fixed) and swap only the subject + the real background noun. Fast,
consistent, on-style.

## 13. Idea seeds (running list — rate, then feed keepers into the `--sref` / `--p` training)

| # | Move | Prompt | Light | Verdict |
|---|------|--------|-------|---------|
| 1 | scale-inversion | `a lone figure beside a single colossal leaning monolith on a vast green hill, deep cobalt sky` | hard graphic | ☐ |
| 2 | impossible-juxtaposition | `a small wooden rowboat adrift on a perfectly still mirror lake set into a red flowering field` | golden warm | ☐ |
| 3 | object-as-monument | `a giant brass key half-buried upright in a pale salt flat, tiny figure at its base` | hard graphic | ☐ |
| 4 | material-swap | `a flock of birds turning to drifting white smoke over an ochre badland ridge` | golden warm | ☐ |
| 5 | mundane×vast | `a beekeeper tending a single tall white hive on an immense striped tulip-field slope` | golden warm | ☐ |
| 6 | mirroring | `a lone cypress and its reflection bisecting a turquoise salt pond under a hard noon sun` | hard graphic | ☐ |

_All seeds sit in the surreal-natural world; each names ONE decisive light. Keep subjects fresh — invent new
ones, don't recycle these verbatim._

_Kept / loved:_ (record prompt + frame as favorites are picked)
