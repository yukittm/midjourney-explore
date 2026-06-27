---
name: mj-night-sky-and-ar45
description: MJ V8.1 dark/night/space-scene behavior (high-stylize over-bloom, bright-sref-vs-dark tension, night-sky failure modes) + --ar 4:5 support confirmation
metadata:
  type: reference
---

Web-verified 2026-06-26 (docs.midjourney.com 403s on fetch → WebSearch verbatim snippets + blakecrosley.com + midlibrary.io fetched). See [[mj-stylize-chaos-hd-params]], [[mj-style-raw]], [[mj-sref-image-url-behavior]], [[mj-optical-refraction-spectral]].

**--ar 4:5 is SUPPORTED on V8.1** (official Aspect Ratio doc lists it; community guides confirm 4:5 added 2026-01-20 alongside 6:11/5:4/21:9). V8.1 accepts any ratio ~1:2 to 2:1; beyond that is experimental. No decimals (use 139:100). 4:5 = the IG portrait ratio.

**High --stylize (~250+) on DARK scenes — the over-process risk is REAL but partially indirect.** Official Stylize doc: stylize controls how strongly MJ applies its training toward "artistic color, composition, and forms"; higher = more artistic/visually interesting but strays from prompt, lower = "sticks to the facts without much extra flair." Community elaboration (easyaibeginner, scalebytech): high stylize → "colors pop like neon," "more saturated," "lush brushstrokes and deep shadows," "dynamic/cinematic lighting" — i.e. MJ ADDS its own saturation/contrast/glow flourishes. For a LOW-KEY night sky this means MJ can brighten/over-saturate/bloom the scene away from the requested dark tone, AND (per [[mj-stylize-chaos-hd-params]]) high stylize COMPETES WITH the sref, washing the palette. No official doc names a dark-scene-specific stylize failure (UNVERIFIED at doc level) — treat the over-bloom-on-dark claim as well-supported community inference, not an official statement. Actionable: keep --s LOW/moderate for low-key scenes, carry color via sref+--sw not via high stylize.

**Bright/saturated sref vs DARK prompt — documented tension + fix.** sref pulls "colors, medium, textures, OR lighting" (official Style Reference doc), so a bright sref WILL push lightness/saturation and can fight a requested dark/low-key tone. Official guidance for "too dark/too bright" mismatch: (a) remove conflicting images from the board / swap to better-matched refs, (b) LOWER --sw so the prompt's lighting language wins. Also official: "use your text prompt to describe what you want to SEE, not how MJ should modify the reference" — explicit dark/low-key/night language in the prompt takes precedence when --sw is moderate. Caveat (community): --sw behaves inconsistently image-vs-code — sw150 subtle on an image but can "obliterate your prompt" on a code. So with a bright image-sref + dark prompt: moderate-to-LOW --sw + strong explicit night/low-key prompt language is the lever; do NOT also push stylize.

**Standard (no --raw) = MORE painterly/stylized; --raw = flatter/more photographic.** Official Raw doc: Raw "reduces automatic beautification → more accurate match when prompting specific styles"; Standard = MJ "adds its own creative touch / auto-pilot" (the MJ Aesthetic: painterly finish, moody cinematic lighting). So for "painterly flowing color, NOT a stock photo," OMITTING --raw (standard mode) is correct — it leans into MJ's artistic interpretation. Raw is the lever for photographic literalism, the opposite goal. (Confirms [[mj-style-raw]].)

**Night-sky / space failure modes (community, no official doc):**
- "night sky" alone → MJ defaults to "generic dark blue with scattered dots." Fix: specify star density, Milky Way band, nebula color, moon phase, atmospheric effects (e.g. "dense Milky Way band, thousands of pinpoint stars, soft violet/teal nebula clouds").
- Sky-only prompts → abstract/floaty; name a foreground/ground anchor for compositional storytelling.
- MJ's native astrophotography aesthetic (midlibrary): "deep blues and vivid oranges, contrasted with blacks and luminescent whites," "dreamy/surreal," central-focus + diagonal lines — i.e. it has a strong DEFAULT cosmic palette that can read as generic/3D-render-ish "space stock art." Counter with raw OR specific astrophotography/film cues + the sref to override the default blue-orange.
- For non-anime realism keep stylize moderate; the "stylize >700 ruins anime" note is anime-specific, not a general dark-scene rule.
