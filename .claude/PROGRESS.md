# PROGRESS.md

**Updated**: 2026-06-23 | **Project**: midjourney-explore | **Branch**: master [uncommitted: yes]

> Single progress SSoT for **both Claude and Codex**. Entry rules: `.claude/protocols/progress-management.md`.
> Entry format: `` YYYY-MM-DD [Actor:scope][s:UUID-8] **{🟢|🟡|🔴} title — status / committed `<hash>`** ``

## Current State
Style model **formalized** (validated in-app 2026-06-23). **Foreground = photoreal invariant** (kernel: `--style raw` + low `--s` + photo cues + `--no painting/illustration/3d/cgi`); **color = single bold image `--sref`** (`--sw` 150–250, `--sv 7`) — the averaging moodboard is retired as the color tool. **The bridge**: name an abstract background as a real drone-photographable phenomenon → one-pass abstract-feel + photoreal figure (R3 validated). **3 background registers** (R1 Color-Block Terrain / R2 Geometric Landform / R3 Chromatic Wave; deferred Pure Color-Field) + a separate **explore lane** (`--c 15–30`). Reference artist = unnamed private `--sref` (name out of system vocabulary). **Automation north-star**: one-pass full-auto (theme → Claude-in-Chrome → IG); user = creative director; **home base deferred**. **On-style is now a REWARD GATE** (photoreal / saturated-chord / one-surreal-idea+restraint / **decisive light**) + a **decisive-light lever** (hard-graphic ⇄ golden-warm); **ONE photoreal render mode** (a "two-mode flat-graphic/warm" split was falsified on the full 11-image set). Objective = **own style** (giz = look-anchor); subject **heroless-leaning**; **exact personal palette deferred** (Mariano + own outputs, later). Observation phase — policy not locked. No automation code yet.

> Solo project (Claude only) — §0 simplification in effect: entries use `[Claude:scope]`, `[s:UUID-8]` omitted. Rule 1 (commit hash on PASS) still applies.

## Roadmap
- [x] Scaffold from template + git init
- [x] Create folder structure (`docs/`, `prompts/`, `moodboards/`, `outputs/`, `automation/`)
- [x] Import Midjourney best-practices research → `docs/research/`
- [x] Analyze reference accounts + set **blend** direction → `docs/style/`
- [x] Import reference image pool → `references/`
- [x] Doc cleanup: de-template contracts + frontmatter convention (`docs/CONVENTIONS.md`)
- [x] Phase 1 start: build & verify the moodboard; set prompt convention + world-view candidates (since consolidated into `docs/style/prompting.md` + `style-definition.md`)
- [x] Validate the V8.1 model in-app (2026-06-23): photoreal kernel + `--sref` color + the bridge + registers R1/R2/R3
- [x] Formalize the model into `docs/style/` + research + automation policy (2026-06-23; 3-agent audit + cross-review)
- [ ] **Promote `style-definition.md` `draft → active`** once a Phase-1 test set holds across R1/R2/R3 + the one-pass path is confirmed end-to-end
- [ ] Lock base prompt templates per register + explore lane → `prompts/`
- [ ] Build Instagram auto-upload pipeline (one-pass path first) → `automation/`

## Entries (newest first)
2026-06-23 [Claude:fix] **🟢 remove `--sv 7` from all recipes (V8.1 rejects it) — PASS / committed `832251d`**
  - Live submit error *"Unsupported Style Reference version 7 for --version 8.1"* traced to `--sv 7` baked into every prompt recipe (from a research-doc claim flagged "verify in-app"). **Fix: for an image `--sref` on V8.1, OMIT `--sv`** (model default; `--sv 6` incompatible with `--hd`, `--sv 4` forces V7). Scrubbed `--sv 7` from style-definition / prompting / automation / prompts; corrected the research-doc `--sv` row to in-app fact. LESSONS updated (verify load-bearing params in-app before baking into recipes). Re-issued the test prompts without `--sv 7`.

2026-06-23 [Claude:style] **🟢 lock the style signature (full-evidence) + reward gate + decisive-light lever — PASS / committed `2052e9c`**
  - Re-grounded the giz signature on the **full 11-image curated set** (3 independent reads + an adversarial check) after catching a **2-image over-generalization** (LESSONS updated). **Falsified** the proposed "two-mode flat-graphic / warm-photographic split" — all 11 are photoreal; "graphic" = composition + hard light. **ONE photoreal render mode kept.**
  - **Added the on-style REWARD GATE** (① photoreal · ② saturated red/green/blue chord · ③ one surreal idea + restraint · ④ **decisive light**) as the anti-drift objective ("on-style" = a checklist, not a vibe), and the **decisive-light lever** (hard-graphic ⇄ golden-warm). Surgical additions; kernel/registers/bridge/explore/one-pass all kept (no rewrite).
  - **User decisions locked:** objective = own style (giz = look-anchor; curated 11 = chosen direction, not all-of-giz); home base = deferred; subject = heroless-leaning/balanced; palette = giz-bold-saturation now, **exact personal palette deferred** (Mariano + own outputs, later); removed "soccer"/specific-subject words from the style docs; "Claude-alone" bounded honestly (prompt-gen + LUT automatable; sref-upload/browser/`--p`/selection/publish human-assisted).
  - Process: 3-agent build + adversarial hole-find + reward/decisions, converged; the adversarial pass caught the two-mode error **before** any doc write (= the no-rework the user asked for). Edited style-definition / prompting / reference-accounts / automation. Next = the **reward-gate validation test** (R1/R2 + both lights, fresh subjects) → promote `draft → active`.

2026-06-23 [Claude:docs] **🟢 formalize the `/archive/` convention (durable / memory-reset-proof) — PASS / committed `e14fdde`**
  - Made `/archive/` the single, self-documenting home for legacy. Added an **Archiving** section to `docs/CONVENTIONS.md` (move-not-delete procedure + `archived` status + the banner format); rebuilt `archive/README.md` as an index recording **archived-date · why · superseded-by** per item + a "how to add" procedure; added a self-identifying `⚠️ ARCHIVED YYYY-MM-DD — why → superseded-by` banner to each archived doc (and fixed the V7 bundle banner's stale path).
  - Goal: after a memory reset, **what / when / why / replaced-by** is recoverable from the files alone (banner) + `/archive/README.md` (index), without prior context.

2026-06-23 [Claude:docs] **🟢 introduce `/archive/` + relocate V7-era legacy out of the live tree — PASS / committed `309d582`**
  - Created top-level **`archive/`** (README + supersede table). `git mv`'d the V7-era research bundle `2026-05-11_midjourney-prompt-best-practices/` (out of `docs/research/`) and the V7-era moodboard-automation idea (out of `automation/`) into it; removed the vestigial empty `agent-memory/design-reviewer/` dir.
  - Updated all pointers (research doc frontmatter + body; `docs/research/README.md` archive section, "8 files"→"7"; `automation/README.md`). `docs/research/` is now current-only (V8.1 doc + README); `automation/` is README-only. No broken refs.
  - Added a LESSONS entry: move superseded docs into `/archive/` (don't delete, don't leave in place) to keep the live tree clean.

2026-06-23 [Claude:style] **🟢 formalize validated V8.1 style model — photoreal invariant + 3 background registers + the bridge + automation policy — PASS / committed `ef27769`**
  - In-app validation (2026-06-23) replaced the moodboard/2-dial model. New SSoT model: **foreground INVARIANT = photoreal** (kernel = `--style raw` + low `--s ~90–120` + photo cues + `--no painting, illustration, 3d render, cgi`); **color = single-image `--sref`** (`--sw` 150–250, `--sv 7`), push color via `--sw` not `--s` — averaging moodboard retired as the color tool.
  - **THE BRIDGE**: ground abstract/flowing backgrounds in REAL drone-photographable phenomena (crop/tulip bands, painted-desert strata, terraced/contour fields, salt ponds, aerial bands) → one raw pass yields abstract-feel + real figure. Breakpoint: drone-photographable = one-pass; pure-paint = compositing.
  - **3 neutral-named background registers** (artist name OUT of system vocabulary; reference artist = unnamed private `--sref`): R1 Color-Block Terrain · R2 Geometric Landform · R3 Chromatic Wave (validated); deferred Pure Color-Field (2-step, manual). Separate **explore lane** (`--c 15–30`).
  - **Prompt-length ~40-word cap RETIRED** — V8.1 honors detailed prompts; lever = kernel + real-phenomenon naming + sref, not word count (LESSONS updated).
  - **Automation north-star** recorded in `automation/`: full auto (theme/prompt-gen → Claude-in-Chrome → IG); user = creative director; one-pass only (compositing manual — V8.1 Editor=V6.1, no official API, unofficial=ToS); **home base deferred** (emerges from `--p` training); consistency = `--p` + image-sref + post-grade LUT.
  - Process: 3-agent audit (style-definition / prompting / cross-doc legacy sweep) → synthesized + authored → **3-agent Round-2 cross-review (converged 0 CRITICAL/HIGH; minor fixes applied)** → committed `ef27769`. Rewrote `style-definition.md` + `prompting.md`; added GLOBAL-realism + bridge + reproducibility-ranking + API-state pointer to the V8.1 research doc; fixed `prompts/README` + `moodboards/README` V7 templates; neutralized giz-as-identity in `reference-accounts`/`README`; resolved prior entry hash `PENDING_COMMIT`→`6b0efbe`.

2026-06-21 [Claude:research] **🟢 V8.1 research doc (web-researched + cross-reviewed) + prompt-length fix — PASS / committed `6b0efbe`**
  - Created `docs/research/2026-06-21_midjourney-v8.1-current.md` (current MJ SSoT). Classified the V7 bundle as **ARCHIVE** (banner + README split: latest vs archive).
  - Built from a 4-agent web-research pass, then a **4-agent web-verified cross-review** (A/C/D/E). Corrections applied: `--sv 4` retained (not removed), `--iw` **0–3** (not 0–2), `--sw` color-band lowered to ~150–250 (300+ experimental), **moodboard untunable by `--sw`/`--sv`**, added **`--hd` (HD-by-default)** + `--exp` + **`/tune` Style Tuner + trained Personalization** (the consistency path for our goal) + `--no` syntax & grammar promoted from archive. **Thesis validated**: two-channel (raw+low-`--s` = realism / sref = color); the moodboard-only route was the wrong tool.
  - Also hardened `docs/style/prompting.md` to a **~40-word target** + added a LESSONS entry (repeated under-delivery on prompt length).
  - Open: relocate the mis-filed `2026-05-11_.../07_future-automation-option.md` out of `docs/research/`.

2026-06-21 [Claude:docs] **🟢 consolidate docs/style 7→4 + apply 2-dial corrections — PASS / committed `da4244f`**
  - Folded `prompting-guide` + `prompt-skill-spec`(recipe) + `idea-bank` → new `docs/style/prompting.md` (craft) with the **corrected recipe** (heroless = first-class, reject = idea-less, `--iw` not `--oref`, element-type defined, single-lane override, soft-painterly register, figure-on-animal hero).
  - Rewrote `style-definition.md` (SSoT) with the **2-dial model** + giz natural-world direction + color/finish corrections + decision log; absorbed world-views' decided direction + future-lane names.
  - **Removed (content folded first; checkpoint `f5d0423` + git history)**: `sref-sweep`, `world-views`, `prompt-skill-spec`, `prompting-guide`, `prompts/idea-bank`. Fixed wikilinks/paths in `reference-accounts` + READMEs.
  - `docs/style/` now: `style-definition` / `prompting` / `reference-accounts` / `README`.

2026-06-21 [Claude:style] **🟢 prompt-model re-verified (2-dial) + doc-consolidation plan — PASS / committed `f5d0423`**
  - Drafted `docs/style/prompt-skill-spec.md` (recipe). Ran multi-agent `/verify` (Full A–E), then a RE-RUN scoped to the user's curated **11-image giz-only** set at `~/Desktop/reference-blend-v1/` (Mariano dropped + swaps).
  - **Model corrected → 2 dials**: subject-dominance × a **3-stop render register** (flat-graphic / soft-painterly / crisp-photoreal), register **NOT derived from subject** (falsified in-set by the sheep / baobab / ibis). Heroless landscapes are **first-class** (~5/11); the real reject is **idea-less**, not heroless. Add **figure-on-animal composite hero** (G01). Demote non-core natural registers (cosmic/sea/grain) to **future scope**. Color-unity is **better** in the giz-only set. `--oref` invalid on V8.1 → use `--iw`; preset table missing; element-type undefined. **Skill DEFERRED** (validate via Phase 1 first; later a thin sampler-only skill).
  - Next: consolidate `docs/style/` **7 → 4** (style-definition SSoT + prompting craft + reference-accounts + README; fold sref-sweep/world-views/prompt-skill-spec/idea-bank, then remove sources — content moved first, no loss) and apply the 2-dial corrections. This entry is the **checkpoint before the restructure**.

2026-06-21 [Claude:style] **🟢 Phase 1: blend-v1 moodboard built & verified; world-views + prompt convention — PASS / committed `17e3466`**
  - MJ plan renewed. Built `blend-v1` moodboard (12 curated refs from `references/`, user-uploaded via browser; `file_upload` tool blocked on session-shared-files, so curated set staged to `~/Desktop/reference-blend-v1/` for manual add). Personalization = blend-v1 only (Global V7/V8 Profile + other moodboards deselected). Verified the blend applies and renders coherently (not muddy).
  - Creative direction explored: `docs/style/world-views.md` (10 world-view candidates), `prompts/idea-bank.md` (conceptual moves). Axis B leaning surreal fine-art × figure × nature/cosmos (not locked).
  - Validated detailed-prompt reproduction (giz tennis court): learned **stylize↓ = fidelity↑**, **specificity narrows range**. Created `docs/style/prompting-guide.md`; adopted **project prompt convention = detailed/specific** (independent agent cross-review → PROCEED WITH CHANGES, applied; research bundle left frozen, sref-sweep probes unchanged).
  - Boundary: no style locked yet (`style-definition.md` still `draft`); no automation.

2026-06-20 [Claude:docs] **🟢 doc cleanup: de-template contracts + frontmatter convention — PASS / committed `dd7c6f4`**
  - Removed legacy "Template-Specific Rules" from `CLAUDE.md` + `AGENTS.md` (project is no longer a template); relocated Project Context to a top-level section + added real Source-of-truth / Verification notes (mirrored in both).
  - Added a minimal frontmatter convention (`docs/CONVENTIONS.md`, no linter) and applied `updated/status/type` frontmatter to `docs/**` + folder READMEs. Removed a stale `mobileeditingclub` reference from `style-definition.md`.
  - Refreshed this PROGRESS (Current State, Roadmap, filled the Approach / Context sections).

2026-06-20 [Claude:style] **🟢 reference accounts analyzed + blend direction + reference pool imported — PASS / committed `bb8bc37`**
  - Confirmed & analyzed reference accounts `giz.akdag` (crisp editorial) + `marianopeccinetti` (retro collage); recorded the two-axis framing (A: taste / B: subject) and the **blend** direction in `docs/style/{reference-accounts,style-definition}.md`.
  - Imported 30 manually-downloaded media into `references/` (18 giz / 7 mariano / 5 unattributed video) via `scripts/import_references.py` + `references/manifest.jsonl` (sha256/provenance). Binaries gitignored; **self-contained — no marketing-ops reuse** (investigated its capture tool but rejected reuse to avoid cross-project contamination).
  - Boundary: no generation yet (MJ plan pending). Next: capture giz SREF codes (Phase 0 remainder); Phase 1 diverge needs the plan.

2026-06-18 [Claude:style] **🟢 sref sweep worksheet — PASS / committed `b08eeff`**
  - Created `docs/style/sref-sweep.md`: divergence-stage worksheet to find a personal style by holding the prompt constant and varying `--sref`. Includes Personalization-control pre-flight, neutral probe prompts per lane, candidate-code table, sweep command patterns, evaluation log, and convergence step.
  - Cross-refs research files 03/05/06. Next: user collects candidate sref codes and runs the sweep.

2026-06-18 [Claude:setup] **🟢 project scaffold + structure + research import — PASS / committed `b08eeff`**
  - Expanded `00_template` (CLAUDE.md / AGENTS.md / .claude / .gitignore); filled Project name + adoption-history + Project Context (Midjourney explore → style → IG automation).
  - Created folders with self-documenting READMEs: `docs/research`, `docs/style`, `prompts`, `moodboards`, `outputs/candidates`, `automation`. Added outputs binary ignores to `.gitignore`.
  - Copied 8-file Midjourney V7 best-practices bundle from `marketing-ops` → `docs/research/2026-05-11_midjourney-prompt-best-practices/`.
  - Verification: `find` confirms tree; structure approved by user. Next: style-establishment phase.

## Key Decisions
- Folder structure mirrors the 3 project phases (explore → style → automate): `docs/research` (external ref), `docs/style` (own-style SSoT), `prompts`, `moodboards`, `outputs`, `automation`.
- `docs/style/` is the SSoT for the project's own visual style; `docs/research/` is read-only external reference (not SSoT).
- outputs binaries git-ignored, metadata sidecars tracked — preserves provenance without bloating the repo.

## Approach for Next Session
Run a Phase-1 **test set per register** (R1/R2/R3) using the kernel + a single bold `--sref` + real-phenomenon background naming; confirm one-pass abstract-feel + photoreal figure holds → promote `style-definition.md` `draft → active`. Then lock per-register base templates in `prompts/`. Track the user's selections (they reveal the home-base register mix + train `--p`). Defer compositing/home-base until the one-pass core is locked. (Formalization cross-reviewed + committed `ef27769`; next concrete step = the R1/R2 test set.)

## Context (Don't Lose)
- **Reference downloads**: scripted IG scraping (gallery-dl, yt-dlp) is blocked by IG auth + Chrome cookie decryption; browser URL-harvest is blocked by the harness redacting signed CDN URLs. Working method = user manually downloads → `scripts/import_references.py` imports into `references/` with a manifest. Self-contained (no marketing-ops reuse, by user request).
- **giz.akdag SREF codes**: not harvested — highlight slides are videos (unreadable) and the codes look like a paid product on her Contra. Color route = a self-uploaded bold `--sref` image, not a moodboard.
- **Style model (formalized 2026-06-23)**: foreground photoreal invariant (kernel) + color via single bold `--sref` + 3 background registers R1/R2/R3 + the bridge. The artist name is out of the system vocabulary (unnamed private `--sref`). SSoT: `docs/style/style-definition.md`.
- **Reference-image upload gotcha**: MJ image upload (moodboard or `--sref`) needs the browser; the `file_upload` tool rejects project/temp paths ("session-shared files only"), so the user uploads manually (stage curated files to `~/Desktop/` for an easy drag-add).
- **Prompt convention**: detailed/specific, but **length is not the lever** (no ~40-word cap) — the levers are the kernel + naming the real subject/phenomenon + the `--sref`. SSoT: `docs/style/prompting.md`.
