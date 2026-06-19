# Reference Accounts — style inspiration

Instagram accounts the user wants to reference for visual taste. These form the **reference pool**:
curate representative images → Midjourney moodboard (or image-URL `--sref`) → drives "similar taste"
generation. See `sref-sweep.md` and `../research/2026-05-11_midjourney-prompt-best-practices/03_*`.

> Goal: distill the *aesthetic qualities* (palette, light, composition, subject, mood, finish) into
> the user's **own original style** — inspiration, not cloning a specific creator's work.

## Accounts

| Handle | URL | Status | Notes |
|--------|-----|--------|-------|
| `giz.akdag` | https://instagram.com/giz.akdag | ✅ confirmed (verified, public, 461K followers, 1,098 posts) | "Gizem Akdag — AI Explorer / Creative Director". AI-generated (Midjourney) editorial art. Has a public **SREF Collection** highlight = shares the actual MJ sref codes. Also `@gizakdag`; bio links contra.com/gizemakdag. |
| `marianopeccinetti` | https://instagram.com/marianopeccinetti | ✅ confirmed (verified, public, 446K followers, 600 posts) | "Mariano Peccinetti — Digital Collages since 2012 · Imaginary Concepts · AI Explorer · Visual poetry". Clients: Gucci/Vogue/Netflix/Guardian/GQ. linktr.ee/marianopeccinetti. (Earlier `marianpoccinetti` was a misspelling.) |

## Aesthetic analysis (fill once images are viewed — do NOT guess)

Per account and/or combined, capture:

- **Subject matter**: what's in frame (portrait / fashion / interior / still-life / landscape ...)
- **Palette**: dominant colors, saturation, warm/cool
- **Lighting**: hard/soft, direction, natural/studio, time of day
- **Composition**: framing, negative space, symmetry, crop ratios
- **Medium / finish**: film vs digital, grain, contrast, post-processing look
- **Mood**: the emotional register
- **Recurring motifs**: anything that repeats and signals the "signature"

### giz.akdag — first-pass analysis (2026-06-18, from top ~17 grid posts)

- **Medium**: AI-generated (Midjourney) conceptual/editorial imagery — photographic realism with a surreal twist.
- **Subject matter**: single hero human figures (often fashion-forward, Black subjects), surreal scenarios; sport/leisure motifs (tennis, soccer, swimming, horse-walking); occasional still-life / market scenes.
- **Palette**: saturated yet filmic; **bold color-blocking** with complementary contrasts — cobalt/cornflower blue, emerald/forest green, terracotta & red-orange, cream/putty. High color confidence, not muted.
- **Lighting**: clean natural daylight, crisp, lightly cinematic — bright and optimistic, NOT moody/dark.
- **Composition**: graphic, poster-like, strong central subject, balanced negative space; portrait crops (~4:5).
- **Medium/finish**: believable photo + painterly/surreal elements; subtle film grain & color.
- **Mood**: playful, witty, optimistic, surreal-but-elegant — "quiet-luxury meets surreal concept".
- **Recurring motifs**: lush vegetation (cactus, banana leaves), water, color-blocked wardrobe, scale-play & figure/material morphing (e.g. a person made of liquid marble), conceptual juxtaposition.
- **🎯 Direct lead**: her **SREF Collection** highlight publishes the Midjourney sref codes behind these looks → prime candidate `--sref` inputs for our sweep (`sref-sweep.md` §2). To capture: open the highlight, read each slide's code, log into the sweep table. (Not yet done.)
- Representative posts seen: NYC subway editorial ("refund hits different"), cactus tennis court, tree-house hybrid with dancers, favela + pink ladder/scale-play, pink wave-sofa by the sea, man walking a horse with a Polaroid, ocean-swimmers aerial, folk-art juice stall, red-dress figure in banana leaves, liquid-marble soccer figure.

### marianopeccinetti (Mariano Peccinetti) — first-pass analysis (2026-06-18, from top ~12 grid posts)

- **Medium**: vintage **digital collage** (since 2012) + AI — grainy, matte, print-like texture, as if cut from old magazines/postcards.
- **Subject matter**: surreal dreamscapes; **cosmic/celestial** motifs (moons, Saturn rings, rainbow arcs, starfields) + nature (horses, oceans, deserts, flowers, clouds); small human figures dwarfed by vast landscapes.
- **Palette**: nostalgic, faded/dusty retro tones — dusty pink, teal, cream, ochre — with occasional psychedelic gradient pops (sunset arcs). Retro-print color, lower saturation than giz.akdag.
- **Lighting/finish**: matte, soft, **grainy vintage photographic texture**; dreamy rather than crisp.
- **Composition**: collage juxtaposition & **scale play** (tiny car/figures vs huge cosmic elements); poster-like, often portrait.
- **Mood**: dreamy, nostalgic, poetic, contemplative surrealism — his own words: "visual poetry".
- **Representative posts seen**: flowers floating on a sea with a swimmer, appaloosa horse on a pink/green hill, giant rainbow arc over a dune with a tiny yellow car, horses galloping among clouds & fish, cotton-candy-cloud legs with soccer ball, people seated on a Saturn ring, motion-blur coastal cars, leaping cat with radial blur, pink rock formations.

### Synthesis — what the two have in common vs. differ (for finding "my style")

- **Common ground**: both are **AI-driven surreal/conceptual** image-makers with single or few figures, strong concepts, scale-play, and a poster/editorial sensibility.
- **Key difference = texture/era register**:
  - `giz.akdag` → **crisp, bold, saturated, contemporary editorial**, color-blocked, witty.
  - `marianopeccinetti` → **faded, grainy, retro-collage, cosmic-dreamy**, lower saturation, poetic.
- **Decision the user faces**: pick one register, or define a personal blend (e.g. surreal-conceptual subjects in a chosen color/texture treatment). This is the core of the style-establishment phase.

## Reference image pool (imported 2026-06-20)

Manually downloaded from Instagram by the user → imported into this project (self-contained;
no other-project tooling) via `scripts/import_references.py`. Binaries git-ignored; provenance
tracked in `references/manifest.jsonl` (sha256, source, attribution).

| Handle | location | count |
|---|---|---|
| giz.akdag | `references/giz.akdag/` | 18 images |
| marianopeccinetti | `references/marianopeccinetti/` | 7 images |
| (videos, unattributed) | `references/_unsorted/` | 5 mp4 |

Attribution was by IG media-id filename group, with one sample per group visually verified.

→ Next: pick the strongest ~8–15 across both → build a blended moodboard (register its snapshot
code in `../../moodboards/`) and translate into `style-definition.md`. Needs MJ plan (Phase 1+).
