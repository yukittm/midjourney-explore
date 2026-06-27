---
name: mj-optical-refraction-spectral
description: MJ prompt craft for optical/refractive subjects — refraction/caustics vs thin-film iridescence, the prism cliche, backlight as key cue, raw-vs-standard open question
metadata:
  type: reference
---

Web-verified (2026-06) findings on rendering OPTICAL/REFRACTIVE subjects in MJ V8.1 and getting "flowing spectral color" instead of generic stock-prism. Mostly OPINION from prompt-guide authors (Reddit unretrievable — see [[web-access-constraints]]); param facts VERIFIED vs MJ docs / blakecrosley V8.1 ref.

**Two distinct registers — keep separate:**
- REFRACTION/CAUSTICS = light bent THROUGH glass/crystal/water, projecting color onto a surface. Keywords: `caustics` (strongest; "forces AI to calculate light passing through"), `subsurface scattering` (translucency glow, not rainbow), `refraction effect`/`refractive edges`. Needs HARD BACKLIGHT + dark bg. Photoreal route: `--style raw` + low `--s`.
- THIN-FILM IRIDESCENCE = color ON the surface of bubbles/oil/shells (swirling, not banded). Keywords: `iridescent`, `oil slick`, `soap bubble`, `pearlescent`/`opalescent`, `holographic`, `duochrome`, `chromatic color shifting` (or `iridescent chromatic color shifting` for stronger). Macro framing + soft diffuse light + dark bg. **This is the BEST route to "flowing spectral color" and the cliche-safe one** (continuous color fields, not rainbow stripes, on organic surfaces).

**Backlight is load-bearing**: refraction only reads when light passes THROUGH subject toward camera. `backlit`/`rim light` (halo, separates transparent subject), `volumetric light`/`godrays` (visible beam), `sunlight through window`/`dappled light` (caustics). Recommended setup: hard directional/single-spot light from behind or behind-side, high contrast, dark bg.

**The "rainbow prism on white bg" cliche** is produced by: `prismatic` + studio/white bg + high stylize + render-engine keywords (`octane render`, `unreal engine`, `rtx`, `4k/8k`, `hyper-real CGI`). Those render keywords PUSH INTO sterile CGI — avoid for artful color. Antidotes (consistent across sources): dark/contextual bg, `caustics` onto a real surface OR `iridescence` instead of `prismatic`, `--style raw`, LOW stylize, and PHOTOGRAPHIC cues (film stock `Kodak Portra 400`, lens `85mm`/`f1.4`, `film grain`, `chromatic aberration`) instead of render cues. See [[mj-style-raw]], [[mj-no-param-antiplastic]], [[mj-stylize-chaos-hd-params]].

**Caveat on `chromatic aberration`**: MJ renders it mostly as purple/green lens fringing (random), NOT a full spectral rainbow. Use `iridescent` for real color.

**Params (optical-specific)**: stylize LOW 0-100 for crisp optical color (high stylize re-averages/washes detail AND competes with sref — get color from subject+lighting+sref, not from cranking stylize). chaos 25-50 for exploration (refraction is high-variance, chaos surfaces good rolls), 0-25 final. `--hd` fine, resolves fine caustic detail.

**KEY OPEN QUESTION (verify in-app, not evidenced anywhere)**: raw vs standard mode for optical color. Inference: raw+low-s = photoreal/literal; STANDARD mode (no raw) applies MJ's aesthetic color bias = likely LUSHER spectral color for a painterly result. No source A/B-tests this on optical subjects. Test both.

**Untested as literal trigger words (NO MJ-craft evidence, only physics pages)**: `dichroic`, `thin-film interference`, `spectral`. Likely usable but unverified — reach the effect via `iridescent`+`oil slick`+`soap bubble`+`beetle shell`/`butterfly wing` (real-world iridescence anchors MJ recognizes). Glass `--sref 1656023399` ("best clear glass sref") also UNVERIFIED — test before baking into a recipe.
