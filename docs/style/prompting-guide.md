---
updated: 2026-06-21
status: active
type: guide
---

# Prompting Guide (Midjourney, moodboard workflow)

Consolidated prompt craft for this project. Pairs with [[idea-bank]] (concepts), [[world-views]]
(directions), [[style-definition]] (the blend), and research files 01/05/06.

## 1. Anatomy (with a moodboard attached)

```
[shot/angle] , [subject + attributes + action] , [setting specifics] , [light] , (color)   --params
```

- Specify **subject / scene / light / (color)**; **do NOT write style/medium** — the moodboard supplies
  aesthetic. Style words fight the moodboard and muddy it.
- Front-load the load-bearing words; keep under ~40 words (later words lose effect).
- Parameters go at the end; no commas inside a parameter block.

## 2. The specificity dial (match detail to intent)

| Mode | Goal | Detail | Why |
|---|---|---|---|
| **Lock / reproduce** | a specific look, consistency | **high** | kill degrees of freedom → outputs converge |
| **Explore / ideate** | find new images & directions | **looser** | room = variety & serendipity; over-specifying kills discovery |

Currently converging a consistent style → lean high. When hunting new world-views → loosen.

**Project convention**: default to the **detailed end of the ~30–40-word envelope** — richly specify
subject + composition + light, while *style stays on the moodboard*. This is the default for
**production / locking a look**; **exploration & sweep work loosens** per the dial above (and most
current activity is still divergence — see [[style-definition]] Phase status, [[sref-sweep]]). The
research agrees on direction: "go easy on detailed prompts — focus on describing the subject and the
scene instead of the art style" (research `06` Q1), and its worked examples are ~22 detailed-subject
words (research `04` §4.1). The ~40 is a **soft V7-era heuristic** (non-official), not a hard cap; the
research bundle's "~30 words" floor is left frozen as recorded external best-practice.

## 3. Slots that narrow the SUBJECT (swap vague → concrete)

who/what + attributes (`a woman in a long red coat` not `a figure`) · count (fewer = more coherent) ·
action/pose · setting specifics (`a cracked white salt flat` not `a landscape`) · time/light · framing
(`high-angle wide shot`). Specify the **few key elements richly**; MJ can't honor many-element micro-layout.

## 4. Always-on rules

- ≤ ~40 words; front-load.
- Don't stack redundant adjectives ("soft moody cinematic ethereal" → averages to bland).
- One `--no` flag, comma-separated.
- With a moodboard: detail the subject, not the style.

## 5. Style strength vs fidelity (key knob)

- **Stylization (`--s`)**: low (~50) = literal/prompt-faithful; high (250–1000) = moodboard/MJ aesthetic
  dominates and **overrides prompt detail**. For reproduction/fidelity, **lower `--s`**. (Observed: `--s 400`
  turned a specified tennis court into a generic red plain; dropping toward 50 restores the literal court.)
- **Variety / chaos (`--c`)**: 0 for consistency/reproduction; 15–30 to spread the 4-grid while exploring.
- **`--style raw`**: more literal/photographic (good when reproducing a real-photo look); softens the
  painterly/dreamy blend — A/B it.
- **`--seed`**: lock to iterate in the same direction.

## 6. Exact reproduction of a specific image

Text can only *approximate*. To copy composition/content of a real reference, use the image itself as an
**image prompt** (`--iw`, e.g. `--iw 2`) — far more faithful than words. The moodboard averages many
images; an image prompt targets one.

## 7. Efficiency — per-lane templates

Don't write from scratch. Keep a base template per world-view/lane (the §1 slots pre-filled for that
world) and just swap the subject. High detail, fast, consistent.
