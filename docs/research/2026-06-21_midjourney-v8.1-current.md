---
updated: 2026-06-23
status: active
type: research
version-target: Midjourney V8.1 (current default since 2026-06-10/11)
supersedes: ../../archive/2026-05-11_midjourney-prompt-best-practices/ (V7-era — moved to /archive/)
sourcing-note: >
  Synthesized from a 4-agent web-research pass + a 4-agent web-verified cross-review (2026-06-21).
  Sources: updates.midjourney.com (authoritative) + multiple 2026 community guides. docs.midjourney.com
  returns HTTP 403 to automated fetch, so exact defaults are corroborated via update posts + guides and
  flagged "verify in-app". Confidence per claim.
---

# Midjourney V8.1 — Current Reference (the project's core problem)

**This is the CURRENT research doc.** The V7-era bundle was moved to
`../../archive/2026-05-11_midjourney-prompt-best-practices/` — use it only for history/sourcing.

## 0. Model era
- **V8.1 = current default (announced 2026-06-10/11).** No newer model as of 2026-06. V8.0 alpha 2026-03-17 (unconfirmed day), V8.1 alpha 2026-04-30. *(High)*
- **V8.1's headline feature = HD by default** + a more **literal/neutral base** render than V7 (so `--style raw` is *less load-bearing* than on V7, but still the realism lever). *(High)*
- **Realism is GLOBAL in V8.1** — `--style raw`/`--s` apply to the *whole* frame; there is **no per-region control**. `::` sets concept *emphasis/weight*, NOT spatial placement, and there is no ControlNet analogue. So a photoreal foreground + a truly painterly/abstract background can't be forced in one pass — use §8 (the bridge). *(High)*

## 1. Core problem & fix — realism and color are INDEPENDENT channels

Our failing stack = **moodboard + no raw + high `--s`** → muted + painterly. Three stacking causes:
1. **Moodboards AVERAGE their images** → multiple hues regress to a muted centre; built for brand *range*, not for reproducing one bold reference (so they **mute** a bold palette). (They default to `--sv 7` like image srefs; whether `--sw` weights a moodboard is **unverified** — the earlier "`--sv` doesn't apply to moodboards" claim was wrong.) *(High on the averaging/muting; sv7-default High)*
2. **`--s` (stylize) with a moodboard/profile = "how strongly to apply that (averaged, muted) style"** + adds painterly flair off the same dial → raising it to 1000 made output *more* muted+painterly. `--s` is **not** a realism or saturation knob. *(High — matches our in-app test)*
3. **No `--style raw`** → MJ's default aesthetic. *(High)*

**The fix — two separate channels:**
- **Realism** = `--style raw` (ON) + **LOW `--s` (~50–150)** + photographic cues (camera/lens, film stock, `natural skin texture, editorial photograph`; avoid `hyper-realistic`) + `--no painting, illustration, 3d render, cgi`.
- **Color** = an explicitly-weighted **`--sref`** (preferably your own bold image as a URL) — NOT the averaging moodboard. Plus explicit hue words + colored lighting.
- **Key insight**: raw mutes *automatic* color, not specified color. **Raw + explicitly specified saturated color = vivid AND photographic.** *(High)*

## 2. Parameter reference (V8.1 — verify exact numbers in-app)

| Param | V8.1 value | Notes / confidence |
|---|---|---|
| `--stylize`/`--s` | 0–1000, default 100 | Photoreal wants ~50–150. With a profile/moodboard, high = apply more of that style (not realism). *(High dir)* |
| `--style raw` (Raw toggle) | on/off | Strips painterly bias → photographic; works with moodboard/sref; less dramatic on V8.1. *(High)* |
| `--hd` / `--sd` | HD = native **2048²** (**cannot be upscaled further**); SD = 1024² → upscale to 2048² | HD-by-default is V8.1's headline. For IG: HD, or SD + Subtle upscale. *(High / verify exact)* |
| `--sref <URL>` / `--sref <code>` | — | Carries **color/light/contrast/texture/composition, NOT subject**. URL = your image's style (preferred). V8.1 sref is higher-fidelity than V7. *(High)* |
| `--sw` (style weight) | 0–1000, default 100 | Documented bands: **0–50 subtle / 50–150 balanced / 150–300 strong / 300+ dominant**. Our recipes use **~150–250** (strong→push); R3 sits at 220–250. No documented `--hd` interaction. *(range/default High; exact bands = tuned heuristics, Med)* |
| `--sv` (sref version) | 6 / 7 (V8 family) | **`--sv 7` is the V8.1 DEFAULT** for image srefs AND moodboards, and is **`--hd`-compatible** (4× faster/cheaper than the old version). **For an IMAGE-URL `--sref` (our path): OMIT `--sv`** → it defaults to sv7 (the desired behavior). **Numeric/random CODES need `--sv 4` (legacy) or `--sv 6` — NOT sv7.** ⚠️ In-app (2026-06-23) writing `--sv 7` **explicitly** with `--version 8.1` threw "Unsupported Style Reference version 7" — likely an sv7×numeric-code / explicit-write quirk; the safe action is simply **don't write `--sv`** (the default is already sv7). *(sv7-default + hd-compat: High; exact error trigger: Med)* |
| `--oref` / `--ow` | ow 0–1000, default 100 | **V7-only — using it FORCES the job onto V7** (forfeits V8.1 realism). No V8-native omni yet ("improved version in training"). Identity-lock only. `--ow 400–600` strong face; 25–75 lets scene dominate. *(High)* |
| `--iw` (image weight) | **0–3, default 1** | Image-prompt strength (corrected: NOT 0–2). *(High)* |
| `--exp` | 0–100, integers, default 0 | A **2nd dimension to `--stylize`** — pushes detail/creativity at the expense of prompt accuracy. **>25 can overpower `--s`/`--p`** (keep ≤25 when combined). On V8.1. *(High)* |
| `--p` (moodboard / personalization) | code | Broad/averaged taste. **Moodboards default to `--sv 7`** (so `--sv` DOES apply); whether `--sw` weights a moodboard is **unverified**. Trained personalization is the consistency layer. *(sv7-default High; --sw-on-moodboard unverified)* |
| `--cref` | — | **V6 / Niji-V6 only** (superseded by `--oref` on V7; not on V8.1). `--cw` 0–100. *(High)* |
| `--q` (quality) | — | **Unsupported on V8.1** (HD/SD replaces it); `--q 2`/`--q 4` workflows require V7. *(High)* |
| `--c` (chaos) | 0–100, default 0 | Grid variety. `--ar` any (4:5 for IG). *(High)* |

## 3. Recommended workflow

### A. One-prompt recipe — bold color + photoreal (use an IMAGE-URL sref; sidesteps code/sv issues)
```
[surreal natural scene + subject], natural texture, editorial photograph, 85mm f/1.8,
Cinestill 800T, bold saturated color-blocking
--style raw --s 110 --sref <YOUR bold giz image URL> --sw 200 --ar 4:5
--no painting, illustration, 3d render, cgi
```
- **For an IMAGE-URL `--sref` (our path): OMIT `--sv`** → it defaults to **sv7** (the V8.1 default, `--hd`-compatible). Don't write `--sv 7` explicitly (it errored in-app — see §2). **Numeric/random CODES** need `--sv 4` (legacy) or `--sv 6`, not sv7.
- Film-stock keyword is high-leverage: `Cinestill 800T` (saturated+photographic), `Kodak Portra 400` (skin).
- Color via *light* (neon/gels/golden hour) reads physically-plausible, not painterly.

### B. Reference-matching (reproduce one look)
`/describe` the reference → harvest tokens → `/shorten`; lock with `--sref <image URL>` `--sw 150–250`
(lower than §A's color-push — here we *match*, not amplify); `--style raw` `--s ~100`; `--seed` to repeat.

### C. Consistent **personal** style (best fit for THIS project's goal)
For a stable house look across many images (not one-off matching), prefer V8-native reproducibility:
- **`/tune` Style Tuner → a custom `--style <code>`**: build a code from image-pair picks; encodes *your*
  aesthetic. Portable, but **subject-fragile** (carries bias from its training prompt) — a domain accent,
  not a global base lock (see the reproducibility ranking below).
- **Personalization profile (`--p`)** *trained* via the like/dislike loop = the platform's intended
  mechanism for a stable personal look (distinct from the averaging-moodboard misuse in §1).
- **Image-URL sref** of our own bold reference = exact palette; on V8.1 use it as the Style Reference with **no `--sv`** (the model default applies).
- **Post-grade as a PRIMARY, deterministic color lever**: a saved Lightroom/Capture One preset (or a LUT in
  `automation/`) gives the *exact* editorial color reproducibly — MJ color sampling is not deterministic.
- **Reproducibility ranking** (most→least deterministic, for a cross-*subject* house look): post-grade
  LUT/preset (exact) > trained `--p` profile (taste, prompt-agnostic) > image-URL `--sref` (palette) >
  `--seed` (same prompt+seed+model only — does NOT transfer across prompts). *(High dir)*
- **Programmatic access / Editor internals** (drives the automation **one-pass-only** constraint): see
  `.claude/agent-memory/researcher/reference_mj-api-automation-state.md` — no official MJ API; the V8.1 web
  Editor/inpaint runs on the **V6.1 model**; Discord Vary Region unavailable on V8.1; unofficial wrappers =
  ToS risk. *(High)*

### HD / upscale
HD jobs are already 2048² (don't upscale). For SD, use **Subtle** (Creative/Magnific hallucinate & drift).

### A/B
Sweep `--s` 60/110/200 and `--sw` 120/180/250 → the crossing of "subject photoreal × color vivid". (Keep `--sw` in the reliable band; only test 300+ if color is still weak.)

## 4. Sref sourcing
- **Best for our palette**: upload one **bold giz reference image** into MJ → set it as **Style Reference**
  (= `--sref <that image>`). Exact palette, no purchase; **no `--sv` needed** on V8.1 (defaults to sv7). Image-URL srefs work with the default sv7; only numeric codes are version-restricted (sv4/sv6).
- **Free code galleries**: SrefHunt, Midlibrary, srefs.co, sref-midjourney.com, Lummi (all live).
- **Paid**: giz.akdag's packs (lemonsqueezy, 400+ codes incl. Photorealism) — **V7/V6.1-targeted**; expect drift on V8.1 (pin `--sv 6`).
- **giz's method = blending 2–3 sref codes**; she does not publish her stylize/raw/post values. Mariano Peccinetti is NOT a sref token (collage artist; Photoshop rework).

## 5. Carry-forward grammar (version-independent — promoted from the V7 archive)
- **`--no`**: ONE flag, comma-list (`--no a, b, c`). Each word parsed independently — `--no modern clothing` = "no modern" + "no clothing" (moderation trap). ≈ a −0.5 weight.
- **`::` weights**: `concept_a::2 concept_b` (no space before `::`). Total weight must stay positive.
- **`--seed N`**: same seed+prompt+model → repeatable. **Token economy**: ~74-token cap; words past **~40 lose influence** — front-load; with a moodboard/sref keep the text spent on subject (style on the ref).
- **Over-styling antidotes** (our core problem): add `--style raw`; lower `--s`; specify film/grain; don't stack adjectives.

## 6. Delta vs the archived V7 research
- `--oref`/`--cref` = V7-only (drop you off V8.1). **Default sref version = `--sv 7`** (V8 family); `--sv 4`/`--sv 6` are for legacy numeric codes. `--sref` fidelity better on V8.1. `--style raw` still valid, less load-bearing. **HD-by-default + `--exp` are new.** The V7 bundle's parameter specifics are otherwise superseded by this doc; its prompt *grammar* (§5) and over-styling pitfalls are carried forward here.

## 7. Confidence & caveats
- **High**: three-cause diagnosis + two-channel fix; raw+low-`--s` for realism; sref(image-URL)+`--sw` for color; **realism is global (no per-region; `::`=emphasis)**; oref forces V7; old codes drift; `--iw 0–3`; HD-by-default; **`--sv 7` = the V8.1 DEFAULT for image srefs/moodboards & is `--hd`-compatible — for an image-URL sref just OMIT `--sv` (numeric codes need sv4/sv6; writing `--sv 7` explicitly errored in-app)**; trained `--p`+post-grade as the consistency path (ranking: post-grade > `--p` > image-sref > seed); **no official MJ API (web Editor runs on V6.1)**; giz blending / Mariano not a token.
- **Medium / verify in-app**: exact `--s`/`--sw` bands; the precise trigger of the explicit-`--sv 7` in-app error; whether `--sw` weights a moodboard; **exact V8.1 `--iw` max** (0–3 well-sourced for V7; the V8.1 number is on the 403-blocked page); `--hd` exact behavior; the **bridge breakpoint** (how far toward pure abstraction grounding-in-a-real-phenomenon holds before the photoreal foreground breaks). *(Resolved 2026-06-23: no V8-native omni / no V8-native editor / no official API — all confirmed still absent.)*
- The V7-era MJ-automation idea formerly bundled here was relocated to `automation/` (it is an internal plan, not external research), keeping `docs/research/` external-only.

## 8. The real-phenomenon bridge (general technique)

Because realism is global (§0), you cannot mix a photoreal subject with a painterly/abstract background in one pass. The workaround: **name the background as a real, drone-photographable phenomenon** and let `--style raw` + low `--s` render it *photographically* — the composition still reads abstract, but every pixel is a photo, so a photoreal figure survives in the same pass. Real flowing/blocked-color phenomena to name: multicolor crop/tulip bands, painted-desert / Zhangye Danxia mineral strata, contour-plowed or terraced fields, salt-evaporation ponds, aerial color bands of farmland/coastline.

**Breakpoint:** if a human could photograph it from a drone → one MJ pass; if it's pure paint/gradient with no physical referent → it needs a 2-step composite. Same principle as §1's *"raw mutes automatic color, not specified color."* *(Med — validated in-app 2026-06-23; the project adopts it as registers R1–R3 in `docs/style/`.)*
