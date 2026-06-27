---
name: mj-sref-reliability-failure-modes
description: Reliability of the style-in-sref + subject-in-text workflow — failure modes (leakage, washout, non-transfer), the brand-consistency test, V8 sv7 style-over-subject tradeoff, --p training thresholds
metadata:
  type: reference
---

Web-verified 2026-06-26 (docs.midjourney 403 → search snippets; everestx, qwe.edu.pl, midlibrary, geekycuriosity, chasejarvis, blakecrosley fetched). Builds on [[mj-sref-image-url-behavior]], [[mj-stylize-chaos-hd-params]], [[mj-sv-style-reference-version]].

**The workflow IS broadly viable but NOT fully reliable — it degrades probabilistically, so batch-then-curate is mandatory.** No source claims sref deterministically separates style from subject. Pro consensus (Chase Jarvis): sref "steals the aesthetic without the content" AND "they also bleed style ... the sref tends to dominate ... use --sw to moderate it."

**FAILURE MODES (named, sourced):**
1. **Subject leakage** — sref pulls facial features/clothing/props/hairstyle from the ref into output. Worst when ref is an iconic close-up portrait with few elements; environmental/scene refs leak less. June 16 2025 rewrite "much less likely" but "better, not perfect" (qwe.edu.pl). midlibrary: "--sref might also incorporate the original subject ... unless the subject is specifically defined in the prompt."
2. **Style non-transfer** — if the loved aspect is a subtle detail (brushstroke, gradient), MJ may not prioritize it; it transfers only what IT deems salient (color/broad-comp/lighting). (qwe.edu.pl)
3. **Style washout at high stylize** — high --s and high --exp COMPETE with the reference; raise reference weight to compensate (official Omni doc principle, applies to sref). Fix when 12 outputs look random: "Lower stylize or raise --sw" (everestx).
4. **Style overpowering subject (V8 sv7-specific)** — geekycuriosity V8-alpha test: "With --sv 7 ... the style takes priority over the subject"; sv6 keeps subject prominent. So on the current V8.1 default (sv7) the named subject can get demoted to background — a NEW reliability risk vs V7-era sv6.
5. **--sw nonlinearity image vs code** — "--sw 150 applied to an image might be subtle. The same value on a code might obliterate your prompt" (search snippet of docs/guides). Codes far more aggressive per unit --sw.

**RELIABILITY TACTICS (sourced):**
- **Brand-consistency test (everestx):** generate 3 different subjects (product, person, workspace) × 4 each = 12 images, same sref+--sw+stylize, lay side by side. Pass = "one photographer on one campaign." Fail (12 random) = ref too weak OR subject prompts dominating → lower stylize / raise --sw.
- **--sw bands (blakecrosley):** 0–50 subtle · 50–150 balanced · 150–300 strong match · 300–1000 dominant. Community sweet spot 65–175 (qwe/prompt-architects). Brand work: 100–200 (everestx). To CUT leakage: drop to 50–70 (images) / 60–80 (codes).
- **Subject-first phrasing:** "describe what you want to SEE, not how to modify the reference." Good: "a golden retriever sitting in a meadow at sunset." Bad: "a dog in the style of this image but more painterly." V7+ weights early tokens heavily → lead with the subject (qwe, prompt-architects).
- **Codes > image URLs for consistency** — codes reference a fixed style vector; image URLs are re-interpreted per job and depend on image quality (blurry/cluttered = inconsistent). Production standard: build a 10–20 code library. (everestx, search snippets). Caveat: codes only work on --sv 4 / --sv 6; image-URL srefs work on all sv versions incl sv7.
- **Niji 7 has best sref fidelity / least style drift** even for non-anime if transfer is critical (blakecrosley).

**Personalization (--p):** captures color/lighting/framing/realism/mood/composition/subject-focus from YOUR ranked images. Needs ≥40 ranked to activate, ≥200 for CONSISTENT/reliable style (official-adjacent, qwe + medium catalog). Intensity rides on --stylize (0–1000, def 100): raise to 400+ if too subtle, drop to ~50 if it overpowers subject. Stacks with --sref (weightable: `--p code::2`, `--sref 123::2`). So --p is the more reliable long-term style anchor than a one-off image-URL sref, but only AFTER heavy training investment.

**sv default reconciliation:** docs say "--sv 6 is default" for **V7**; the V8/V8.1 default is **--sv 7** (4x faster/cheaper, supports --hd/--p/--stylize/--exp). Both true for their model era. See [[mj-sv-style-reference-version]].
