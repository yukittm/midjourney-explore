---
updated: 2026-06-24
status: active
type: guide
---

# icon-pfp — standalone menu (NOT the core style)

> **Scope guard.** This is a **separate, one-off deliverable track** for profile-picture / icon
> artifacts. Its tuned parameters are **LOCAL to this menu** and must **NOT** be generalized into the
> core style recipe (`docs/style/prompting.md`, `docs/style/style-definition.md`). The core style stays
> the **photoreal-color-wave** recipe; this menu is a flat-graphic departure. Keep the two distinct.

## Purpose
Circular, profile-picture-ready graphics built from the project's color-wave palette — an **abstract
wave pattern filling a perfect circle on pure white**. (No photoreal subject, no theme.)

## Adopted recipe (V1 — abstract wave circle)
Run **from-scratch**: set the `--sref` image in the UI, **Remix / image-prompt slot empty**.

```
an abstract pattern of smooth flowing wavy color bands completely filling a perfect circle, bold undulating waves of emerald, crimson, soft pink and cobalt, purely abstract with no subject, clean circular edge, filled edge to edge, flat graphic, centered, pure white background only outside the circle --s 110 --sw 150 --ar 4:5 --no 3d render, cgi, photorealistic, photograph, face, portrait, figure, shadow, sphere, text
```

Tuning knobs: wave coarseness `bold` ↔ `fine`; restrict the palette to 2 colors for a cleaner read.

## LOCAL param deltas vs the core recipe (why this is a separate track)
| Param | Core (photoreal) | This menu (flat graphic) |
|---|---|---|
| `--style raw` | on | **dropped** (raw fights flat 2D) |
| `--no` list | `painting, illustration, 3d render, cgi` | **`painting/illustration` removed** (we want graphic), **add `face, portrait, figure, sphere, shadow, text`** |
| `--sw` | 150–250 | **~150** (lower so the white-outside / flat fill holds) |
| fill | scene with depth | **flat, edge-to-edge inside a clean circle; white only outside** |

## Key finding — SREF choice dominates the output
The **specific `--sref` image picked** changes the result **a lot** (clean wave bands vs noisy glitch).
**Record the exact sref used** for any adopted icon so it can be reproduced.

## Exploration log (how we got here)
1. Matte/glass **color sphere** containing the waves → user wanted no gloss, then no 3D.
2. **Flat color circle** filled with waves (white only outside).
3. **Minimal line-art circle** with white knockout *inside* → then reversed to **full fill, no inside white**.
4. **Face via color blocks / pareidolia / optical-illusion** → MJ drew explicit faces (rejected) or lost the face; **face theme abandoned**.
5. **No-theme abstract wave circle** → **adopted (V1)**.
