---
date: 2026-05-11
status: draft-v1
version-target: Midjourney v7 (default May 2026)
spec-block: as of 2026-05
source-urls:
  - https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts
  - https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference
  - https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards
  - https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization
  - https://updates.midjourney.com/profiles-and-moodboards/
  - https://updates.midjourney.com/style-references-for-v7/
  - https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/
  - https://geekycuriosity.substack.com/p/midjourney-mixing-moodboard-style
  - https://geekycuriosity.substack.com/p/mastering-midjourney-moodboard
---

# 03 — Image Prompts, Style References, and Moodboards

This is the **most important doc for this project**. The reference workflow is: user manually curates `04_production/assets/candidates/` → handpicks subset → uploads to Midjourney **Moodboard** → generates. Understanding the three reference mechanisms is load-bearing.

## 3.1 Three reference mechanisms (don't conflate)

| Mechanism | Controls | Triggered by | Weight knob | Updateable? |
|---|---|---|---|---|
| **Image Prompt** | Content / composition / subject layout | URL **at the start** of prompt | `--iw 0–3` (default 1) | n/a (per-render) |
| **Style Reference (`--sref`)** | Aesthetic only (color, light, texture, medium) — no content copy | `--sref <url\|code>` | `--sw 0–1000` (default 100) | Code is fixed; URL upload averages on the fly |
| **Moodboard (`--p` / `--profile`)** | Averaged aesthetic from multiple curated images | `--p <code>` or `--profile <code>` | **None — silently ignored** | **Yes — add/remove images, snapshot code changes** |

> "Moodboards offer the best balance of control and flexibility. Unlike a static Sref code, you can update a moodboard." — [Chase Jarvis](https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/)

For this project: **moodboard is the right primary tool**, sref codes are a secondary lever for "I want this *exact* aesthetic, repeatable," image prompts are for "match this *composition*."

## 3.2 Image Prompt (URL at start of prompt)

### Syntax

```
https://reference.url/image.jpg [text prompt] --iw <weight> --style raw --v 7 --ar 4:5
```

> "Click the + icon next to prompt bar; drag image into 'Image Prompt' slot." — [Chase Jarvis](https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/) (V7 web app workflow)

### `--iw` behavior (V7)

> "The `--iw` value range for V7 and V6 is 0 to 3, while V5 is 0 to 2. The default `--iw` value is 1." ([Image Prompts](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts) via WebSearch snippet)

- `--iw 0.5` → text prompt dominates, image is loose inspiration.
- `--iw 1` → balanced.
- `--iw 2–3` → image strongly enforced (composition, color palette, form).

V7 is **more responsive** to small `--iw` changes than V6 — try 0.8 / 1.2 first.

### Caveat: image prompts bleed style

> "They also bleed style. If you upload a low-fi Polaroid as an image reference, Midjourney will likely degrade the quality." — [Chase Jarvis](https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/)

For this project, image prompts are the **wrong default** — when you want aesthetic transfer without composition copying, use moodboard or sref instead. Use image prompts only when you specifically need to lock composition (e.g., "same overhead flat-lay grid as this reference").

## 3.3 Style Reference (`--sref`)

### Two formats

**(a) URL upload**: `--sref https://reference.url/img.jpg`. Midjourney reads aesthetic from the image directly. Less consistent across runs (each render re-reads the URL).

**(b) Alphanumeric code**: `--sref 1344854894` (or any of the public sref code libraries — see [srefcodes.com](https://srefcodes.com/), [promptsref.com](https://promptsref.com/) for community-curated examples). Codes lock in a specific aesthetic, and the same code → same aesthetic every render.

> "Unlike uploading an image (which can be fuzzy), a code delivers the exact same aesthetic rendering every single time." — [Chase Jarvis](https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/)

### Multiple srefs and weights

```
--sref CODE_A::3 CODE_B::1 https://ref.url/img.jpg::1
```

`::` weight syntax works on srefs (unlike moodboards). Use to bias toward one aesthetic when blending.

### V7 sref version note

> "The Style Reference feature has been updated for V7 and old style codes may not produce the same styles anymore. To use old codes, add `--sv 4` to your prompt (uses the old V7 model) or switch to V6." ([Style References for V7 announcement](https://updates.midjourney.com/style-references-for-v7/) via WebSearch snippet)

If you find a great V6-era sref code, validate it under V7 before adopting; if it drifts, append `--sv 4`.

### Sref vs. moodboard, when to choose which

- **Sref** → "I want this *exact* lock-in aesthetic, indefinitely repeatable, never changes." Best when you've found a specific code that nails your brand look.
- **Moodboard** → "I have a curated set of references that together communicate the aesthetic; I may add more references later as the brand evolves." Best for this project, since the candidate pool grows over time.

## 3.4 Moodboard (`--p` / `--profile`) — primary path for this project

### What it is

> "Moodboards are a type of Midjourney personalization that lets you select specific images to create a unique style for your Midjourney projects. Moodboards help you express and communicate your vision across a wider aesthetic range, especially compared to Style References, which are more specific." ([Moodboards](https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards) via WebSearch snippet)

> "Moodboards take inspiration from the images that you add. As you add more diverse images to the board, the model will start to remix them in more complex ways." ([Profiles and Moodboards](https://updates.midjourney.com/profiles-and-moodboards/))

### How to create one (web app)

1. Go to **midjourney.com/personalize** (or click Moodboards in the main nav).
2. Click **New Moodboard** → name it.
3. Add images by:
   - Uploading from device,
   - Pasting image URLs,
   - Selecting from your Midjourney gallery.
4. Use the moodboard by appending `--p <m-id>` or `--profile <snapshot-code>` to the prompt, OR set it as the default moodboard via the Personalization button next to the Imagine bar.

### Two ID formats — important

| Form | Example | Persists across deletion? | Stable across moodboard edits? |
|---|---|---|---|
| `m...ID` | `--p m7360976358991724574` | **No** — invalidates on delete | Yes — same ID points to current state |
| Snapshot code | `--profile r1bwkpa` | **Yes** — code persists even after the moodboard is deleted | **No** — changes every time you add/remove an image |

Source: [Geeky Animals — Mastering Midjourney Moodboard](https://geekycuriosity.substack.com/p/mastering-midjourney-moodboard).

> "Add an image to your existing moodboard, and the snapshot code changes completely. … Removing that same image reverts the code to its previous state, suggesting the system maintains historical versions." (same source)

**Implication for this project's audit trail**: always record the snapshot code **at the time of generation**. Don't only save the human-readable moodboard name — that won't reproduce the exact aesthetic if the moodboard is later edited.

### How many images? (heuristic)

> "Group 5–10 images to create a custom, nuanced aesthetic averaged across all inputs." — [Chase Jarvis](https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/)

> "You'll need 40 ratings to get started, and the profile should be fairly stable by 200." — [Profiles and Moodboards](https://updates.midjourney.com/profiles-and-moodboards/) (this is the personalization-rating threshold; moodboards inherit personalization but don't have an analogous official "image count" rule.)

> ⚠️ 推測: 5–10 is a heuristic floor from a credible secondary source ([Chase Jarvis](https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/)) but is **not** in the official docs I could verify from this sandbox. Treat as a starting heuristic; scale up to 12–20 if outputs look chaotic, scale down to 4–6 if outputs look too narrow.

For this project's lanes:
- **Editorial** (mixed mood, mixed light): 10–15 images for variety.
- **Fashion** (single brand language): 8–12 tightly curated.
- **Surface / material** (texture studies): 6–10 with consistent lighting.
- **Object still-life** (consistent set design): 6–10 with consistent camera/scale cue.

### No weighting on moodboards

> "The Moodboard, unlike Sref, does not currently support weightage. The bot will ignore code weight and the duplicated codes." — [Geeky Animals — Mixing Moodboard, Style, Reference, and Personalization](https://geekycuriosity.substack.com/p/midjourney-mixing-moodboard-style)

You **cannot** write `--p code1::3 code2::1`. The `::3` and `::1` are silently dropped, and duplicate codes are deduped.

**Workaround**: if you need one aesthetic to dominate, do one of:

1. Use a single moodboard, drop in **more copies of the dominant aesthetic's images** (since averaging is by image, more dominant-aesthetic images = stronger average toward that aesthetic).
2. Combine moodboard + sref code, use `--sw` to balance (`--sw 50` reduces sref influence relative to moodboard).
3. Tune via prompt language: front-load the dominant aesthetic's adjectives, push secondary into `--no` if applicable.

### Mixing moodboard with other refs

> "You can combine two Srefs, two Moodboards, and two Personalization codes at once!" — [Geeky Animals — Mixing](https://geekycuriosity.substack.com/p/midjourney-mixing-moodboard-style)

```
[text prompt] --profile MOOD_A MOOD_B --sref CODE_A CODE_B --v 7 --style raw --ar 4:5
```

Useful pattern for this project: **black-and-white illustration moodboard + colorful sref code** to add color to a monochromatic averaged aesthetic. Pattern attributed to same source.

### Moodboard compatibility

> "Moodboards are compatible with Midjourney versions 6 and 7, but cannot be used with Style Reference Version (`--sv`) or Style Weight (`--sw`)." ([Moodboards](https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards) via WebSearch snippet)

→ While a moodboard is active, you **cannot** tune sref via `--sw` and you **cannot** select a legacy sref version via `--sv`.

### Personalization on/off

V7 turns Personalization on by default and **requires the user to unlock it** by ranking ~40 image pairs ([V7 Alpha](https://updates.midjourney.com/v7-alpha/)). The trained personalization profile then biases every prompt unless toggled off via the Personalization button.

**For this project, the safer setup is**:

1. Either set the moodboard as the *default* personalization (so the bias is the moodboard, not an unrelated trained profile),
2. OR toggle Personalization off entirely and use `--p <code>` explicitly per prompt to keep aesthetic source 100% transparent.

> ⚠️ 推測: I could not directly verify the precise interaction between the V7-default personalized profile and an explicitly-attached `--p <moodboard>` code from this sandbox. The safer assumption is **the two stack** (default profile applies + moodboard adds), so for fully attributable output, set the moodboard as default OR turn off the trained profile.

## 3.5 Decision flow for this project

```
Have curated reference images?
├─ Yes → Need composition copy?
│   ├─ Yes → Image prompt (URL + --iw 1.5–2)
│   └─ No  → Need exact, locked aesthetic?
│       ├─ Yes (and aesthetic is rare/specific) → --sref CODE (community library)
│       └─ No  → Moodboard (--p / --profile)  ← THIS PROJECT'S DEFAULT
└─ No → Pure text prompt with --style raw + --v 7
```
