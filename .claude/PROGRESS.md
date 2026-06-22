# PROGRESS.md

**Updated**: 2026-06-21 | **Project**: midjourney-explore | **Branch**: master [uncommitted: yes]

> Single progress SSoT for **both Claude and Codex**. Entry rules: `.claude/protocols/progress-management.md`.
> Entry format: `` YYYY-MM-DD [Actor:scope][s:UUID-8] **{🟢|🟡|🔴} title — status / committed `<hash>`** ``

## Current State
Phase 1 underway (MJ plan renewed). Built & verified the `blend-v1` moodboard (12 curated refs; Personalization = blend-v1 only, Global profile off) — the blend renders coherently (not muddy). Exploring world-views + prompt craft; adopted a project **prompt convention** (detailed/specific). Axis B (subject) leaning **surreal fine-art × figure × nature/cosmos**, not yet locked. No automation code yet.

> Solo project (Claude only) — §0 simplification in effect: entries use `[Claude:scope]`, `[s:UUID-8]` omitted. Rule 1 (commit hash on PASS) still applies.

## Roadmap
- [x] Scaffold from template + git init
- [x] Create folder structure (`docs/`, `prompts/`, `moodboards/`, `outputs/`, `automation/`)
- [x] Import Midjourney best-practices research → `docs/research/`
- [x] Analyze reference accounts + set **blend** direction → `docs/style/`
- [x] Import reference image pool → `references/`
- [x] Doc cleanup: de-template contracts + frontmatter convention (`docs/CONVENTIONS.md`)
- [x] Phase 1 start: build & verify `blend-v1` moodboard (blend renders coherently); set prompt convention (`docs/style/prompting-guide.md`) + world-view candidates (`docs/style/world-views.md`)
- [ ] **Converge style**: pick a world-view → focused moodboard → lock base prompts → decide Axis B → `style-definition.md` draft → active
- [ ] Lock base prompt templates per lane → `prompts/`
- [ ] Build Instagram auto-upload pipeline → `automation/`

## Entries (newest first)
2026-06-21 [Claude:research] **🟢 V8.1 research doc (web-researched + cross-reviewed) + prompt-length fix — PASS / `PENDING_COMMIT`**
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
Once the Midjourney plan is renewed: (1) browser pre-flight — Personalization **OFF**; (2) build a **blended moodboard** from `references/` (giz + mariano), register its snapshot code in `moodboards/`; (3) run neutral probe prompts (`docs/style/sref-sweep.md`) to diverge — this also surfaces Axis B (subject world); (4) characterize keepers and converge `style-definition.md` from `draft` → `active`.

## Context (Don't Lose)
- **Reference downloads**: scripted IG scraping (gallery-dl, yt-dlp) is blocked by IG auth + Chrome cookie decryption; browser URL-harvest is blocked by the harness redacting signed CDN URLs. Working method = user manually downloads → `scripts/import_references.py` imports into `references/` with a manifest. Self-contained (no marketing-ops reuse, by user request).
- **giz.akdag SREF codes**: not harvested — highlight slides are videos (unreadable) and the codes look like a paid product on her Contra. Blend uses the moodboard route instead.
- **Style = two axes**: A taste (sref/moodboard) = blend (`blend-v1` built & working); B subject world = being probed (leaning surreal fine-art × figure × nature/cosmos).
- **Moodboard upload gotcha**: MJ moodboard image upload needs the browser; the `file_upload` tool rejects project/temp paths ("session-shared files only"), so the user uploads manually (stage curated files to `~/Desktop/` for an easy drag-add).
- **Prompt convention**: this project defaults to detailed/specific prompts (subject+composition richly, ~30–40 words; style on the moodboard); loosen for exploration. SSoT: `docs/style/prompting-guide.md`.
