---
name: mj-seed-styletuner-cross-subject
description: MJ --seed does NOT carry style across subjects (only composition/noise-layout); Style Tuner (--style code) is LEGACY/--v5.2-only; V8 successor is Style Creator (makes --sref codes)
metadata:
  type: reference
---

Web-verified 2026-06-26 via docs.midjourney.com snippets (Seeds, Legacy Features/style-tuner, Style Creator, Personalization, Stylize, Raw). docs.midjourney 403s on direct WebFetch — quotes are from search snippets of the official pages. See [[mj-stylize-chaos-hd-params]], [[mj-style-raw]], [[mj-moodboard-vs-sref]].

**--seed: range 0–4294967295, default random.** NOT a style-consistency lever across subjects. Official Seeds doc verbatim: "Seeds can't capture or bookmark a specific style, character, or appearance across different prompts. They only influence the initial layout of noise that begins the rendering process." Same seed + SAME prompt = "siblings, not twins" (similar composition, details differ); "99% identical in V8.1." Same seed + DIFFERENT prompt = preserves COMPOSITION/layout/perspective only (panda→fox keeps pose+background), NOT style. So for "keep style constant, change ONLY subject" the answer is NO — seed is the wrong tool (use --sref / --p personalization / moodboard for style; seed only locks the noise field so it's a within-prompt experimental control). Don't use Turbo mode with seeds (unreliable lock).

**Style Tuner / --style <code>: LEGACY.** Official "Legacy Features" page (docs/style-tuner now redirects there): "/tune command no longer works, and new Style Tuners cannot be created. However ... existing --style code parameters can still be used." CRITICAL: the codes are "limited to --v 5.2" — so a --style numeric code is USELESS on V8.1. Style Tuner was a v5.2 Discord feature, a precursor to Personalization/Moodboards/Style Explorer. Do NOT recommend --style <code> for this V8.1 project.

**--style raw is DIFFERENT and current** (the only live --style value on V8.x): reduces MJ's automatic beautification, "less automatic beautification applied," more literal to the prompt. Compatible v5.1+. (See [[mj-style-raw]] for the realism-kernel usage.)

**V8 successor to Style Tuner = "Style Creator"** (docs Style Creator page, midjourney.com only): pick/reject from an image grid → produces a reusable **--sref style-reference CODE** (NOT a --style code). This + Personalization (--p, compatible v6/7/8.1) are the real cross-subject style-consistency tools for V8.1, alongside image-URL --sref.

**--stylize / --s: internal aesthetic INTENSITY, not external transfer.** Official Stylize framing: adjusts "how strongly Midjourney's default aesthetic style, which favors artistic color, composition, and forms, is applied." Range 0–1000, default 100 (Low 50 / Med 100 / High 250 / Very High 750). Low=literal-to-prompt, high=MJ's own artistic embellishment (strays from prompt). It transfers NO external/specific style — it only dials MJ's OWN look. (Cross-ref: high --s COMPETES with --sref, see [[mj-stylize-chaos-hd-params]].)
