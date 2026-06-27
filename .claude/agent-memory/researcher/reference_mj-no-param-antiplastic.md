---
name: mj-no-param-antiplastic
description: MJ --no behaves as a -0.5 negative weight (not a hard remove); moderation reads each --no word independently; anti-plastic/CGI craft recipe (style raw + low stylize + film/lens/light cues)
metadata:
  type: reference
---

Web-verified 2026-06-26 via docs.midjourney.com "No" article (search snippet; page 403s on fetch), whytryai.com negative-prompt deep dive, and multiple 2025-26 photoreal guides (pxz.ai, promptsera, fluxnote, aiarty, halfjourney/Medium). See [[mj-stylize-chaos-hd-params]], [[web-access-constraints]].

**--no = negative weight, NOT a hard delete.** Official "No" doc: using `--no X` is the SAME as weighting that part of a multi-prompt to **-0.5**. It reduces probability/influence; it does not guarantee removal. whytryai confirms: "Despite adding lots of negative descriptors, you may still find Midjourney including these elements." So --no is a nudge, not a switch. Explicit multi-prompt negative weights can be tuned ~ -0.2 to -0.9 for more/less strength.

**CRITICAL caveat — moderation reads each --no word INDEPENDENTLY.** Official doc example: `--no modern clothing` is read as "no modern" AND "no clothing" (would strip clothing entirely). Implication: multi-word --no phrases fragment. Prefer single tokens or well-known compound terms ("octane render" is safe-ish as a known phrase, but watch "smooth plastic" → "no smooth" + "no plastic"). Best practice per docs: describe what you DO want in the positive prompt instead of relying on --no.

**Anti-plastic/CGI recipe (verified consensus across guides):**
1. `--style raw` — bypasses MJ's default "beautification"/stylization filter (official Raw doc: simple prompts get more realistic/photo-like; less opinionated, more literal). Single biggest lever.
2. LOW `--stylize` (--s 0–100) — high stylize re-adds the artificial "overly perfect" look; low = literal/realistic. (Note: one guide said 500–750 "works for realism" — that's an OUTLIER vs the low-stylize consensus; treat low as default.)
3. Positive medium/optics cues do real work: film stock (Kodak Portra 400, Cinestill 800T), "shot on [camera]", lens/aperture (100mm macro, f/1.8), "film grain", "natural light / golden hour / soft diffuse light", "skin/surface texture", "subsurface scattering". Naming a real capture medium pulls from photographic (not 3D-render) training data.
4. `--no` list practitioners actually use: `3d render, cgi, octane render, unreal engine, plastic, airbrushed, smooth, digital painting, illustration, cartoon, anime, blown out highlights, artificial lighting`. Keep tokens single-word where possible (moderation fragmentation).

**Why macro/close-ups go plastic (mechanism — mix of verified + opinion):** training-data bias toward retouched/smoothed imagery + missing camera spec → MJ defaults to flawless smooth surfaces, hard specular highlights, studio-lit gloss, and ZERO grain/noise (the "too-processed when you zoom in" tell). Counter by explicitly requesting grain, matte/diffuse light, real texture, and a capture medium.
