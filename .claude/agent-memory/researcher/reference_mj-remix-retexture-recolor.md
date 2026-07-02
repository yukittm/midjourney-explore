---
name: mj-remix-retexture-recolor
description: MJ V8.1 Remix Subtle/Strong semantics, what carries into the remix bar, and Retexture vs Remix for recoloring while keeping composition
metadata:
  type: reference
---

Web-verified 2026-07-02 via docs.midjourney.com search snippets (Remix 32799074515213, Modifying-Your-Creations 33329329805581, Editor 32764383466893, Style-Reference 32180011136653), geekycuriosity, titanxt, aiarty. docs.midjourney.com still 403s on direct WebFetch — read via WebSearch snippets. See [[mj-sref-image-url-behavior]], [[mj-sv-style-reference-version]], [[web-access-constraints]].

**Remix mechanics (official Remix doc):** Remix re-runs your ORIGINAL prompt + source image as the anchor; it does NOT attach a fresh new image-prompt under the hood — it re-imagines the whole job with the source as visual foundation. Subtle = minor adjustments, maintains overall style + LAYOUT, changes details. Strong = "creative reset": bigger changes to layout/pose/composition/arrangement while keeping the theme. Same Subtle/Strong behavior as Variations. Both keep original structure/layout as the base (Subtle much more tightly).

**What carries into the remix bar:** After clicking Remix, "your original prompt and image automatically populate in your Imagine bar with the Remix label." So the ORIGINAL text + image-prompt URL(s) + `--sref` + params all repopulate and are editable — you can edit or delete any of them before submitting, and "Reset Prompt" reverts. sref specifically carries over by default on rerun/vary/remix (same style code persists) unless you edit it out. This is why the user's wave sref stays attached during Remix (and why `--sw` doesn't error).

**Remix param constraint (official):** you can add/remove params in Remix but they must stay mutually compatible (e.g. changing --version can make an old --stylize value illegal → error). Only params that influence variations apply (ar, no, stop, tile listed).

**--sw needs a style source:** `--sw` requires an active `--sref` (image URL or numeric code). Without one → "--sw requires style reference" error. `--sw` is INCOMPATIBLE with Moodboards/`--p` (silently ignored there — moodboards use `--s` instead, per [[mj-moodboard-vs-sref]]). Range 0–1000, default 100. Community sweet spot 65–175; blakecrosley bands 0–50 subtle / 50–150 balanced / 150–300 strong / 300–1000 dominant.

**RECOLOR while keeping composition — ranked for CURRENT web app:**
1. **Retexture** (Editor > Retexture tab) — PURPOSE-BUILT for this. Uses a depth controlnet: keeps original SHAPE/composition, repaints textures/colors/materials/lighting from your new prompt. Supports `--sref`/`--sw`/cref/personalization. CAVEAT: Editor/Retexture currently runs on the V6.1 model, not V8.1 — expect a slight quality/aesthetic shift from a V8.1 keeper. Best structural preservation.
2. **Remix Subtle** — keeps layout, lets you change palette via color words + keep the wave sref at low `--sw`. Looser composition-lock than Retexture but stays on the V8.1 pipeline (no model downgrade). Good when you want to preserve the V8.1 look and only nudge palette.
3. **Vary Region / inpaint (Editor)** — only for LOCAL recolor of a masked area, not a global palette shift; also V6.1. Not first choice for whole-image recolor.

**Remix + sref palette conflict (⚠️ community/inferred, LOW-MED confidence — not doc-stated):** at low `--sw` (~20–60) the sref imposes little palette; text color words dominate → good for "texture yes, palette no." At high `--sw` (~200) the sref's own palette reasserts and can override the text color words. So for "keep the dissolve/texture from the wave sref but recolor via text," LOW --sw (the user's --sw 30) is the correct lever. No official doc gives numeric sw guidance for this; bands are secondary-source.
