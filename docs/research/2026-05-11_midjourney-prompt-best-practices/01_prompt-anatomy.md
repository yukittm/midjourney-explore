---
date: 2026-05-11
status: draft-v1
version-target: Midjourney v7 (default as of May 2026), v6.1 fallback
spec-block: as of 2026-05
source-urls:
  - https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics
  - https://docs.midjourney.com/hc/en-us/articles/32658968492557-Multi-Prompts-Weights
  - https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw-Mode
  - https://aituts.com/midjourney-shorten/
---

# 01 — Prompt Anatomy

## 1.1 What a Midjourney prompt is

> "Your prompts can be simple — even a single word or emoji works. Short prompts let the default Midjourney style fill in the gaps, but if specific elements are important to you, you should include them. Fewer details mean more variety but you get less control over the outcome." — paraphrased from [Prompt Basics](https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics) (via WebSearch quoted snippet, 2026-05).

A prompt is interpreted as: **(optional image URL) → text description → parameters**. Parameters always go at the end, after a space, with no commas/periods inside parameter blocks. ([Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List))

## 1.2 The six descriptive axes (official)

Per [Prompt Basics](https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics), be clear about details that matter across these axes:

| Axis | Examples |
|---|---|
| **Subject** | person, animal, character, location, object |
| **Medium** | photo, painting, illustration, sculpture, doodle, tapestry |
| **Environment** | indoors, outdoors, on the moon, underwater, in the city |
| **Lighting** | soft, ambient, overcast, neon, studio lights |
| **Color** | vibrant, muted, bright, monochromatic, pastel, black and white |
| **Mood** | calm, energetic, melancholic, etc. |

For this project (editorial / fashion / surface / object still-life), **Medium + Lighting + Color** carry most of the aesthetic load when paired with a moodboard. Subject is the literal thing in frame. Environment and Mood are the modifiers.

## 1.3 Recommended structural template (this project)

```
[medium] of [subject], [environment/scene cue], [lighting cue], [color/mood cue], [optional camera/lens cue] --style raw --v 7 --ar X:Y --profile <moodboard-code>
```

Concrete example (editorial fashion):

```
editorial portrait of a woman in oversized wool coat, austere concrete interior, overcast window light, muted putty palette, shot on Canon RF 85mm f/1.2L --style raw --v 7 --ar 4:5 --profile r1bwkpa
```

**Why front-load**: words later in the prompt lose influence (see §1.6 Token economy).

## 1.4 Where parameters go

- All `--xxx` parameters at the **end**, separated by a space.
- **No commas, periods, or other punctuation inside parameter blocks.** ([Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List))
- Image prompts (URLs) go at the **start** of the prompt, before the text description. ([Image Prompts](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts))

```
https://ref.url/img.jpg [text prompt] --iw 1 --style raw --v 7 --ar 4:5
```

## 1.5 Multi-prompt `::` separator (advanced)

`::` separates the prompt into weighted concepts. Format: `concept_a::N concept_b::M` (no space before `::`, single space after).

> "If you prompt `space:: ship`, you're asking Midjourney to think about 'space' and 'ship' as distinct elements and then mix them together. … `space::2 ship` tells Midjourney that 'space' is twice as important as 'ship.'" ([Multi-Prompts & Weights](https://docs.midjourney.com/hc/en-us/articles/32658968492557-Multi-Prompts-Weights), via WebSearch snippet)

V4+, Niji 4+, V5/5.1/5.2, V6/6.1, V7 accept **decimal weights**. Negative weights work but the **total of all weights must remain positive**.

For this project, prefer plain natural-language descriptions over heavy `::` weighting — moodboard already drives the aesthetic. Use `::` only when two concepts visibly contradict in renders (e.g., `linen sculpture::2 industrial::1`).

## 1.6 Token economy (critical for this project)

> "Any tokens beyond the **74-token limit** are ignored by Midjourney. … The longer your prompt is, the more likely Midjourney is to assign a weight of 0.00 to important keywords, especially later on in the prompt. … Once you exceed a certain number of words, the influence of subsequent words on the final result becomes negligible, and **anything written after approximately 40 words has minimal impact**." — Midlibrary v6 in-depth review, Aituts /shorten guide (secondary sources, but consistent across multiple).

[Aituts /shorten guide](https://aituts.com/midjourney-shorten/) describes the official `/shorten` command (Discord) which returns Midjourney's actual token weighting and recommends a tightened prompt — a useful pre-flight when you want to know which words are being dropped.

> ⚠️ 推測: 74-token cap and 40-word drop-off are widely cited but I could not directly extract from official docs in this sandbox (403). They are present in multiple independent secondary sources. Treat as strong heuristic.

**Practical floor for this project:** keep the textual prompt under **30 words** when a moodboard is attached, since the moodboard absorbs aesthetic load. Reserve those 30 words for: medium, subject, scene cue, lighting cue, color/material cue, optional camera/lens cue.

## 1.7 Permutations `{a, b, c}` for batch testing

> "For example, a `{red, green} bird in the {jungle, desert}` will produce four prompts. … Permutations can also be applied to the weights of multiprompt segments, … `--ar {1:1, 2:3, 3:5}`." ([Permutations](https://docs.midjourney.com/hc/en-us/articles/32761322355597-Permutations), via WebSearch snippet)

Use case for this project: when a moodboard is new, batch-test crop ratios — `--ar {1:1, 4:5, 9:16}` — without running three separate prompts.

## 1.8 Discord vs. Web app surface

Both surfaces accept the same prompt grammar. Differences:

- **Web app (`alpha.midjourney.com` / `midjourney.com`)** has the visual moodboard / personalization UI, drag-and-drop image prompts, and Draft Mode toggle in the Imagine bar. ([V7 Alpha announcement](https://updates.midjourney.com/v7-alpha/))
- **Discord** still works via `/imagine`, but moodboard/personalization codes must be referenced by their `--profile` / `--p` alphanumeric on the prompt — there's no inline UI for picking them mid-prompt.

For this project's moodboard-driven workflow, the **web app is the operating surface**. Treat Discord as a secondary surface for quick `/imagine` retries.

## 1.9 Default behaviors that affect every prompt

- **V7 default-on Personalization**: requires ranking ~40 image pairs to unlock V7 at all. Once unlocked, V7 always applies the trained taste unless toggled off via the Personalization button. ([V7 Alpha](https://updates.midjourney.com/v7-alpha/))
- **`--stylize` default = 100** on a 0–1000 range. ([Stylize](https://docs.midjourney.com/hc/en-us/articles/32196176868109-Stylize))
- **`--chaos` default = 0** on a 0–100 range. ([Chaos / Variety](https://docs.midjourney.com/hc/en-us/articles/32099348346765-Chaos-Variety), via WebSearch snippet)
- **`--iw` default = 1** on a 0–3 range (V6/V7). ([Image Prompts](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts))
- **`--sw` default = 100** on a 0–1000 range.
- **`--cw` default = 100** on a 0–100 range (V6 only — `--cref` does not work in V7).
- **`--ow` default = 100** on a 1–1000 range (V7 omni-reference).

For editorial / fashion / surface work where moodboard does the heavy lifting, lock these to known values explicitly rather than relying on defaults — V7's auto-personalization makes "unspecified = default" non-deterministic across users.
