---
updated: 2026-06-23
status: draft
type: style
---

# Style Definition — SSoT

> Working SSoT for the project's own visual style. The model below was **validated in-app on 2026-06-23**
> (the realism kernel + the bridge produced on-style one-pass results; **R3 validated**, R1/R2 follow from
> the same kernel pending the Phase-1 test set) — it supersedes the earlier 2-dial framing: render is now
> **pinned to photoreal** for any real subject, and
> variation moves to the **background-register** axis. North star = near-full pipeline automation (below).
> Craft/how-to: [[prompting]]. Source analysis: [[reference-accounts]]. Current MJ mechanics:
> `../research/2026-06-21_midjourney-v8.1-current.md`.

## North star & operating mode

End goal = **near-full automation of the pipeline**: theme/prompt generation → Claude-driven Midjourney
operation (Claude-in-Chrome) → Instagram publishing. In that loop the **user is the creative director**
(reacts to themes + selects images — "this / that" only); **Claude autonomously generates the patterns and
combinations**. Selections are not just curation — they double as the like/dislike training signal for the
consistency stack.

**Currently in the observation / exploration phase — policy NOT locked.** The model below is the working
state, refined as generations validate; written so the *automatable* (one-pass) path stays explicit.

## Two axes (the grammar)

"My style" = two independent decisions, mapping onto Midjourney's content/style split:

| Axis | what it is | MJ lever |
|---|---|---|
| **A. Render + color** | how it looks | the realism **kernel** (`--style raw` + low `--s`) + a single bold image **`--sref`** (`--sw`, `--sv 7`) |
| **B. Subject world** | what is depicted | the text **prompt** |

Independent: hold the look fixed and vary subjects, or vice versa. **Correction vs. earlier drafts** — the
look is no longer set by an averaging **moodboard**, and color is **not** pushed with `--s`. A moodboard
averages its images toward a muted centre and can't be weighted; a single bold `--sref` carries the bold
palette and *can* be pushed via `--sw`. See Color channel + `../research/2026-06-21_midjourney-v8.1-current.md` §1.

## The foreground invariant (non-negotiable, all modes)

**Real subjects — people and animals — always render PHOTOREAL, never painterly.** Holds across every
register and mode; a **law, not a lean** (the earlier "content tendency" framing is superseded). The realism
**kernel** that enforces it:

- **`--style raw`** + **low `--s` (~90–120)** — the realism lever; keep `--s` low so the prompt + photographic
  cues dominate, not MJ's automatic aesthetic.
- **Photographic cues** in-prompt: a camera/lens (e.g. `85mm f/1.8`), a film stock (e.g. `Cinestill 800T`,
  `Kodak Portra 400`), and `editorial photograph, sharp realistic skin/texture`.
- **`--no painting, illustration, 3d render, cgi`** — one flag, comma-list.

Color is **not** part of the kernel — raw mutes *automatic* color, not *specified* color, so the bold palette
rides on the `--sref` + `--sw` channel. Raw + a bold sref = vivid AND photographic.

## Color channel

Color = **one bold IMAGE `--sref`** (a self-uploaded reference image), **not** the averaging moodboard.

- **`--sw ~150–250`** — the color-push knob; stay in band (`>300` washes out).
- **`--sv 7`** — image-ref sref version (numeric *codes* would pair with sv6/sv4 instead).
- **Push color via `--sw`, never `--s`.** Raising `--s` applies more of the (muted, averaged) style + painterly
  flair — it is not a saturation knob.

The bold color-blocking palette (red/orange field + green + deep-blue sky as a frequent chord) is carried by
the sref image and held constant across registers — this is what gives a batch its unity. Don't hand-specify
the full palette in-prompt; let the sref own it. Hue *accents* or colored *lighting* (neon / gels / golden
hour) read physically plausible, not painterly.

## The dial model (integrated)

The earlier **2-dial** model (subject-dominance × a free 3-stop render register: flat-graphic / soft-painterly
/ crisp-photoreal) is **refined, not discarded**. With the foreground invariant in force, render-register is
**pinned to photoreal** for any real subject — no longer a free production dial. Live variation is now:

1. **Subject dominance** — heroless color-field landscape (**first-class, not a defect**) → minor subject →
   photoreal hero. Each background register spans this full range freely.
2. **Background register** — **R1 / R2 / R3** (next section). This is where look-variety now lives.

What happened to the old render stops: **crisp-photoreal** became the invariant; the **soft-painterly middle**
survives only in the separate **Explore lane** (it can't be forced on a real subject in the production path);
**flat-graphic** is not in the automated path. Set everything with the **kernel + `--sref --sw`** — never "+
the moodboard".

## Background registers

Three production registers — **neutral names; no artist name in the system vocabulary** (the reference artist
exists only as an unnamed private style-ref image). The **foreground invariant holds across all three**, and
each still spans subject-dominance freely (heroless landscape → photoreal hero).

| Register | What it is | Params (one-pass) |
|---|---|---|
| **R1 Color-Block Terrain** | Bold saturated color on **real photographable terrain** — salt flats, badlands, dunes, ridgelines. Easiest, most reliable. | `--style raw --s 110 --sw 180` |
| **R2 Geometric Landform** | Clean **real** geometric land — stepped terraces, basalt columns, salt-pond grids, conical volcano. Geometry from real *nouns*, **not** "geometric/minimalist" *style* words. | `--style raw --s 100–120 --sw 150` |
| **R3 Chromatic Wave** | Flowing multicolor "wave" via **the bridge** (below). **Validated in-app 2026-06-23.** | `--style raw --s 100–110 --sw 220–250` |

All three are **one-pass**. A fourth, **Pure Color-Field** (non-representational), needs a 2-step composite and
is OUT of the automated path — see Deferred.

### The bridge (core resolution)

To get an **abstract-feeling, flowing-color background that still renders photoreal in one pass**, ground it in
a **real photographable phenomenon** rather than asking for "paint" / "gradient": multicolor crop / tulip
bands, painted-desert / Zhangye mineral strata, contour / terraced fields, salt-evaporation ponds, aerial
color bands. Then raw + low `--s` render the flowing color **photographically**, the composition still *feels*
abstract, and **a photoreal figure survives in the same pass**.

> **Breakpoint:** if a drone could photograph it, raw renders it and the figure survives. If it has no real
> referent (pure paint / gradient / brushstroke), it is **compositing territory** — manual, not the automated
> path.

*(Confidence: Med — R3 was validated in-app 2026-06-23; the exact far-abstraction breakpoint is still
unverified. See `../research/2026-06-21_midjourney-v8.1-current.md` §7–8.)*

## Explore lane (serendipity)

A separate, **un-preset discovery lane** that loosens control with **`--c 15–30`** to preserve serendipity —
including the **soft-painterly middle** the production registers engineer out. **Distinct from R1–R3**: use it
to find new looks, not to ship a locked style. Keepers feed the selection loop (and the `--p` training signal).

## Subject world — surreal natural world (the stage)

Natural / geological landscapes are the **stage**, optionally inhabited. The spine — the actual discriminator —
is **bold color-blocking + a single graphic gesture against negative space**: the natural world is the *stage*,
not the *theme*.

Subject range (breadth within unity):
- **Terrain (base)**: hills, plains, desert, water, rock, plateau, salt flats, badlands, dunes.
- **Architecture / structure**: a lone tiny house/cottage on a hill; a geometric pavilion / cube.
- **Flora**: cacti, a lone iconic tree, flowering shrubs.
- **Fauna**: horse, antelope, birds; a **figure-on-animal composite** as one hero.
- **Figures**: a lone person, dancers, small groups. (All people/animals → photoreal, per the invariant.)
- **Devices**: scale-play, mirroring, motion, color-blocking.

**Heroless color-field landscapes are first-class**, not a defect. **Keep subjects fresh** — the surreal natural
*world* is the constant; the specific subject/scene must be newly invented each time, not recycled (see
`.claude/rules/LESSONS.md`). Prompt convention: **detailed / specific** — richly specify subject + composition
+ light; the *look* (palette, render) stays on the kernel + `--sref`. See [[prompting]].

## Automation reality (one-pass constraint)

Automated path = **ONE-PASS only**, because V8.1 realism is **global**:

- `--style raw` / `--s` affect the **whole frame** — **no per-region control**. `::` is **concept emphasis, not
  spatial placement**; no ControlNet analogue. So "photoreal foreground + truly painterly/abstract background"
  **cannot be forced in one pass** by mixing raw/no-raw — which is why **the bridge** exists.
- **Compositing / inpaint** (needed only for pure non-representational abstraction) is **manual curation only**:
  the V8.1 web Editor does **not** run the V8.1 model and there is **no official MJ API**, so the automated path
  can't reliably composite — details + ToS risk in
  `.claude/agent-memory/researcher/reference_mj-api-automation-state.md`.

Design implication: anything not reachable in one pass is **out of the automated lane** by construction.

## Consistency stack

Cross-image cohesion, in priority order:

1. **Trained Personalization `--p`** — encodes *taste*, trained via the user's like/dislike selections.
2. **Fixed image `--sref` + `--sw` + `--sv 7`** — locks the *palette*.
3. **Deterministic post-grade (LUT / preset)** — the **only exact color lock** (MJ color is non-deterministic
   even at a fixed seed); a saved LUT/preset in `automation/` guarantees reproducible editorial color.

Caveats: a `/tune` custom `--style` code is a **subject-fragile accent**, not a base lock; **`--seed` repeats
the *same* prompt only** — not a cross-subject style lever.

## Home base — deferred

A single dominant "home" register is **deliberately NOT pre-decided.** It should **emerge from the user's
selections** over time — and those selections double as the `--p` training signal. Cohesion is **already
guaranteed by the shared kernel** (every image = raw + low `--s` + photoreal subject + one bold `--sref`), so a
dominant register isn't required now. Revisit once selection history reveals a lean.

## Deferred / out-of-automated-path

- **Pure Color-Field** (non-representational abstraction) — no real referent → **2-step composite**, manual
  curation only.
- **Cosmic / sea / film-grain** registers (a retro-collage direction; analysis in [[reference-accounts]]) remain
  **deferred** — revisit as future lanes after the core holds.
- Fuller candidate-lane names from the earlier "world-views" exploration live in **git history**; revive if wanted.

## Reference material

- Imported pool in `../../references/` (giz 18 + mariano 7 + 5 videos; provenance `references/manifest.jsonl`).
  This pool **feeds the private style-ref image** — it is not a system moodboard.
- **Color channel = a single self-uploaded bold reference image used as `--sref`** (the unnamed private
  style-ref). The reference artist is **not a named input to the system** — only this private image is.
- Reference SREF *codes* are **not harvested** (a paid product on the source's Contra); the route is the
  self-uploaded `--sref` image, **not** a moodboard. See [[reference-accounts]].

## Decision / verification log

- **2026-06-18**: two-axis framing; blend direction set.
- **2026-06-20**: reference pool imported; prompt convention = detailed/specific; doc cleanup + frontmatter.
- **2026-06-21**: Phase-1 moodboard built & rendering coherently. Multi-agent `/verify` ×2 → **2-dial model**
  (realism *not* subject-derived); **heroless = first-class**; **figure-on-animal** hero added; cosmic/sea/grain
  → future scope; **prompt-gen skill DEFERRED**. Docs consolidated 7→4.
- **2026-06-23**: **In-app validation.** Confirmed the **foreground invariant** (real subjects always photoreal
  via the raw + low-`--s` + photographic-cue **kernel**) and **the bridge** (grounding a flowing-color
  background in a real photographable phenomenon → abstract-feel + photoreal + surviving figure in ONE pass; R3
  validated). Locked the **3 registers R1/R2/R3** (neutral names — **no artist name in the system vocab**).
  **Superseded** the 2-dial model: render pinned to photoreal, variation = background-register. **Moodboard →
  single bold `--sref`** (`--sw ~150–250`, `--sv 7`); push color via `--sw`, never `--s`. Confirmed V8.1 realism
  is **global** (no per-region; `::` = emphasis) → automated path is **one-pass only**, pure-abstraction
  compositing is **manual-only**. **Home base = deferred** (emerges from selections = `--p` signal). Added the
  **Explore lane** (`--c 15–30`) + the **consistency stack** (`--p` + fixed `--sref`+`--sw`+`--sv 7` +
  post-grade LUT). Formalized via a 3-agent audit + cross-review.

## Status

**Working model — being validated by ongoing generation (observation phase; policy not locked).** Promote
`draft → active` once the **realism kernel, the bridge, and registers R1–R3 hold across a test set** and the
**one-pass automated path** is confirmed end-to-end. Home base stays deferred until selection history reveals a
lean.
