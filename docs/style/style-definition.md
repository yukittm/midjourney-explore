---
updated: 2026-06-21
status: draft
type: style
---

# Style Definition — SSoT

> Working SSoT for the project's own visual style. Still pre-full-Phase-1: refined as generations
> validate. The model below was corrected by a multi-agent `/verify` pass (2026-06-21) — see the
> Decision log. Craft/how-to lives in [[prompting]]; source analysis in [[reference-accounts]].

## Two axes

"My style" = two independent decisions, mapping onto Midjourney's content/style split:

| Axis | what it is | MJ lever |
|---|---|---|
| **A. Reference taste** | how it looks | moodboard / `--sref` / `--s` |
| **B. Subject world** | what is depicted | the text **prompt** |

Independent: hold taste fixed and vary subjects, or vice versa. A coherent creator-style holds both.

## Axis A — taste: giz-based blend (now **giz-dominant**)

- **Origin**: a blend of `giz.akdag` (crisp, bold color-blocking, surreal-editorial) × `marianopeccinetti`
  (retro, grainy, dreamy collage).
- **Current basis (2026-06-21)**: the curated `blend-v1` moodboard is **giz-only — 11 images**
  (`~/Desktop/reference-blend-v1/`; Mariano dropped + swaps in curation). The blend has shifted
  **giz-dominant**.
- **The unifying look = the moodboard's bold color-blocking + saturated color grade**, constant across modes.

### The render model — 2 dials (corrected 2026-06-21 via `/verify`)

Realism is **NOT** derived from subject type (an earlier 1-dial model claimed it was; falsified by the
curated set itself — the soft/graphic sheep, the soft-photoreal baobab & island, the painterly ibises).
The style varies along **two independent dials**:

1. **Subject dominance** — pure-landscape (**heroless is first-class**) → minor subject → photoreal hero.
2. **Render register (3-stop)** — flat-graphic / **soft-painterly (the characteristic middle, most at risk
   of being engineered out)** / crisp-photoreal. Sampled **independently** of subject; set in MJ by
   `--s` / `--style raw` + the moodboard.

There is a content *tendency* (human figures → photoreal; built / bare-landscape forms → graphic) but it
is a lean, not a law — register must stay an independent control.

### Finish

Driven by **subject + motion**, **not** shot distance. **Crisp is the default** in the current giz basis;
**film-grain / matte is absent** from it (a Mariano artifact) → future scope, not now.

### Color

Strong unity in the giz-only basis: **red/orange field + green + deep-blue sky** color-blocking. **Leave
color to the (color-coherent) moodboard** — don't specify it in-prompt — to keep batch unity.

## Axis B — subject world: **giz-based surreal natural world** (decided 2026-06-21)

Natural / geological landscapes as the **stage**, optionally inhabited by giz-signature elements. The
spine (the actual discriminator, per `/verify`): **bold color-blocking + a single graphic gesture against
negative space** — the natural world is the stage, not the theme.

Subject range (breadth within unity):
- **Terrain (base)**: hills, plains, desert, water, rock, plateau.
- **Architecture/structure**: a **lone tiny house/cottage on a hill — the signature recurring motif (~7/11)**;
  geometric pavilion / cube.
- **Flora**: cacti, a lone iconic tree, flowering shrubs.
- **Fauna**: horse, antelope, birds; **figure-on-animal composite** (e.g. the antelope rider).
- **Figures**: a lone person, dancers, small groups.
- **Devices**: scale-play, mirroring, **motion (a giz signature)**, color-blocking.

**Heroless color-field landscapes are first-class** (~5 of the 11 keepers), not a defect.

Prompt convention: **detailed/specific** (richly specify subject + composition + light; style on the
moodboard). See [[prompting]].

## Future scope (generalized)

Registers **beyond the core giz natural-landscape world** — including the Mariano-derived **cosmic / sea /
film-grain** registers — are **deferred**. Revisit as future lanes after the core is locked. (Fuller
candidate directions from the earlier "world-views" exploration are in git history; revive if wanted.)

Deferred future lanes (names kept here; fuller detail in git): Still Poetry · Bold Play (sport/dynamic) ·
Editorial Mirage (fashion) · Scale Theater · Domestic Cosmos · Quiet Rituals · Elemental Companions ·
Solitary Wonder · Dreamt Weather · Chromatic Solitude.

## Reference material

- Imported pool in `../../references/` (giz 18 + mariano 7 + 5 videos; provenance `references/manifest.jsonl`).
- **Curated moodboard basis = `~/Desktop/reference-blend-v1/` (11 giz).**
- giz SREF codes **not harvested** (a paid product on her Contra) — route is the moodboard. See [[reference-accounts]].

## Decision / verification log

- **2026-06-18**: two-axis framing; blend direction set.
- **2026-06-20**: reference pool imported; prompt convention = detailed/specific; doc cleanup + frontmatter.
- **2026-06-21**: Phase-1 moodboard built & rendering coherently. Multi-agent `/verify` ×2 (full, then re-run
  scoped to the curated 11) → **2-dial model** (not 1-dial; realism *not* subject-derived); **heroless =
  first-class**; **figure-on-animal** hero added; cosmic/sea/grain → future scope; **prompt-gen skill
  DEFERRED** (validate via Phase 1 first; later a thin sampler-only skill). Docs consolidated 7→4.

## Status

**Hypothesis → being validated by Phase-1 generation.** Promote `draft → active` once the 2-dial model and
finish hold across a test set.
