---
date: 2026-05-11
status: draft-v1
version-target: Midjourney v7 (default May 2026), niji 6 noted
spec-block: as of 2026-05
source-urls:
  - https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw-Mode
  - https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards
  - https://medium.com/creative-1/steal-my-25-advanced-midjourney-photography-prompts-5f1f71703391
  - https://medium.com/design-bootcamp/15-midjourney-prompts-for-fashion-photography-5fc499cdce9b
  - https://blog.mlq.ai/midjourney-photography-prompts/
  - https://imaginewithrashid.com/16-midjourney-prompts-for-product-photography/
  - https://imaginewithrashid.com/20-midjourney-prompts-for-still-life-photography/
  - https://openart.ai/blog/post/midjourney-prompts-for-texture
  - https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/
---

# 04 — Examples and Patterns

This project's reference workflow assumes a **moodboard is already attached**. All examples below are written for that path: text prompt does scene/subject/light specification; moodboard does aesthetic. **Replace `<MB_CODE>` with the actual snapshot code from the relevant moodboard.**

> Camera/lens cue convention from [Medium "25 Advanced MJ Photography Prompts"](https://medium.com/creative-1/steal-my-25-advanced-midjourney-photography-prompts-5f1f71703391): writing `Canon RF 85mm f/1.2L` produces noticeably different bokeh and depth than `85mm lens` — Midjourney responds to brand-specific optical signatures.

## 4.1 Editorial portrait (Instagram feed, 4:5)

### Pattern

```
editorial portrait of [SUBJECT], [SCENE/ENVIRONMENT], [LIGHTING CUE], [COLOR/MOOD], shot on [CAMERA + LENS] --style raw --v 7 --ar 4:5 --profile <MB_CODE> --s 100
```

### Concrete example

```
editorial portrait of a woman in oversized wool coat, austere concrete interior, overcast window light, muted putty palette, shot on Canon RF 85mm f/1.2L --style raw --v 7 --ar 4:5 --profile <MB_CODE> --s 100
```

### Notes

- **`--style raw`** suppresses MJ's painterly default — critical for editorial fidelity ([Raw Mode](https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw-Mode)).
- **`--s 100`** (default stylize) is a deliberate baseline — the moodboard does the styling, not the stylize knob.
- Word count ≈ 22 words → well under the 40-word influence cap.
- Subject + scene + light + color + camera = 5 axes ([Prompt Basics](https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics)). Mood is implicit in moodboard.

## 4.2 Fashion campaign frame (single subject, full body)

### Pattern

```
[full-body | half-body | close-up] fashion photograph of [SUBJECT WITH WARDROBE], [LOCATION CUE], [LIGHT CUE], [TIME-OF-DAY], [FILM/CAMERA CUE] --style raw --v 7 --ar 4:5 --profile <MB_CODE>
```

### Concrete examples

(a) **Quiet-luxury studio editorial:**
```
half-body fashion photograph of a model in raw linen tunic, plaster-white seamless studio backdrop, soft north-facing daylight, late morning, Hasselblad medium format --style raw --v 7 --ar 4:5 --profile <MB_CODE>
```

(b) **Outdoor narrative:**
```
full-body fashion photograph of a figure in long charcoal trench, deserted coastal road, overcast diffused light, late autumn, Fujicolor Pro 400H film grain --style raw --v 7 --ar 4:5 --profile <MB_CODE>
```

### Notes

- Fashion benefits from **specific film/camera cues** more than editorial portraits — the medium signature is part of the aesthetic.
- For **calmer / more controlled output**, do NOT add `--c` or `--weird`. Defaults are correct.
- For consistent characters across a campaign, see V7 `--oref` (this is character consistency territory, not pure reference generation; not the primary need for this project).

## 4.3 Surface / material study (texture, no subject)

### Pattern

```
extreme close-up of [MATERIAL] surface, [SURFACE STATE], [LIGHT], [SCALE CUE] --style raw --v 7 --ar 1:1 --profile <MB_CODE> --q 2
```

### Concrete examples

(a) **Linen fold detail:**
```
extreme close-up of crumpled raw linen surface, slight diagonal fold, single soft window light from upper left, macro scale --style raw --v 7 --ar 1:1 --profile <MB_CODE> --q 2
```

(b) **Concrete patina:**
```
extreme close-up of weathered concrete wall, fine cracking and water staining, even ambient light, eye-level macro --style raw --v 7 --ar 1:1 --profile <MB_CODE> --q 2
```

(c) **Repeating tileable material:**
```
top-down close-up of woven wool fabric, neutral oat color, even soft light --style raw --v 7 --tile --q 2 --profile <MB_CODE>
```
*Note*: `--tile` produces seamless repeats — most reliable at `--ar 1:1`. Don't combine with non-square aspect ratios.

### Notes

- **`--q 2`** doubles render time; worth it for surface work where fine grain is the point.
- **No mood / no narrative words** — surface studies are diagnostic. The moodboard supplies the aesthetic register; prompt supplies the material spec.
- "Macro" + "extreme close-up" together: redundant in current MJ but the redundancy clarifies scale. ~~Inflates token count~~ — keep one.

## 4.4 Object still-life

### Pattern

```
still life of [OBJECT], [SET DRESSING], [SURFACE], [LIGHT], [CAMERA POSITION] --style raw --v 7 --ar 4:5 --profile <MB_CODE>
```

### Concrete examples

(a) **Single-object hero shot:**
```
still life of a worn leather notebook, alone on a raw oak desk, soft side window light, eye level --style raw --v 7 --ar 4:5 --profile <MB_CODE>
```

(b) **Composed grouping:**
```
still life of three hand-thrown ceramic cups arranged in a triangle, on linen runner over weathered wood, low afternoon light from left, three-quarter angle --style raw --v 7 --ar 4:5 --profile <MB_CODE>
```

(c) **Object grammar emphasis** (per project LESSONS.md "object grammar / material action" rule):
```
still life of a folded raw silk panel partially draped over a stone slab, contact shadow visible, single soft north window light, eye level --style raw --v 7 --ar 4:5 --profile <MB_CODE>
```
*Note*: `folded`, `draped`, `contact shadow` = the "object grammar / material action" cues that prevent slipping into anonymous abstract-form output (per `.claude/rules/LESSONS.md` 2026-05-09 entry).

## 4.5 Mixed: moodboard + sref code

When the moodboard nails the *register* but you want a specific *color/light treatment* on top, combine:

```
[text prompt with subject/scene/light cue] --profile <MB_CODE> --sref <COMMUNITY_CODE> --style raw --v 7 --ar 4:5
```

Note: while moodboard is active, **`--sw` does not work** ([Moodboards docs](https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards) via WebSearch snippet) — you cannot tune sref strength while moodboard is attached. To re-enable sref weighting, drop the moodboard and rely on sref alone.

## 4.6 Mixed: image prompt + moodboard (composition lock)

When you have a curated composition you want to *match* (overhead flat-lay grid, specific subject placement) and a moodboard for aesthetic:

```
https://your.candidate.url/composition.jpg [text prompt for subject] --iw 1.5 --profile <MB_CODE> --style raw --v 7 --ar 4:5
```

`--iw 1.5` biases toward composition match while leaving the moodboard's aesthetic averaging in play. If composition still drifts, raise to `--iw 2`.

## 4.7 Permutation patterns for batch testing

When validating a new moodboard against multiple lanes, run a permutation:

```
[base text prompt] --style raw --v 7 --profile <MB_CODE> --ar {1:1, 4:5, 9:16}
```

→ Three jobs in one command, each at a different aspect ratio. Useful for: "does this moodboard hold up across feed (1:1), portrait (4:5), and story (9:16)?"

Pro plan / Mega plan required for permutations on Discord ([Permutations](https://docs.midjourney.com/hc/en-us/articles/32761322355597-Permutations)).

## 4.8 Niji (anime) — covered briefly

Niji is the anime-tuned model track. For this project's editorial / fashion / surface lanes, **Niji is generally the wrong tool**. Niji only enters if a specific creative brief calls for an anime / manga / illustration register that the main model can't produce believably.

Pattern for completeness:
```
[scene + subject], [emotion cue], detailed anime illustration --niji 6 --style expressive --ar 4:5
```

Niji-only style flags: `--style cute`, `--style scenic`, `--style expressive`, `--style original` (defaults to `original`). Use `--style raw` to suppress the strongest anime tells if you need a more illustrative-but-grounded look. Source: [Welcome to Niji V6](https://nijijourney.com/blog/niji-updates-welcome-to-niji-v6) via WebSearch snippet.

## 4.9 Anti-patterns to avoid (cross-ref [05_pitfalls-and-tips.md](./05_pitfalls-and-tips.md))

- **Long flowery descriptions** (50+ words) — words past ~40 are weighted near zero.
- **Multiple `--no` flags** — only the last one is read; use one comma-list.
- **Stacking `--sref` + `--p` + `--style raw` + `--v 7` + `--niji 6`** — `--niji` is its own model track, conflicts with `--v`.
- **`--cref` in V7 prompts** — silently ignored; use `--oref`.
- **`--p code1::3 code2::1`** — moodboard ignores per-code weight; the `::N` is dropped silently.
- **Adding camera/lens cue without `--style raw`** — the painterly default fights the photographic intent; output will look "AI photo-illustration" instead of believable photography.
