---
name: mj-lock-style-vary-subject-workflow
description: Canonical MJ "lock style, vary subject" workflows (V7/V8.1, 2025-2026) — sref vs --p personalization vs moodboard vs seed; what experienced artists actually combine
metadata:
  type: reference
---

Web-verified 2026-06-26. See [[mj-moodboard-vs-sref]], [[mj-sref-image-url-behavior]], [[mj-sv-style-reference-version]], [[web-access-constraints]]. docs.midjourney 403s on WebFetch — official wording read via WebSearch verbatim snippets.

**The four mechanisms and what each officially does:**
- `--sref <image URL or code>` = STYLE-ONLY transfer (color/medium/texture/lighting, NOT subject/composition). Official: "doesn't copy objects or people... helping you achieve a consistent visual theme." Pin across prompts via the LOCK ICON in the Imagine bar (official). `--sw` 0–1000 def 100 controls strength. The targeted, project-scoped tool.
- `--p <pID>` Personalization = AMBIENT learned-style profile from ~200 pair-rankings/likes; applies to ALL your prompts when toggled on (or per-prompt with `--p`). Official (updates.midjourney): "not a stable feature right now, it will change as you do more pair ratings." Strength via `--s` (stylize) NOT --sw. "ambient fingerprint" / baseline.
- Moodboard = a personalization profile built from MANY curated images, referenced `--p mID` (m-prefix). `--sw` is SILENTLY IGNORED with moodboards; strength via `--s`. Generalizes a palette across N images (robust to subject variation) but no weight control.
- `--seed` = layout/noise only. **Official Seeds doc explicitly: "Seeds can't capture or bookmark a specific style, character, or appearance across different prompts... For consistency in your images, we recommend style references, omni references, and personalization."** So fixed-seed is NOT a style-lock mechanism — it locks composition within a session, fights other params, unreliable across sessions.

**What experienced artists actually combine (the real answer to the focus question) — THREE archetypes, all valid:**
1. SOLO sref-image archetype (most common in guides): single "hero" image as `--sref URL`, reused/pinned across every prompt; text prompt varies the subject; tune `--sw` (default 100; QWE band 65–175, images 150–200 if weak / 50–70 if strong). NO seed, NO --p. (titanxt, atypicalco, sider, TheDevDesigns base.)
2. STACKED text-block + seed + sref (TheDevDesigns "style scaffold"): reusable text template `{subject}, cinematic {lighting}, {texture}, shot on {lens}, {backdrop}... --seed X --ar 4:5 --sref {hero URL}` — combines (a)+(c)+(d). NOTE: the seed here only stabilizes composition/grain within a set, contradicting official "seed ≠ style"; treat seed as optional/weak.
3. PRO layered archetype (Jamey Gannon / ChatPRD, blakecrosley, PromptDervish): Pinterest moodboard → pick individual images as `--sref` → ALSO train a `--p` personalization code ("late 2025 aesthetic") → stack `--p` (ambient baseline) + `--sref` (project mood) in one prompt; deliver sref+--p codes + base prompts as a kit. Official: `--sref` and `--p` CAN be combined in one prompt (space-separated); blend multiple of each, weight srefs with `::n`.

**Key reconciliation / consensus:** the dominant recommendation = `--p` as the always-on AMBIENT baseline + a fixed `--sref` (image or code) for the SPECIFIC project look, prompt varies subject. Start with ONE sref, add a 2nd only for a known missing element (stacking 3 at --sw 800 does NOT blend — QWE). Avoid relying on seed for STYLE. Don't over-stack competing signals (--style + --sref + --p + high stylize fight each other — start simple).

**V8 Style Creator / Style Tuner (`/tune`)** = newer route: rate 16–128 image pairs → outputs a reusable `--sref`-style code generated from scratch (vs sref which borrows from existing imagery). Portable/shareable. (mindstudio.)

**sref version gotcha (carry from [[mj-sv-style-reference-version]]):** MJ rewrote the sref system 2025-06-16; pre-that-date codes need `--sv 4` for legacy results. Default is sv7 on V8.1.
