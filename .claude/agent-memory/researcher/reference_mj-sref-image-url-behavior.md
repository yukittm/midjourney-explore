---
name: mj-sref-image-url-behavior
description: What an image-URL --sref transfers (style-only, NO composition), --sw range/bands, and sref+image-prompt combination on MJ V8/V8.1
metadata:
  type: reference
---

Web-verified 2026-06-26 (docs.midjourney.com 403s on WebFetch — used WebSearch verbatim snippets + blakecrosley.com + midlibrary.io). Re-confirmed 2026-06-26 (2nd pass). See [[mj-sv-style-reference-version]] for the --sv story and [[web-access-constraints]].

**Official Style Reference article URL (current):** https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference (the older `32100404500749-Style-Reference` is stale — the article ID changed). Version article: https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version. All still 403 on direct WebFetch; read via search snippets.

**--sref transfers STYLE ONLY, not composition/subject.** Official docs (Style Reference article, via search snippet): a Style Reference "doesn't copy objects or people, just the overall style—like colors, medium, textures, or lighting—helping you achieve a consistent visual theme." So an image-URL `--sref` carries color/palette, medium, texture, lighting/mood — and IGNORES specific objects, subject matter, AND composition/layout. This is the key contrast vs. using the image as an **image prompt** (image prompt DOES pull in subject + composition; influence tuned by `--iw`). CAVEAT: one secondary source (midlibrary photographers guide) loosely lists "composition" among what sref "draws upon" — this contradicts the official docs and is the weaker source; trust the official "doesn't copy ... composition" wording.

**--sw (style weight): range 0–1000, default 100** (confirmed by official Style Reference doc snippet + blakecrosley + midlibrary, all agree). Higher = style ref dominates (palette/mood/medium pushed harder); lower = text prompt wins. blakecrosley bands: 0–50 subtle, 50–150 balanced, 150–300 strong style match, 300–1000 dominant. For strong-but-not-washed-out color, ~150–300 is the "strong match" band (community/secondary estimate, not official). NOTE: `--sw` ≠ `--iw` (image weight, for image prompts).

**--sref + image prompt / Omni / Char ref CAN be combined in one job** (official: "combine images with style codes"; secondary sources confirm sref + image prompt + cref/oref coexist). When combined: the image prompt supplies subject/composition (strength via `--iw`), `--sref` supplies style (strength via `--sw`) — they act on different axes. Multiple sref images allowed (space-separated; per-image weight via `::value` after URL).

**Model version (2026-06-26):** V8.1 is the current default (became default ~2026-06-10/11; released on web 2026-04-30). No V8.2 or V9 shipped; V8.2 is the active improvement target, no public roadmap/date.
