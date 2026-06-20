---
updated: 2026-06-20
status: active
type: guide
---

# Style Sweep — `--sref` discovery worksheet

Purpose: find a personal style by holding the **prompt constant** and varying the **aesthetic reference**.
This is the *divergence* stage. Output of this worksheet → a shortlist that feeds the *convergence*
stage (build a moodboard or lock a few sref codes) recorded in `style-definition.md`.

Reference: `../research/2026-05-11_midjourney-prompt-best-practices/` files 03 (mechanisms),
05 (pitfalls), 06 (moodboard semantics).

---

## 0. Pre-flight (do this first — otherwise the experiment is contaminated)

- [ ] **Personalization controlled.** V7 has Personalization **on by default**; your trained taste
      leaks into every render. For a clean sweep, **toggle Personalization OFF** (or set a single
      known moodboard as default). Otherwise you cannot tell whether a difference came from the
      `--sref` or from your profile. (research 05 §5.6, 03 §3.4)
- [ ] **Pin the version**: `--v 7` on every prompt (avoid silent drift to V8). For V6-era sref
      codes that look wrong under V7, append `--sv 4`. (research 02, 05 §5.5)
- [ ] **Confirm operating surface**: web app (`midjourney.com`) for the moodboard/personalization UI.

---

## 1. Probe prompts (held constant across the sweep)

Keep these short and neutral so the **sref** carries the aesthetic, not the words. One probe per lane
you care about. Edit these to match your intended subjects.

| ID | Lane | Probe prompt (text only — params added in §3) |
|----|------|----------------------------------------------|
| P1 | portrait | `editorial portrait of a person, plain interior, window light` |
| P2 | still-life | `still life of a single ceramic vessel on a plain surface, soft side light` |
| P3 | texture | `extreme close-up of a folded fabric surface, soft directional light` |

> Tip: same subject, varied sref → the differences you see ARE the style. Resist adding adjectives.

---

## 2. Candidate `--sref` codes

Collect codes to try. Community libraries: srefcodes.com, promptsref.com (research 03 §3.3).
Also try `--sref <your-own-image-URL>` for references you already love.

| Code / URL | Source | First impression | Lanes it suits | Keep? |
|------------|--------|------------------|----------------|-------|
|  |  |  |  | ☐ |
|  |  |  |  | ☐ |
|  |  |  |  | ☐ |

---

## 3. Sweep command patterns

**Single probe × single sref:**
```
[probe text] --sref <CODE> --style raw --v 7 --ar 4:5
```

**Batch one probe across several aspect ratios** (validate a code across IG slots):
```
[probe text] --sref <CODE> --style raw --v 7 --ar {1:1, 4:5, 9:16}
```

**Add grid variety** while judging a code (see the range it can produce):
```
[probe text] --sref <CODE> --style raw --v 7 --ar 4:5 --c 20
```

**Blend two codes with weights** (sref supports `::` weighting; moodboards do NOT):
```
[probe text] --sref <CODE_A>::3 <CODE_B>::1 --style raw --v 7 --ar 4:5
```

Record `--seed N` on anything you may want to regenerate.

---

## 4. Evaluation log

For each run worth keeping, save the output to `outputs/candidates/` and log it here.

| Date | Probe | sref code | seed | Output path | Verdict (keep / drop / why) |
|------|-------|-----------|------|-------------|------------------------------|
|  |  |  |  |  |  |

Judge for: does it read as *mine*? consistent across the 3 probes? believable (not generic-AI)?
distinct from the other candidates?

---

## 5. Convergence (next stage, when a shortlist exists)

1. Pick the 1–3 codes that consistently feel like "my style".
2. Decide the lock mechanism:
   - **Single look, indefinitely repeatable** → keep the `--sref` code(s).
   - **Evolving curated aesthetic** → build a **moodboard** from the kept outputs/references
     (research recommends moodboard as the production primary), register its snapshot code in
     `../../moodboards/`.
3. Write the result into `style-definition.md` (the SSoT): the aesthetic in words + the chosen
   codes + sample outputs.
