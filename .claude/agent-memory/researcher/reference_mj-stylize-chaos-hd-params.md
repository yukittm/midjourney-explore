---
name: mj-stylize-chaos-hd-params
description: MJ V8.1 --stylize/--chaos/--hd ranges, defaults, and the high-stylize-vs-sref competition (stylize fights sref, doesn't amplify it)
metadata:
  type: reference
---

Web-verified 2026-06-26 via docs.midjourney.com snippets (Stylize, Chaos/Variety, Style Reference, Omni Reference, Parameter List, Version articles), blakecrosley.com (fetched), and community guides. High confidence on ranges/defaults; medium on band thresholds (secondary). See [[mj-sref-image-url-behavior]], [[mj-sv-style-reference-version]].

**--stylize: range 0–1000, default 100** (official Stylize doc). Named tiers: --s 50 = "Style Low", 100 = default, 250 = "Style High", 750 = "Style Very High". Higher = more artistic freedom / strays from prompt; lower = more literal.

**--stylize vs --sref: they COMPETE, they do NOT amplify the sref.** High stylize DILUTES/washes out a style reference. Official basis: Omni Reference doc says high --stylize/--exp "compete for influence," so raise the reference weight to compensate (same principle applies to sref/--sw). Official Style Reference guidance: if a referenced style doesn't show clearly, REDUCE --stylize. So for faithful color/style transfer, keep stylize MODERATE (community sweet spot ~60–175) and raise --sw, rather than pushing stylize to 250. At --s 250 ("Style High") the sref's palette/medium can get overridden by MJ's own artistic interpretation. NOTE: official docs say --sw "has more impact with style CODES than with image URLs" — so an image-URL sref is somewhat more robust to high stylize than a numeric code, but the competition still holds.

**--weird (--w): range 0–3000, default 0** (official Weird doc, web-verified 2026-06-26). Takes creative risks on CONTENT itself (melting forms, three-eyed faces) — the lever for "object becomes virtual/abstract" surreal transformations / morphology, NOT for material realism or color absorption. Grid stays consistently-weird-but-varied. Experimental + INCONSISTENT at high values; not fully seed-compatible. Stacks with --stylize ("wonderfully interesting" together), no documented hard conflict and no numeric coupling; but --chaos 100 + --weird 3000 = grid detached from prompt. Distinct from --chaos: weird changes WHAT the subject is; chaos only spreads the 4-grid. Craft band for deliberate deformation ~250–750 (community estimate).

**--chaos (--c): range 0–100, default 0** (official Chaos/Variety doc; "Variety" on midjourney.com). Higher = the 4-image grid varies more / strays from prompt. Bands (blakecrosley/community): 0–25 final-render/consistent, 25 = "slight variations", 50–75 exploration. **--chaos 10 is LOW/mild and safe** — below the 25 "slight variations" threshold, so minimal grid variety with low incoherence risk. Not a coherence hazard at 10.

**--hd: EXISTS and is current on V8.1** (NOT deprecated). It is V8.1's native-2K (2048px) HD generation, replacing the old separate upscale step. HD is the DEFAULT on V8.1 standard jobs; --sd = standard-def cheaper alt. Cost ~1.3 GPU min (HD) vs ~0.8 (SD). This is a DIFFERENT meaning from the legacy pre-V6 "--hd high-definition style" param. --hd is --sv7-compatible (the V8.1 sref default supports --hd). **No known conflict between --hd and --stylize, --chaos, or --sref/--sw.** --hd's incompatibilities (per compatibility chart) are with V7-only features: Omni Reference (--oref/--ow), Character Reference, multi-prompts, --q (Quality), Niji, Turbo — none of which are stylize/chaos/sref.
