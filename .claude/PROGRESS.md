# PROGRESS.md

**Updated**: 2026-06-20 | **Project**: midjourney-explore | **Branch**: master [uncommitted: no]

> Single progress SSoT for **both Claude and Codex**. Entry rules: `.claude/protocols/progress-management.md`.
> Entry format: `` YYYY-MM-DD [Actor:scope][s:UUID-8] **{🟢|🟡|🔴} title — status / committed `<hash>`** ``

## Current State
Style-establishment phase, divergence prep done: reference accounts analyzed (`giz.akdag` + `marianopeccinetti`), **blend** direction set, reference image pool imported (`references/`). Docs cleaned (de-templated contracts + minimal frontmatter convention). **Blocked on the Midjourney plan** for Phase 1 generation. No automation code yet.

> Solo project (Claude only) — §0 simplification in effect: entries use `[Claude:scope]`, `[s:UUID-8]` omitted. Rule 1 (commit hash on PASS) still applies.

## Roadmap
- [x] Scaffold from template + git init
- [x] Create folder structure (`docs/`, `prompts/`, `moodboards/`, `outputs/`, `automation/`)
- [x] Import Midjourney best-practices research → `docs/research/`
- [x] Analyze reference accounts + set **blend** direction → `docs/style/`
- [x] Import reference image pool → `references/`
- [x] Doc cleanup: de-template contracts + frontmatter convention (`docs/CONVENTIONS.md`)
- [ ] **Style establishment (Phase 1 — needs MJ plan)**: build blended moodboard from `references/`, probe-generate, decide Axis B (subject) → converge SSoT `docs/style/style-definition.md`
- [ ] Lock base prompt templates per lane → `prompts/`
- [ ] Build Instagram auto-upload pipeline → `automation/`

## Entries (newest first)
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
- **Style = two axes**: A taste (sref/moodboard) = blend (decided); B subject world = decided by probing (pending plan).
