---
name: mj-reusable-style-kernel-recipe
description: The "style kernel / reusable recipe" approach (fixed phrases+params+sref pasted into every prompt, swap only subject) IS a well-established, widely-published MJ practice — official tooling + community guides
metadata:
  type: reference
---

The reusable "style kernel / base prompt / style block" approach the project is building toward is NOT idiosyncratic — it is the mainstream, widely-published MJ workflow (2023-2026). Cited sources:

## Canonical structural concept (anchor)
- **PREFIX / SCENE / SUFFIX anatomy** (Tristan Wolff "Midjourney Cheat Sheet V5", medium.com/design-bootcamp/the-midjourney-cheat-sheet-v5-54b5fd92d2da, 2023-04-11): `/imagine prompt: [PREFIX] [SCENE] [SUFFIX] [Parameters]`. PREFIX = "defines image medium & style", SCENE = "defines content", SUFFIX = "modulates Prefix & Scene". PREFIX+SUFFIX = the FIXED reusable style anchors; SCENE = the variable subject. This is the exact kernel idea, named in 2023.
- **Bold/italic copy-paste template** (Chris Ellinas "Ultimate MJ Cheat Sheet", same Medium pub): italic = subject you replace, BOLD = fixed style block copied as-is.

## Concrete reusable base-recipe examples (verbatim, cited)
- **TheDevDesigns "3-Layer Consistency Framework"** (medium.com/@theDevDesigns/...-lock-it-in-08c99f5bc38d, 2025-10-20) — cleanest `{subject}`-slot scaffold: `/imagine prompt: {subject}, cinematic {lighting}, {texture}, shot on {lens}, {backdrop}, high detail, clean composition --seed {your_seed} --ar 4:5 --sref {url_of_your_hero_image}`. Keep seed constant; swap only subject + slot fillers.
- **blakecrosley V8.1 guide** (blakecrosley.com/guides/midjourney) reusable base template: `[Shot type] by [Director], [subject], [action/pose], [costume/styling], [setting], captured with [Camera] using [Lens], [lighting], [mood] --ar [ratio] --s [value] --p`.
- **EverestX sref playbook** (everestx.com/tutorials/midjourney/midjourney-style-references-sref-codes, V7 era): "Treat reference URLs/codes as a non-negotiable part of your prompt template, not a bonus" + documented per-mode fragment "Hero editorial: --sref 3847291056 --sw 150 --stylize 100" + "Build a personal 'style code library' — 10-20 codes... This is the production AI image team standard."

## Official Midjourney tooling for fixed style blocks
- **/prefer suffix** (docs.midjourney.com/docs/settings-and-presets — 403 to fetch but quoted widely; torybarber.com/midjourney-preferences 2025-02-12): auto-appends saved text+params to the END of EVERY prompt. The native "fixed kernel" feature.
- **/prefer option set**: store named reusable strings (params/URLs/srefs) to call per-prompt.
- **Personalization --p** (docs Personalization article): portable profile code, "everyone's working from the same aesthetic baseline"; V7 profiles compatible with V8.1 (default since 2026-06-11).
- **--sref numeric codes** more consistent than image URLs (reference fixed style vector); "use that number in a hundred different prompts."

## Tooling / prompt-builder side
- HoppyCat prompt-pack (github.com/HoppyCat/prompt-pack) Google Sheet, copy-paste tabs; Prompter Guide (prompterguide.com); PromptFolder saves prompts + style presets.

KEY TAKEAWAY for the project: a fixed style block + fixed params + sref reused across prompts with only the subject swapped is textbook MJ practice with both official tooling support and a deep community-guide tradition. Recommend implementing via /prefer suffix (Discord) or a saved snippet, anchored on the project's sref + raw + low-s realism kernel.
