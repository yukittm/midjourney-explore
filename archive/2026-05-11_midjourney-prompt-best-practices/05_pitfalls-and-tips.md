---
date: 2026-05-11
status: draft-v1
version-target: Midjourney v7 (default May 2026)
spec-block: as of 2026-05
source-urls:
  - https://docs.midjourney.com/hc/en-us/articles/32173351982093-No
  - https://docs.midjourney.com/hc/en-us/articles/32658968492557-Multi-Prompts-Weights
  - https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw-Mode
  - https://aituts.com/midjourney-shorten/
  - https://medium.com/@alexcarltully/how-i-use-underscores-to-get-more-out-of-my-midjourney-prompts-1972f69d9306
  - https://kikiandmozart.beehiiv.com/p/tricks-for-effective-midjourney-prompts
  - https://www.whytryai.com/p/midjourney-negative-prompt
  - https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/
  - https://geekycuriosity.substack.com/p/midjourney-mixing-moodboard-style
---

# 05 — Pitfalls and Tips

## 5.1 Token budget — the silent dropper

### The 74-token cap

> "Any tokens beyond the 74-token limit are ignored by Midjourney. … The longer your prompt is, the more likely Midjourney is to assign a weight of 0.00 to important keywords, especially later on in the prompt." — [Aituts /shorten guide](https://aituts.com/midjourney-shorten/) (secondary; widely cited)

> ⚠️ 推測: I could not extract the exact 74-token limit from the official Midjourney docs in this sandbox (403). It is widely cited across multiple independent sources; treat as strong heuristic.

### The ~40-word drop-off

> "Once you exceed a certain number of words, the influence of subsequent words on the final result becomes negligible, and anything written after approximately 40 words has minimal impact." — same source.

### Practical tips

1. **Front-load the load-bearing words**: subject, medium, key aesthetic adjective, key light cue. Camera/lens last among the optional bits.
2. **Use `/shorten` (Discord)** to see Midjourney's actual token weighting and a suggested tightened prompt. ([Aituts /shorten guide](https://aituts.com/midjourney-shorten/))
3. **Underscore-fuse multi-word terms**: `north_window_light` is one token; `north window light` is three. ([Alex Tully — underscores in MJ prompts](https://medium.com/@alexcarltully/how-i-use-underscores-to-get-more-out-of-my-midjourney-prompts-1972f69d9306))
4. **Push aesthetic load to the moodboard**, leave the prompt for spec.

## 5.2 `--no` parsing — the moderation trap

### One flag, comma list

> "You cannot include multiple `--no` commands in your description, but should separate each exclusion term with commas within a single `--no`, for example: `--no shadows, color, gradients`." ([No](https://docs.midjourney.com/hc/en-us/articles/32173351982093-No) via WebSearch snippet)

`--no shadows --no color` is wrong — only one `--no` is honored.

### Each word is independent

> "Midjourney's moderation system reads every word you add to the `--no` parameter independently. This means if you prompt `--no modern clothing` it will read that as 'no modern' and 'no clothing'! This interpretation can accidentally trigger a warning, as it might seem like you're requesting an image of someone without clothing. In this case, include the type of clothing you do want in your prompt, rather than using `--no`." (same source via WebSearch snippet)

### Effective `--no` patterns

- ✅ Single nouns: `--no text, watermark, logo, signature`
- ✅ Concrete visual elements: `--no shadows, gradient, blur`
- ❌ Adjective+noun pairs: `--no modern clothing` — read as two separate negations.
- ❌ Compound concepts: `--no AI artifacts` — "no ai" + "no artifacts" is incoherent.
- **Negative prompts work better as positive prompts in reverse**: instead of `--no painted look`, write `--style raw` + `photographic`. Direct positive guidance often beats negative.

### `--no` is internally a `-0.5` weight

> "Using the no parameter is the same as using a -0.5 weight." ([No](https://docs.midjourney.com/hc/en-us/articles/32173351982093-No))

So `--no shadows` ≈ `shadows::-0.5` in the prompt. If you need stronger suppression, use multi-prompt with explicit negative weight: `... shadows::-1`. Remember total weight must remain positive.

## 5.3 Over-styling — the AI-photo giveaway

The most common Midjourney editorial failure mode is the "AI photo-illustration" register: technically a photograph, aesthetically a painting in disguise. Causes:

- **Default `--style` (no `--style raw`)** → painterly bias kicks in. Always add `--style raw` for editorial / fashion / surface / product.
- **High `--s` (>200) on photographic prompts** → MJ adds artistic interpretation that fights the photo intent. Stay at 50–150 for photo work.
- **Stacking adjectives** ("soft cinematic moody dramatic ethereal") → MJ averages, picks the median register, often lands on "stylized" instead of "literal."
- **Personalization profile bias** in V7 — your trained taste leaks into every prompt unless you toggle off or override with moodboard.

### Antidotes

| Symptom | Fix |
|---|---|
| Output looks like a painting of a photo | Add `--style raw`; lower `--s` to 50. |
| Skin / fabric texture too smooth | Add `--q 2`; specify film grain (e.g., `Fujicolor Pro 400H film grain`). |
| Light is dramatic when you wanted overcast | Specify lighting precisely (`overcast diffused light, no direct sun`). |
| Output looks generic-AI even with moodboard | Reduce text prompt length (let moodboard do more); add specific camera + lens. |

## 5.4 Weight collisions

### Multi-prompt sum must be positive

> "Just remember, the total of all weights in your prompt needs to be a positive number." ([Multi-Prompts & Weights](https://docs.midjourney.com/hc/en-us/articles/32658968492557-Multi-Prompts-Weights) via WebSearch snippet)

`A::1 B::-2` will reject. `A::2 B::-1` is fine.

### Moodboard ignores weight, sref honors it

```
--p MB_A::3 MB_B::1   ← :: dropped silently (and duplicate codes deduped)
--sref CODE_A::3 CODE_B::1   ← weights respected
```

### Moodboard active blocks `--sw` and `--sv`

If you mix moodboard + sref, the sref's `--sw` (style weight) is **inactive**. To tune sref strength, you must drop the moodboard.

## 5.5 Version drift — the time bomb

### Symptoms

- A prompt that worked in V6.1 produces a different output today.
- A community sref code that "should" produce a specific aesthetic now misses.

### Causes

- V7 became default 2025-06-16 ([Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version) via WebSearch snippet); existing prompts without `--v 6.1` silently switched.
- V7 sref version differs from V6 — old codes drift unless `--sv 4` is added ([Style References for V7](https://updates.midjourney.com/style-references-for-v7/) via WebSearch snippet).
- V8 alpha is rolling out (V8.0 2026-03-17, V8.1 2026-04-30); when V8 becomes default, the same drift will recur.

### Prevention

- **Always pin the version**: `--v 7` (or `--v 6.1`) on every prompt. Never rely on default.
- **Record the seed** (`--seed N`) for any output you may need to regenerate later.
- **Snapshot the moodboard code** at the time of generation (the `--profile` alphanumeric, not the `m...ID`), since the snapshot persists across moodboard edits and deletion ([Geeky Animals — Mastering Moodboard](https://geekycuriosity.substack.com/p/mastering-midjourney-moodboard)).

## 5.6 V7-specific gotchas

1. **Personalization required**: V7 won't generate at all until you've ranked ~40 image pairs ([V7 Alpha](https://updates.midjourney.com/v7-alpha/) via WebSearch snippet). Plan ~5 minutes for first-time setup.
2. **Personalization on by default**: every V7 prompt is biased by your trained profile unless you toggle off or override with a different moodboard as default. For attributable output, set the project moodboard as default.
3. **`--cref` is incompatible with V7** — silently ignored. Use `--oref` for V7 character/object identity.
4. **`--oref` costs 2x GPU** ([Omni Reference](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference) via WebSearch snippet); plan accordingly.
5. **Vary Region, Pan, Zoom Out** still use V6.1 internally even when your prompt is V7 — don't expect V7 fidelity from these post-generation operations.
6. **Inpainting / outpainting** also still use V6.1; the `--oref` reference does **not** carry through.

## 5.7 Moodboard-specific gotchas

1. **Two ID formats with different persistence rules** (see [03_image-prompts-and-moodboard.md §3.4](./03_image-prompts-and-moodboard.md)). Save the snapshot code at every generation.
2. **Snapshot code changes on every image add/remove** ([Geeky Animals](https://geekycuriosity.substack.com/p/mastering-midjourney-moodboard)). If audit trail matters, freeze the moodboard before a production run.
3. **No per-image weight inside a moodboard** — to bias toward one aesthetic, add more copies of that aesthetic's images.
4. **Mixed-style moodboards average toward chaos**. If you put illustration + photography + 3D-render in one moodboard, output averages to an unstable middle. Keep moodboards register-coherent.
5. **Moodboard cannot use `--sw` / `--sv`** — if you need sref tuning, drop the moodboard.
6. **A moodboard with too few images** (< 4) behaves unpredictably; the averaging effect needs enough samples. The Chase Jarvis-cited 5–10 floor is a reasonable starting point. ([Chase Jarvis](https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/))

## 5.8 General prompt hygiene checklist (this project)

Before sending a prompt:

- [ ] `--v 7` (or `--v 6.1`) explicitly set
- [ ] `--style raw` if photographic intent
- [ ] `--ar X:Y` matches downstream IG slot (4:5 / 1:1 / 9:16)
- [ ] `--profile <snapshot-code>` (not `--p m...ID`) for audit trail
- [ ] Text prompt under ~30 words (moodboard does aesthetic load)
- [ ] One `--no` flag, comma-separated terms, no adjective+noun pairs
- [ ] No stacking of redundant adjectives ("soft moody cinematic ethereal")
- [ ] Camera/lens cue specific (`Canon RF 85mm f/1.2L`) not generic (`85mm`)
- [ ] Personalization state known: either default-profile = this moodboard, or Personalization toggled off
- [ ] Seed recorded if regeneration may be needed (`--seed N`)
- [ ] Moodboard snapshot code + image list logged for the run

## 5.9 When the prompt isn't the problem

If the same moodboard + same prompt + similar text descriptions keep producing outputs that miss the intent, the issue is usually upstream:

- **Moodboard is internally incoherent** (mixed registers, mixed lighting eras, mixed media). Audit and re-curate.
- **The intent is not actually in the moodboard's aesthetic average** — you're trying to push the moodboard toward something not represented in any of its images. Add 2–3 reference images that anchor the missing direction.
- **The candidate pool itself is biased** — if `04_production/assets/candidates/` skews toward one aesthetic family, the moodboard will too. Consider broadening the candidate pool before re-curating.

This is the "fresh evidence vs. context-aware evidence" distinction from `.claude/rules/LESSONS.md`: a moodboard inherits the bias of whatever was in the candidate pool when it was curated. Treat moodboards as **versioned artifacts**, not as eternal truths.
