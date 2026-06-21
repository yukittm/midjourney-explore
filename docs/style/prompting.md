---
updated: 2026-06-21
status: active
type: guide
---

# Prompting — convention, recipe, idea moves

The single place for **how to write prompts** for this project. The style *model* (the 2 dials, the
giz natural world, color/finish) lives in [[style-definition]]; this is the craft. The generation
**recipe (§7) is a draft pending Phase-1 validation — not yet a skill.** Pairs with [[reference-accounts]].

## 1. Anatomy (moodboard workflow)

```
[shot/angle] , [subject + attributes + action] , [setting] , [light]   --params
```
- Specify **subject / scene / light**; **do NOT write style/medium** — the moodboard owns aesthetic.
  The one allowed exception is a **finish cue** (grain / blur / matte), used sparingly.
- Front-load the load-bearing words; ~30–40 words (a soft V7-era heuristic, non-official — not a hard cap).
- Params at the end; no commas inside a param block.

## 2. Detail convention (the dial)

| Mode | Goal | Detail |
|---|---|---|
| **Lock / produce** | a specific look, consistency | **high** (kill degrees of freedom) |
| **Explore / ideate** | find new images | **looser** (room = variety & serendipity) |

**Project default = the detailed end of the ~30–40-word envelope** — richly specify subject + composition
+ light; style stays on the moodboard. Loosen for exploration. (Research agrees on direction: "describe
the subject and scene, not the art style" — research 06 Q1; the bundle's "~30-word" floor is left frozen.)

## 3. Narrowing slots (vague → concrete)

who/what + attributes (`a woman in a long red coat`, not `a figure`) · count (fewer = more coherent) ·
action/pose · setting (`a cracked white salt flat`, not `a landscape`) · time/light · framing. Specify the
**few key elements richly**; MJ can't honor many-element micro-layout.

## 4. Always-on rules

- ≤ ~40 words; front-load.
- Don't stack redundant adjectives ("soft moody cinematic ethereal" → bland average).
- One `--no` flag, comma-separated.
- With a moodboard: detail the **subject**, not the style.

## 5. Style strength vs fidelity (knobs)

- **Stylize `--s`**: low (~50) = literal/prompt-faithful; high (250–1000) = moodboard/MJ aesthetic dominates
  and overrides prompt detail. (Observed: `--s 400` flattened a specified tennis court into a red plain;
  ~50 restored it.) `--s` is also the **render-register knob** (graphic ↔ photoreal — see [[style-definition]]).
- **Variety `--c`**: 0 for consistency; 15–30 to spread the 4-grid while exploring.
- **`--style raw`**: more literal/photographic; softens the painterly register — A/B it.
- **`--seed`**: lock to iterate in one direction.

## 6. Exact reproduction → image prompt

Text only *approximates*. To copy a real reference's composition/content, use the image itself as an
**image prompt** (`--iw`, e.g. `--iw 2`) — far more faithful than words. (Note: `--oref` is **V7-only and
invalid on V8.1**, the current default — use `--iw`.)

## 7. The generation recipe (DRAFT — pending Phase-1 validation; not a skill yet)

For producing **varied, intentional, on-style** prompts. Built on the **2-dial model** in [[style-definition]].

### Modes — 2 dials (sample both; they are independent)
- **Dial 1 — subject dominance**: pure-landscape (**heroless is first-class**) → minor subject → photoreal hero.
- **Dial 2 — render register (3-stop)**: flat-graphic / **soft-painterly (the characteristic middle)** / crisp-photoreal.
  Register is **not** derived from the subject — sample it independently (esp. to reach the soft-painterly middle).

### Variation axes (pick one value each = the artistic intention)
- **Shot distance**: extreme-close / close / mid / wide / aerial. *Rotate it; don't default to wide; include close-ups.*
- **Camera angle**: eye-level / low / high / top-down / profile.
- **Focal idea**: name the ONE idea. If there is a hero, give a **subordination lever** (scale / sharpness /
  color-isolation / negative-space). **Heroless-but-device-driven is allowed.**
- **Density**: **≤3 element-types** (an "element-type" = a distinct named subject/object class; sky, ground,
  and light do not count). Richness = one element's texture, not element count.
- **Compositional device (exactly ONE = the "idea")**: mirroring / scale-tension / leading-line /
  juxtaposition / framing / negative-space / motion-echo.
- **Render register** (Dial 2 above) — sampled independently of subject.
- **Mood**: witty / tender / sublime / melancholy / kinetic. **Light**: golden / clean-midday / dusk / overcast.

### Conceptual moves (the idea engine)
1. **Scale inversion** — giant / tiny (a man riding a giant antelope).
2. **Impossible juxtaposition** — right subject, wrong context (horses among clouds).
3. **Material swap** — substance becomes something else (liquid-marble figure).
4. **Mundane act on a vast stage** — everyday action made monumental by the setting.
5. **Object as monument** — an everyday object huge / central in a landscape.
6. **Figure-on-animal composite** — a figure fused with an animal as one hero (the antelope rider).

> Method: pick a subject × one move → a strong idea.

### Anti-patterns (reject + re-sample)
- **Idea-less inventory** (no device) — this, NOT "heroless", is the real failure (heroless color-field landscapes are valid).
- **Element-listing / >3 element-types.**
- **Default-wide** — justify wide by a scale/mirror idea; cap it per batch.
- **Style/medium words** (moodboard owns style); finish cues OK, sparingly.
- **"Pleasant wallpaper"** — no device, no tension.

### Batch diversity (generating N)
- Rotate **shot distance** (≥1 close-up; cap wide).
- **Unique device** per prompt.
- Rotate **hero category** incl. **"landscape (no hero)"**.
- **Single-lane override**: if the user asks for ONE lane/mode (e.g. "6 color-field landscapes"), honor it
  — do **not** force diversity.
- **Color → the moodboard** (a color-coherent giz moodboard gives unity — see [[style-definition]] color note).

### Output
- N prompts, ~30–40 words, **color left to the moodboard**.
- For a **photoreal hero**, append: *anchor realism with a real photo as image prompt (`--iw ~2`).*
- Tag each prompt: **mode · register · device · shot** (for curation).

## 8. Idea seeds (running list — rate, then feed keepers back into the moodboard)

| # | Move | Prompt | Verdict |
|---|------|--------|---------|
| 1 | swap | `a footballer dribbling a glowing planet across a dark field of stars` | ☐ |
| 2 | scale | `a goalkeeper leaping to catch a falling moon over an empty grass stadium` | ☐ |
| 3 | juxtaposition | `two teams playing football on the rings of a distant planet, dust and starlight` | ☐ |
| 4 | mundane×vast | `a lone sprinter trailing a comet's tail across an endless white salt flat` | ☐ |
| 5 | scale + animal | `a tiny figure leading a herd of cloud-sized white horses over the hills` | ☐ |
| 6 | object-monument | `a grand piano half-buried in a desert dune, a small figure playing it at dusk` | ☐ |

_Kept / loved:_ (record prompt + frame as favorites are picked)

## 9. Per-lane templates

Don't write from scratch. Keep a base template per lane (the §1 slots pre-filled for that world) and swap
the subject. High detail, fast, consistent.
