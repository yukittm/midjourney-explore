---
updated: 2026-06-23
status: active
type: reference
---

# Reference Accounts — style inspiration

Instagram accounts the user wants to reference for visual taste. These form the **reference pool**:
curate representative images → use one bold image as a **`--sref`** (the project's color channel) →
drives "similar taste" generation. See [[style-definition]] (the model), [[prompting]] (the craft), and
`../research/2026-06-21_midjourney-v8.1-current.md` (current mechanics).

> Goal: distill the *aesthetic qualities* (palette, light, composition, subject, mood, finish) into
> the user's **own original style** — inspiration, not cloning a specific creator's work.
>
> **Naming note:** the reference artists are analyzed here as *inspiration only*. The artist's name does
> **not** appear in the project's style vocabulary (registers, prompts) — it survives only as an
> **unnamed private `--sref` image**. See [[style-definition]].

## Accounts

| Handle | URL | Status | Notes |
|--------|-----|--------|-------|
| `giz.akdag` | https://instagram.com/giz.akdag | ✅ confirmed (verified, public, 461K followers, 1,098 posts) | "Gizem Akdag — AI Explorer / Creative Director". AI-generated (Midjourney) editorial art. Has a public **SREF Collection** highlight, but the codes appear to be a **paid product** (Contra) and the slides are videos — not harvested (see below). Also `@gizakdag`; bio links contra.com/gizemakdag. |
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
- **SREF Collection note**: her highlight publishes sref codes, but they appear to be a **paid product** (Contra) and the slides are videos (not capturable) — **not harvested** (decided 2026-06-20). Our route is a self-uploaded bold reference image as `--sref`, not her codes.
- Representative posts seen: NYC subway editorial ("refund hits different"), cactus tennis court, tree-house hybrid with dancers, favela + pink ladder/scale-play, pink wave-sofa by the sea, man walking a horse with a Polaroid, ocean-swimmers aerial, folk-art juice stall, red-dress figure in banana leaves, liquid-marble soccer figure.

### marianopeccinetti (Mariano Peccinetti) — first-pass analysis (2026-06-18, from top ~12 grid posts)

- **Medium**: vintage **digital collage** (since 2012) + AI — grainy, matte, print-like texture, as if cut from old magazines/postcards.
- **Subject matter**: surreal dreamscapes; **cosmic/celestial** motifs (moons, Saturn rings, rainbow arcs, starfields) + nature (horses, oceans, deserts, flowers, clouds); small human figures dwarfed by vast landscapes.
- **Palette**: nostalgic, faded/dusty retro tones — dusty pink, teal, cream, ochre — with occasional psychedelic gradient pops (sunset arcs). Retro-print color, lower saturation than giz.akdag.
- **Lighting/finish**: matte, soft, **grainy vintage photographic texture**; dreamy rather than crisp.
- **Composition**: collage juxtaposition & **scale play** (tiny car/figures vs huge cosmic elements); poster-like, often portrait.
- **Mood**: dreamy, nostalgic, poetic, contemplative surrealism — his own words: "visual poetry".
- **Representative posts seen**: flowers floating on a sea with a swimmer, appaloosa horse on a pink/green hill, giant rainbow arc over a dune with a tiny yellow car, horses galloping among clouds & fish, cotton-candy-cloud legs with soccer ball, people seated on a Saturn ring, motion-blur coastal cars, leaping cat with radial blur, pink rock formations.

### Converged giz signature — from the FULL 11-image curated set (2026-06-23)

Derived from **3 independent reads of all 11 curated images** (`~/Desktop/reference-blend-v1/`) — an independent
characterization + an adversarial check — after an earlier 2-image over-generalization was caught (see
`.claude/rules/LESSONS.md`). This is the project's working signature (the **calibration anchor for our OWN
style**; the curated 11 = the user's chosen *direction*, not all of giz):

- **Heroless / minimal is the majority** (~7/11); a dominant human/animal hero is the minority (~3-4/11).
- **Saturated red/orange + green + deep-blue CHORD** is the core palette; deep-cobalt sky is the default (~7/11, not universal).
- **ONE clear, often surreal, idea per frame**; never busy/multi-idea. **Generous negative space + restraint.**
- **Richness = saturation + the single idea + a few present elements + decisive light — NOT element count or hero dominance** (~8/11 "striking via few"; only ~3/11 "rich via density").
- **ONE render mode: photoreal.** The "graphic / color-block" look is **composition + hard light on real subjects**, not a flat/illustrated render. (A proposed "two-mode flat-graphic vs photographic" split was *falsified* — all 11 are photoreal.)
- **Decisive light**, two treatments: hard high-key/graphic (heroless/color-field) ⇄ golden warm-directional (with a subject).
- Recurring motifs: a small **white-cube / white-house geometry** (~6/11); **motion-blur** as a deliberate device; 3:4 vertical with strong horizontal banding.

The locked model + the on-style **reward gate** derived from this live in [[style-definition]]. **Mariano stays
a deferred input** — referenced later when the project converges its **own** house palette (not yet locked).

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

→ Status: this pool feeds a **single bold `--sref` image** (the project's color channel) — the earlier
`blend-v1` moodboard (giz-only, 11 images) is superseded as the color tool (a moodboard mutes color; see
[[style-definition]] Color channel). The locked model + direction live in [[style-definition]].
