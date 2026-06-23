---
date: 2026-05-11
status: draft-v1
version-target: Midjourney v6.1 (legacy default) and v7 (current default as of May 2026)
v8-note: V8 alpha rolled out 2026-03-17; V8.1 alpha rolled out 2026-04-30; V7 remains default model as of 2026-05-11
source-urls:
  - https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics
  - https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List
  - https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards
  - https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference
  - https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts
  - https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference
  - https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference
  - https://docs.midjourney.com/hc/en-us/articles/32173351982093-No
  - https://docs.midjourney.com/hc/en-us/articles/32099348346765-Chaos-Variety
  - https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw-Mode
  - https://docs.midjourney.com/hc/en-us/articles/32196176868109-Stylize
  - https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version
  - https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization
  - https://docs.midjourney.com/hc/en-us/articles/32658968492557-Multi-Prompts-Weights
  - https://docs.midjourney.com/hc/en-us/articles/32761322355597-Permutations
  - https://docs.midjourney.com/hc/en-us/articles/35577175650957-Draft-Conversational-Modes
  - https://updates.midjourney.com/v7-alpha/
  - https://updates.midjourney.com/profiles-and-moodboards/
  - https://updates.midjourney.com/style-references-for-v7/
  - https://updates.midjourney.com/omni-reference-oref/
  - https://updates.midjourney.com/character-refs/
  - https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/
  - https://medium.com/creativity-ai/midjourney-how-to-use-moodboard-35c20a0e9266
  - https://geekycuriosity.substack.com/p/midjourney-mixing-moodboard-style
sandbox-note: docs.midjourney.com returned 403 from this sandbox; spec values are extracted via WebSearch result snippets that quote the official pages, plus fetched secondary sources. Where a number is purely from a secondary source, it is flagged in the relevant doc.
---

> **⚠️ ARCHIVED (V7-era).** Superseded by `../2026-06-21_midjourney-v8.1-current.md` for all current
> parameter behavior. Kept for history + sourcing. Do not use its V7 spec values as current.

# Midjourney Prompt Best Practices — Index

Project: `@softslowedit` Instagram. Reference image generation for editorial / fashion / surface (texture, material) / object still-life. Reference workflow: user manually curates `04_production/assets/candidates/` → handpicks subset → uploads to Midjourney **Moodboard** → generates with prompt.

## File Index

| File | Purpose |
|---|---|
| [01_prompt-anatomy.md](./01_prompt-anatomy.md) | Prompt structure, subject / medium / environment / lighting / color / mood, where parameters go, token economy. |
| [02_parameters-reference.md](./02_parameters-reference.md) | Parameter table: `--ar`, `--s`, `--c`, `--weird`, `--no`, `--raw`, `--v`, `--niji`, `--iw`, `--sw`, `--sv`, `--cw`, `--ow`, `--p`, `--profile`, `--sref`, `--cref`, `--oref`, `::` weights, `{}` permutations, `--seed`, `--stop`, `--q`, `--tile`. |
| [03_image-prompts-and-moodboard.md](./03_image-prompts-and-moodboard.md) | Image prompt URL vs. Style Reference (`--sref`) vs. Moodboard (`--p` / `--profile`); moodboard creation, mixing, no-weight limitation; this project's recommended path. |
| [04_examples-and-patterns.md](./04_examples-and-patterns.md) | Concrete prompt templates for editorial / fashion / surface-material / object-still-life with this project's moodboard-first workflow. |
| [05_pitfalls-and-tips.md](./05_pitfalls-and-tips.md) | Token budget (74-token cap, ~40-word influence drop-off), `--no` parsing trap, weight collisions, over-styling, AI-generated giveaways, version drift. |

---

## TL;DR (this project's takeaways)

1. **V7 is the default model as of May 2026**; V8 alpha exists (2026-03-17 V8.0, 2026-04-30 V8.1) but is not default yet. Pin every prompt with `--v 7` (or `--v 6.1` for fallback) so renders don't silently drift when V8 becomes default. ([Midjourney Version docs](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version), [Releasebot v8 timeline](https://releasebot.io/updates/midjourney))

2. **V7 requires unlocking Personalization before first use** (~5 min ranking exercise) and Personalization is **on by default**. This means even a "neutral" prompt is biased toward your trained taste — for editorial reference work where you want fidelity to the moodboard, **toggle Personalization off OR set the moodboard as your default profile** so the bias is the moodboard, not an unrelated trained style. ([V7 alpha announcement](https://updates.midjourney.com/v7-alpha/))

3. **Moodboard (`--p mID` or `--profile <code>`) is the right tool for this project** — it's literally "upload your curated reference set, the model averages the aesthetic." Fits the manual-curation pipeline directly. ([Moodboards docs](https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards), [Profiles and Moodboards announcement](https://updates.midjourney.com/profiles-and-moodboards/))

4. **Moodboard does NOT support per-code weighting** — `--p code1::3 code2::1` is silently ignored. If you need weighting, use `--sref code::weight` or split into two moodboards and tune via prompt language. ([Geeky Animals — Mixing Moodboard, Style, Reference, and Personalization](https://geekycuriosity.substack.com/p/midjourney-mixing-moodboard-style))

5. **Moodboard ≠ Style Reference ≠ Image Prompt** — three different tools:
   - **Image prompt** (URL at start of prompt, `--iw 0–3`): copies content/composition; **bleeds style** (low-fi reference → low-fi output).
   - **`--sref`**: aesthetic only, no content copy; supports `--sw` weight.
   - **Moodboard `--p`**: averaged aesthetic across multiple images, updateable, no weight knob.
   For "I curated 8 references and want the *vibe*" → moodboard. For "I want this *exact* color/lighting/grading" → sref code. For "match this *composition*" → image prompt with low `--iw`. ([Chase Jarvis breakdown](https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/))

6. **Moodboard rating threshold for stability**: official guidance is "**40 ratings to get started, ... fairly stable by 200**" for personalization profiles — moodboards inherit similar averaging behavior. Plan to seed a moodboard with **at least 5–10 curated images** before relying on it for production. ([Profiles and Moodboards](https://updates.midjourney.com/profiles-and-moodboards/), [Chase Jarvis: 5–10 images](https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/))

7. **`--style raw` for editorial / fashion / surface / product** — removes Midjourney's default painterly bias, gives more literal photographic output. Pairs well with moodboard for "this aesthetic, but as a believable photograph." ([Raw Mode](https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw-Mode))

8. **Token economy: 74-token hard cap**, words after ~40 lose influence. Front-load subject + critical aesthetic words; push descriptors to the moodboard side. ([Aituts /shorten guide](https://aituts.com/midjourney-shorten/), Midlibrary v6 in-depth review)

9. **`--no` is per-comma-list, not per-flag** — `--no shadows, color, gradients`, NOT `--no shadows --no color`. Each word is parsed independently, so `--no modern clothing` reads as "no modern" + "no clothing" (can trigger moderation). ([No docs via WebSearch quote](https://docs.midjourney.com/hc/en-us/articles/32173351982093-No))

10. **`--cref` is incompatible with V7**; use `--oref` (Omni Reference) for V7 character/object identity. Costs **2x GPU**. ([Omni Reference docs](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference), [Omni Reference announcement](https://updates.midjourney.com/omni-reference-oref/))

---

## Carry-forward (minimum 3 steps to integrate this into the project workflow)

1. **Set up at least one production moodboard per lane** (editorial / fashion / surface / object still-life), each seeded with 8–12 curated images from `04_production/assets/candidates/`. Save the moodboard `--profile` snapshot code (the alphanumeric, NOT the `m...ID` form, because `m...ID` invalidates on deletion per [Geeky Animals — Mastering Moodboard](https://geekycuriosity.substack.com/p/mastering-midjourney-moodboard)).

2. **Lock a base prompt template per lane** in `03_masters/prompts/midjourney.md` (new file, mirroring existing `krea.md` / `nano-banana-pro.md`): subject phrase + camera/lens cue + lighting cue + `--style raw --v 7 --ar X:Y --profile <code>`. Token budget ≤ 40 words.

3. **Define a moodboard-update protocol** — when adding/removing reference images, the snapshot code changes ([Geeky Animals](https://geekycuriosity.substack.com/p/mastering-midjourney-moodboard)). Record the snapshot code + moodboard contents (file list) at the time of each generation run, so future audits can attribute outputs to a specific moodboard state.

---

## Constraints / unverified items

- **`docs.midjourney.com` returned HTTP 403** from this sandbox; primary spec values are extracted from WebSearch result snippets that quote the official pages directly (Anthropic web search backend has the docs cached and quotes them in result text). Where a value comes from a secondary source only, it is flagged in the relevant doc as `> ⚠️ 推測:`.
- **`--p` vs `--profile`**: both are documented as valid for moodboards/personalization, but the latest `m...` ID format vs. snapshot alphanumeric form has subtle persistence differences (snapshot persists across moodboard deletion, `m...ID` does not). This was confirmed in [Geeky Animals — Mastering Midjourney Moodboard](https://geekycuriosity.substack.com/p/mastering-midjourney-moodboard); not directly verified in official docs from this sandbox.
- **Moodboard image count "5–10"** comes from [Chase Jarvis](https://chasejarvis.com/blog/how-to-control-midjourney-style-references-image-references-and-moodboards/), not official docs. Official docs only specify the personalization profile's "40 ratings to start, 200 to stabilize" threshold; moodboards explicitly inherit personalization. Treat 5–10 as a heuristic floor, scale up if averaging looks chaotic.
- **V8 / V8.1 alpha specifics**: only flagged at high level (release dates, "not default yet"). All v7-specific spec values may not carry forward to V8 — re-verify before V8 becomes default.
