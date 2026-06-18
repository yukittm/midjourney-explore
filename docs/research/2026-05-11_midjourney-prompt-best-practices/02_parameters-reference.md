---
date: 2026-05-11
status: draft-v1
version-target: Midjourney v7 (default May 2026), v6.1 fallback, niji 6 noted
spec-block: as of 2026-05
source-urls:
  - https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List
  - https://docs.midjourney.com/hc/en-us/articles/32099348346765-Chaos-Variety
  - https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw-Mode
  - https://docs.midjourney.com/hc/en-us/articles/32196176868109-Stylize
  - https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version
  - https://docs.midjourney.com/hc/en-us/articles/32173351982093-No
  - https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference
  - https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference
  - https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts
  - https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference
  - https://docs.midjourney.com/hc/en-us/articles/32658968492557-Multi-Prompts-Weights
  - https://docs.midjourney.com/hc/en-us/articles/32761322355597-Permutations
  - https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards
  - https://updates.midjourney.com/omni-reference-oref/
  - https://updates.midjourney.com/style-references-for-v7/
---

# 02 — Parameters Reference

> All values **as of 2026-05**, V7 default. Re-verify when V8 becomes default. `docs.midjourney.com` was unreachable from this sandbox (403); spec values below are from WebSearch result snippets quoting the official pages, plus the secondary sources cited.

## 2.1 Quick parameter table

| Flag | Range / values | Default | Versions | Purpose |
|---|---|---|---|---|
| `--ar W:H` (`--aspect`) | any ratio | 1:1 | all | image dimensions |
| `--v N` (`--version`) | 1–7 | 7 (May 2026) | all | model version |
| `--niji N` | 5, 6 | — | niji track | anime-tuned model |
| `--style <name>` | `raw`, `cute`, `scenic`, `expressive`, `original` | none | V6/V6.1/V7 (raw); niji track (cute/scenic/expressive/original) | preset styling adjustment |
| `--s N` (`--stylize`) | 0–1000 | 100 | V4+ | strength of MJ's default style |
| `--c N` (`--chaos`) | 0–100 | 0 | all | variety across the 4-image grid |
| `--weird N` | 0–3000 | 0 | V5+ | surreal/unconventional bias |
| `--no <a, b, c>` | comma list | — | all | negative prompt; one flag, comma-separated terms |
| `--q N` (`--quality`) | 0.25–2 | 1 | all | render time/quality multiplier |
| `--seed N` | int | random | all | reproducibility |
| `--stop N` | 10–100 | 100 | all | early-stop denoising at N% |
| `--tile` | flag | off | all | seamlessly tileable output |
| `--iw N` | 0–3 (V6/V7), 0–2 (V5) | 1 | V5+ | image-prompt weight (URL at start of prompt) |
| `--sref <url\|code>` | URL or alphanumeric code | — | V6/V6.1/V7 | style reference (aesthetic only) |
| `--sw N` (`--style-weight`) | 0–1000 | 100 | V6/V6.1/V7 | strength of `--sref` influence |
| `--sv N` (`--style-version`) | 1–4 (V7 supports legacy via `--sv 4`) | latest | V7 | sref version selector |
| `--cref <url>` | URL | — | V6 only | character reference (V7 incompatible — use `--oref`) |
| `--cw N` (`--character-weight`) | 0–100 | 100 | V6 only | 100=strong adherence, 0=face-only |
| `--oref <url>` (`--omni-reference`) | one URL | — | V7 only | unified character/object identity reference |
| `--ow N` (`--omni-weight`) | 1–1000 | 100 | V7 only | strength of `--oref`; keep <400 unless `--s` is very high |
| `--p [code]` (`--profile [code]`) | alphanumeric code or empty (uses default) | — | V6/V6.1/V7 | personalization / moodboard reference |
| `::N` | int or decimal | — | all | multi-prompt weight separator (no space before `::`, single space after) |
| `{a, b, c}` | curly brace list | — | all | permutation expansion (Pro plan for batch) |
| `--draft` (web button) | flag | off | V7 web app | half-cost, ~10x faster preview |

Sources for each row: `--ar`/`--s`/`--c` ([Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List)); `--c` range 0–100 ([Chaos / Variety](https://docs.midjourney.com/hc/en-us/articles/32099348346765-Chaos-Variety)); `--weird` 0–3000 (Medium "weird vs chaos vs stylize" via [WebSearch snippet](https://medium.com/ai-art-creators/whats-the-difference-between-weird-chaos-and-stylize-in-midjourney-d7e16cab2420)); `--style raw` ([Raw Mode](https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw-Mode)); `--no` ([No](https://docs.midjourney.com/hc/en-us/articles/32173351982093-No)); `--sref`/`--sw` ([Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference), [Style References for V7 announcement](https://updates.midjourney.com/style-references-for-v7/)); `--cref`/`--cw` ([Character Reference](https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference)); `--oref`/`--ow` ([Omni Reference docs](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference), [Omni Reference announcement](https://updates.midjourney.com/omni-reference-oref/)); `--iw` ([Image Prompts](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts)); `::` ([Multi-Prompts & Weights](https://docs.midjourney.com/hc/en-us/articles/32658968492557-Multi-Prompts-Weights)); `{}` ([Permutations](https://docs.midjourney.com/hc/en-us/articles/32761322355597-Permutations)); `--p` ([Moodboards](https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards)).

---

## 2.2 Behavior detail per parameter

### `--ar` Aspect Ratio

> "Sets the image's width-to-height ratio (e.g., `--ar 16:9` for widescreen, `--ar 2:3` for a portrait)." ([Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List))

For Instagram feed/carousel: `--ar 4:5` (portrait) or `--ar 1:1` (square). For story/reel covers: `--ar 9:16`.

### `--v` / `--niji`

V7 is the **default model as of May 2026**. ([Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version))

V8 alpha (2026-03-17) and V8.1 alpha (2026-04-30) exist but are **not the default** ([Releasebot Midjourney updates](https://releasebot.io/updates/midjourney)). Always specify `--v 7` (or `--v 6.1`) explicitly so output doesn't drift when V8 becomes default.

V6.1 was the previous default (2024-07-30 → 2025-06-16). It generates ~25% faster than V6, with better coherence and an updated personalization model ([Version 6.1 announcement](https://updates.midjourney.com/version-6-1/) via WebSearch quoted snippet).

`--niji 6` is the anime model, separate track. Same prompt grammar, different aesthetic prior. Niji-only style flags: `--style cute`, `--style scenic`, `--style expressive`, `--style original`. To suppress the anime look in niji, use `--style raw`. ([Welcome to Niji V6](https://nijijourney.com/blog/niji-updates-welcome-to-niji-v6) via WebSearch snippet)

### `--style raw`

> "In Standard Mode, Midjourney automatically adds its own creative touch to your images. When you switch to Raw Mode, you're essentially turning off this 'auto-pilot.' With simple prompts, you'll often get more realistic, photo-like images." — [Raw Mode](https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw-Mode) (via WebSearch snippet)

For this project (editorial / fashion / surface / object still-life), **`--style raw` is the default for production prompts**. The painterly default makes editorial photography look stylized in a generic-AI way.

### `--s` / `--stylize`

> "Stylize ranges from 0 for literal to 1000 for painterly." ([Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List))

Default 100. For editorial photo work, **try `--s 50–150`**; for surface/material studies that need texture realism, lower (50–100); for stylized fashion campaigns, 200–400.

### `--c` / `--chaos`

> "Chaos lets you add more variety to the image results you get from each prompt. You can set the chaos value anywhere between 0 and 100, but keep in mind that higher values mean the images can be quite different and may not stick as closely to your prompt." ([Chaos / Variety](https://docs.midjourney.com/hc/en-us/articles/32099348346765-Chaos-Variety))

Default 0 (the 4 grid images are very similar). For exploration runs (early in a moodboard's life), use `--c 20–40`. Keep at 0 for production.

### `--weird`

> "Weird provides surreal deviation from expected output, with values from 0–3000." (via WebSearch snippet, [Medium "weird vs chaos vs stylize"](https://medium.com/ai-art-creators/whats-the-difference-between-weird-chaos-and-stylize-in-midjourney-d7e16cab2420))

For editorial / surface / product, **leave at 0**. Useful only for art-direction explorations.

### `--no`

> "Add `--no` to the end of your prompt, followed by the thing or list of things you don't want in your image. … Using the no parameter is the same as using a -0.5 weight." ([No](https://docs.midjourney.com/hc/en-us/articles/32173351982093-No))

**Critical syntax rule**: one flag, comma-separated. `--no shadows, color, gradients` ✅. `--no shadows --no color` ❌ ("You cannot include multiple `--no` commands"). Each word is parsed independently — `--no modern clothing` reads as "no modern" + "no clothing" (moderation trigger). Quote and detail in [05_pitfalls-and-tips.md](./05_pitfalls-and-tips.md).

### `--iw` Image Weight (image prompt)

> "The `--iw` value range for V7 and V6 is 0 to 3, while V5 is 0 to 2. The default `--iw` value is 1." ([Image Prompts](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts))

Decimal accepted (`--iw 0.5`, `--iw 0.01`). V7 is **more responsive** than V6 — small changes cause larger stylistic shifts; prefer 0.8 / 1.2 over 0.5 / 1.5 for fine-tuning.

### `--sref` Style Reference

> "Sref doesn't copy the actual objects or subjects. Instead, it captures the overall mood, including colors, textures, lighting, and medium." (via WebSearch snippet, official Style Reference docs)

Two formats:
1. **URL upload**: `--sref https://...`. Aesthetic averaged from the image. Less consistent.
2. **Alphanumeric code**: `--sref 1344854894`. Repeatable; same code → same aesthetic every time.

Multiple sref values: space-separated. Per-sref weighting: `--sref CODE_A::5 CODE_B::2 https://...::1`.

V7 has its own sref version. **Old V6-era codes don't render the same in V7** — to use legacy behavior, append `--sv 4` ([Style References for V7](https://updates.midjourney.com/style-references-for-v7/) via WebSearch snippet) OR fall back to `--v 6.1`.

### `--sw` Style Weight

0–1000, default 100. Higher = sref dominates the output. Use to balance against text prompt or against an image prompt.

### `--cref` / `--cw` (V6 only)

> "When using V7, use Omni Reference instead. As of 2026, the standard Character Reference (`--cref`) is incompatible with Midjourney Version 7." (via WebSearch snippet)

`--cw` 0–100; default 100 (strong adherence). 0 = face only.

For this project, character consistency is **not** the primary need (we're generating reference imagery, not narrative scenes with recurring characters). Skip unless a specific story slot needs identity.

### `--oref` / `--ow` Omni Reference (V7)

> "Omni Reference allows you to put a person or object into your images, and it can only be used with Midjourney version 7. … `--ow` allows you to control how much detail from your reference image appears in your new image. You can set this parameter to any value between 1 and 1,000, with the default being `--ow 100`. Unless you are using a very high stylize value, it's best to keep your weight below 400, otherwise your results may be unpredictable. … Using Omni Reference will cost 2x more GPU time compared to regular V7 images." ([Omni Reference](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference), [Omni Reference announcement](https://updates.midjourney.com/omni-reference-oref/) via WebSearch snippet)

Constraints:
- One image only (single `--oref <url>`).
- Requires a text prompt.
- Not compatible with Vary Region, Pan, Zoom Out, inpainting, outpainting (those still use V6.1).

### `--p` / `--profile` Personalization & Moodboard

> "To use a specific moodboard, copy its ID from your Moodboards Page with the use icon and add it to the end of your prompt (example: `--p mID`). You can also add `--p` to the end of your prompt in the Imagine bar to apply your default moodboard to your prompt." ([Moodboards](https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards) via WebSearch snippet)

Two ID formats:
- **`m...` ID** (e.g., `--p m7360976358991724574`): points to the moodboard collection. **Invalidates if you delete the moodboard.**
- **Snapshot code** (e.g., `--profile r1bwkpa`): permanent alphanumeric. **Persists even after deletion**, but the snapshot code itself **changes every time you add/remove an image** from the moodboard. ([Geeky Animals — Mastering Midjourney Moodboard](https://geekycuriosity.substack.com/p/mastering-midjourney-moodboard))

Multiple moodboards/personalizations:
> "You can combine two Srefs, two Moodboards, and two Personalization codes at once!" Example: `--profile b6zubim ymzqaj9 oamxod7 rg1aj89 --sref 1344854894 3505500910` ([Geeky Animals — Mixing](https://geekycuriosity.substack.com/p/midjourney-mixing-moodboard-style))

**No weighting on moodboards**: "The Moodboard, unlike Sref, does not currently support weightage. The bot will ignore code weight and the duplicated codes." Same source.

**Compatibility**:
> "Moodboards are compatible with Midjourney versions 6 and 7, but cannot be used with Style Reference Version (`--sv`) or Style Weight (`--sw`)." ([Moodboards](https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards) via WebSearch snippet)

→ If you mix moodboard + sref, you cannot tune the sref via `--sw` while moodboard is active.

### `::` Multi-prompt weights

> "Add a double colon `::` after each section of your prompt you want to separate. There should be no space on the left side of your double colon, and a single space on the right side." ([Multi-Prompts & Weights](https://docs.midjourney.com/hc/en-us/articles/32658968492557-Multi-Prompts-Weights) via WebSearch snippet)

`space::2 ship` = "space" weighted 2×, "ship" weighted 1× (implicit). Negative weights work (`hot air balloon::-0.5`) **as long as the total of all weights is positive**.

### `{a, b, c}` Permutations

> "A `{red, green} bird in the {jungle, desert}` will produce four prompts. … Permutations can also be applied to the weights of multiprompt segments, … `--ar {1:1, 2:3, 3:5}`." ([Permutations](https://docs.midjourney.com/hc/en-us/articles/32761322355597-Permutations) via WebSearch snippet)

Pro plan or Mega plan (and Fast Mode) required for batch permutations on Discord.

### `--seed`, `--stop`, `--q`, `--tile`

- `--seed N`: integer. Same seed + same prompt + same model = identical output (within stochastic noise tolerances). Use for A/B-ing one variable.
- `--stop N` (10–100): truncates denoising at N%. `--stop 50` produces softer, less detailed images. Useful for moodboard-style early-output exploration.
- `--q 0.25 / 0.5 / 1 / 2`: render-time multiplier; `--q 2` for sharp final art. ([Raw Mode discussion via WebSearch snippet](https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw-Mode))
- `--tile`: produces seamlessly tileable patterns. Useful for surface/texture work where the output will be used as a repeat pattern.

### `--draft` (V7 web only)

V7 introduced **Draft Mode**: "half the cost and renders images at 10 times the speed" ([V7 Alpha](https://updates.midjourney.com/v7-alpha/) via WebSearch snippet). Draft images are lower fidelity but consistent enough for ideation. Draft Mode also enables **Conversational Mode** ("swap out a cat with an owl") and **Voice Mode** on the web app. ([Draft & Conversational Modes](https://docs.midjourney.com/hc/en-us/articles/35577175650957-Draft-Conversational-Modes))

For this project: use Draft Mode for moodboard exploration (fast iteration on prompt phrasing), then switch to standard mode + `--q 2` for the final output.

---

## 2.3 Compatibility matrix (quick reference)

| Feature combo | Works? | Notes |
|---|---|---|
| `--p` (moodboard) + `--sref` | Yes | But `--sw` and `--sv` are blocked while moodboard is active. |
| `--p` + `--style raw` | Yes | Recommended for editorial/photo work. |
| `--p` + `--niji 6` | Yes (V6 line) | Personalization compatible with V6. ([Personalization](https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization) via WebSearch snippet) |
| `--cref` + V7 | **No** | Use `--oref` in V7. |
| `--oref` + V6/V6.1 | **No** | V7 only. |
| `--oref` + Vary Region / Pan / Zoom | **No** | Those operations still use V6.1. |
| `--tile` + `--ar non-1:1` | Yes | But seamless tiling assumes square symmetry — most reliable at `--ar 1:1`. |
| `--sref code1::3 code2::1` | Yes | Per-sref weighting supported. |
| `--p code1::3 code2::1` | **No** | Moodboard ignores per-code weight. |
