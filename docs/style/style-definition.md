---
updated: 2026-06-21
status: draft
type: style
---

# Style Definition — SSoT (WORKING DRAFT / hypothesis)

> Status: **hypothesis, not yet validated by generation** (MJ plan expired as of 2026-06-18).
> This is the anchor to steer exploration, NOT a fixed conclusion — the real style emerges from
> Phase 1 generations and gets revised here. See [[sref-sweep]], [[reference-accounts]].

## Two axes (the user's framing, 2026-06-18)

"My style" = two independent decisions, which map **1:1 onto Midjourney's content/style split**:

| Axis | what it is | MJ lever | Status |
|---|---|---|---|
| **A. Reference taste** | how it looks (aesthetic / style) | `--sref` / moodboard | direction decided → blend (below) |
| **B. Subject world** | what is depicted | the text **prompt** | **TO DECIDE** (see end) |

Independent levers: hold the taste fixed and vary subjects, or vice versa — also how we run
experiments. A coherent creator-style holds **both** consistent.

## Axis A — Reference taste: blend (decided 2026-06-18)

**Blend** of the two reference accounts — keep their shared axis, mix their differing registers.

- **Shared axis (the spine)**: AI-driven **surreal / conceptual** imagery with single-or-few figures,
  scale-play, poster-like editorial composition, "visual poetry" concepts.
- **Take from `giz.akdag`**: bold **color-blocking** confidence, clean daylight, contemporary
  fashion-forward subjects, wit.
- **Take from `marianopeccinetti`**: **retro / grainy matte film texture**, cosmic & natural
  dreamscape motifs, faded nostalgic undertone, collage juxtaposition.

## Working style hypothesis (one sentence)

> Contemporary surreal-editorial figures with **bold color-blocking and strong concepts**, rendered
> with a **retro, grainy film-collage finish** and dreamlike cosmic/natural staging.

Attribute targets to test:
- **Palette**: confident color-blocking (giz) BUT slightly faded/print-toned (Mariano) — saturated yet nostalgic.
- **Light**: clean daylight, but matte/soft rather than glossy.
- **Texture/finish**: visible film grain, paper/collage matte — NOT clean digital gloss.
- **Subject**: a clear hero figure or object in a surreal, concept-driven scene.
- **Composition**: graphic, poster-like, scale-play.
- **Mood**: witty-but-poetic; optimistic surrealism with a nostalgic edge.

## How to realize the blend in Midjourney (technique map)

The "blend" maps to concrete MJ levers (see research 03/05):

1. **Two-sref blend with weights** (sref honors `::` weights; moodboard does not):
   `[probe] --sref <crisp-editorial-code>::2 <retro-film-code>::1 --v 7 --ar 4:5`
   Tune the ratio to slide between giz-crisp and Mariano-retro.
2. **Moodboard mixing both registers**: curate a single moodboard with images from BOTH accounts +
   our own picks; tune dominance via `--s` (more retro images → more retro average). Updatable, "ours".
3. **Grain/finish cues in the prompt** to push the retro finish: e.g. "35mm film grain, matte print"
   — and decide `--style raw` per test (raw = literal photo; off = painterly — the collage look may
   actually want the painterly default dialed via `--s`, TBD by experiment).

> ⚠️ Which lever wins is an empirical question — resolve by running Phase 1, not by assertion.

## Originality stance

Use others' published sref codes + their images as **inputs / learning**, but **converge on our own
curated moodboard** (or our own derived sref) so the final style is ours, not a borrowed fingerprint.

## Reference material in hand

- **Imported reference pool** in `../../references/` (self-contained to this project): 18 `giz.akdag`
  + 7 `marianopeccinetti` images + 5 videos; provenance in `references/manifest.jsonl`. This is the
  **moodboard-build input** for the blend.
- **giz.akdag SREF codes — NOT harvested** (decided 2026-06-20): the "SREF Collection" highlight
  slides are videos (unreadable via capture) and the codes appear to be a **paid product** on her
  Contra. Route: build the blend from the imported image pool (moodboard), not by borrowing her
  codes. For the optional two-sref technique, use community/random codes instead.

## Exploration plan

| Phase | Action | Needs MJ plan? |
|---|---|---|
| 0 prep | Collect candidate references (both accounts + pool) + giz's published sref codes into the sweep table | No — can do now |
| 1 diverge | Fixed probe prompts × {two-sref blends, moodboard, image-srefs}; collect keepers | Yes |
| 2 characterize | Update the hypothesis above from what actually resonated | Yes (after 1) |
| 3 converge | Lock the blend as a curated moodboard (or a chosen sref pair) | Yes |
| 4 validate | Run across varied subjects; feed good outputs back into the moodboard | Yes |

## Axis B — Subject world (TO DECIDE)

What you choose to depict — the recurring subjects/themes that make the body of work coherent and
recognizably yours. This is the **prompt side**, a personal/creative choice, and it also defines what
the Instagram account is "about".

**Prompt convention (this project's prompt side)**: default to **detailed/specific** prompts — richly
specify subject + composition + light (the detailed end of the ~30–40-word envelope; style stays on the
moodboard). Default for production/lock; loosen for exploration. See [[prompting-guide]].

Each reference account pairs a taste WITH a subject world:
- `giz.akdag`: fashion-forward figures in witty surreal scenarios.
- `marianopeccinetti`: cosmic & natural dreamscapes, few/no figures.

Candidate subject directions to react to (not exhaustive):
- People / portraits / fashion figures
- Still-life & objects (sculptural, product-like)
- Landscapes / nature / cosmic
- Architecture / interiors / urban
- Surreal conceptual scenes (figure + object juxtaposition)
- Food / everyday objects

→ Decision: pick **1–2 subject worlds** to start. Can brainstorm if helpful. This + Axis A together
become the locked style.
