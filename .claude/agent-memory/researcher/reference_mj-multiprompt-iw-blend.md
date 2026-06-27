---
name: mj-multiprompt-iw-blend
description: MJ V8/V8.1 facts — multi-prompts (::) NOT supported on V8/V8.1 (only v1-6.1/Niji); --iw range/default; /blend still current
metadata:
  type: reference
---

Web-verified 2026-06-26 (docs.midjourney.com 403s — used WebSearch verbatim snippets of the official Multi-Prompts/Version/Image-Prompts/Blend docs + blakecrosley + kitemetric + mjsplitter + geekycuriosity). See [[web-access-constraints]], [[mj-sref-image-url-behavior]].

**MULTI-PROMPTS (`::` separator and `::N` weights) — NOT supported on V8/V8.1.** Official Multi-Prompts & Weights doc lists support for: "versions 1, 2, 3, 4, Niji 4, 5, Niji 5, 6, Niji 6, and 6.1." V7, V8, V8.1 are NOT in that list. blakecrosley confirms: "Multi-prompts are not listed as V8.1-compatible in the Version compatibility chart." Weight precision sub-rule: v1-3 whole numbers only; v4/Niji4/5/Niji5/5.1/5.2/6/6.1 allow decimals. => For V8.1 production prompts, do NOT use `::` weighting; it's silently ignored / not honored on current models.

**IMAGE WEIGHT `--iw`** — official Image Prompts + Parameter List docs give **range 0–3, default 1** for V7 and V6 (V5 was 0–2, default historically 0.5/1). The docs do NOT publish a distinct V8/V8.1 number; multiple secondary guides (kitemetric, mjsplitter, stefvanlooveren) all report 0–3 default 1 and explicitly do NOT carve out a different V8/V8.1 range. The "V8 = 0.5–3.0" and "V8.1 = 0–2" claims are UNVERIFIED secondary-source noise that mjsplitter itself warns about ("some older content references 0-2... prioritize official docs"). Best-supported value for V8.1: **0–3, default 1** (inherited V6/V7 figure; no official V8.1-specific override found). Image prompts + --iw were ABSENT in V8.0 and RESTORED in V8.1 (official updates.midjourney v8.1-alpha: "Image prompts and even image weights are now available in V8.1").

**`/blend` — still current.** Official "Blend Images in Discord" doc live: combines up to 5 images, no text prompt support, optional dimensions, respects custom suffix. For >5 images or to mix with text, use `/imagine` with image prompts instead. Image Prompts doc: paste image URL directly into prompt; text is optional but "if you use text prompts together with image prompts, you will have a greater degree of control"; `--iw` is the controlling parameter for image-vs-text balance.
