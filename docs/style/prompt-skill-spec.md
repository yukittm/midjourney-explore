---
updated: 2026-06-21
status: draft
type: guide
---

# Prompt-Generation Skill — Spec (DRAFT, under verification)

The content to encode in `.claude/skills/mj-prompt-forge/SKILL.md`. This is the consolidated recipe
from the whole style-establishment thread. **Under multi-agent verification before build.**

## Purpose
Generate N **varied, intentional, on-style** Midjourney prompts for the project's blend world, to be
run with the project's moodboard (the moodboard is set in MJ, not by the skill).

## World / theme (Axis B)
giz-based **surreal natural world**: natural/geological landscapes as the stage, optionally inhabited
by giz-signature elements. Natural atmosphere base. Topical/event objects + cosmic + sea/waves are
**extensible motifs** decided per batch.

## Mode = ONE soft dial (refined per premise-check — UNDER VERIFICATION)
- **Dial — subject dominance**: pure landscape (no subject) → minor subject → photoreal subject hero.
  Continuous; sample across it incl. in-between (soft boundaries, no hard buckets).
- **Realism is DERIVED, not an independent dial**: organic subjects (animals/figures/trees) → photoreal;
  geometric/landscape forms → graphic; plus a global `--s`. (Avoids incoherent "graphic photoreal animal".)
- **Unifying look = the moodboard** (color grade / bold color-blocking) — constant across all modes.

## Variation axes (pick one value each = the artistic intention)
1. **Shot distance**: extreme close-up / close / mid / wide / aerial.
2. **Camera angle**: eye-level / low / high / top-down / profile.
3. **Focal hero + subordination lever** (scale / sharpness / color-isolation / negative-space) — exactly 1 hero.
4. **Density**: ≤3 element-types; richness = one element's texture, not element count.
5. **Compositional device (exactly ONE = the "idea")**: mirroring / scale-tension / leading-line /
   juxtaposition / framing / negative-space / motion-echo.
6. **Mood**: witty / tender / sublime / melancholy / kinetic.
7. **Light**: golden / clean-midday / dusk / overcast / night.
8. **Finish (shot-dependent)**: crisp for close-ups / organic hero; matte-grain-painterly for wide / cosmic.
   (Phase-1 A/B candidate, not locked.)

## Subject pool (open / flag-able)
- **Base**: house, plants (cacti / lone tree / shrubs), animals, figures, geometric structures, terrain forms.
- **Topical/event**: e.g. soccer during the World Cup (per occasion).
- **Candidate motifs** (decide per batch): cosmic/space, sea/waves.

## Batch diversity sampler (forced — guarantees variety)
- Shot-distance quota: **≤2 wide per 6, ≥1 close-up**.
- Compositional **device unique per prompt** within a batch.
- Rotate **hero category** (animal / figure / object / phenomenon) and **mode** (landscape ↔ subject) across the batch.
- Pair **mood → device → light** coherently (small preset table), not random.
- Reject-and-resample any prompt that trips an anti-pattern.

## Anti-patterns (auto-reject)
- >3 element-types / element-listing.
- Default-wide over the quota.
- Heroless scene ("a person between them").
- Idea-less inventory (no device).
- Style/medium words in the prompt (moodboard owns style) — but **finish cues** (grain/blur/matte) are allowed.
- "Pleasant wallpaper" (no hero, no idea, no tension).

## Output format
- N prompts, ~30–40 words (soft cap), **color left to the moodboard**.
- Each prompt tagged with its **mode · device · shot** (for curation).
- For a photoreal-hero prompt, append: *"anchor realism with a real photo of <subject> as image prompt
  (`--iw ~2`) or `--oref`."*

## Constraints / unknowns
- ~40-word cap is a **soft V7-era heuristic**; V8.1 is now default.
- Finish axis is an **A/B candidate**, not locked (the blend is still a hypothesis pre-full-Phase-1).
- The skill produces prompts only; the moodboard and `--s` are set in MJ.
