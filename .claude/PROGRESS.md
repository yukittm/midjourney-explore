# PROGRESS.md

**Updated**: 2026-06-20 | **Project**: midjourney-explore | **Branch**: master [uncommitted: yes]

> Single progress SSoT for **both Claude and Codex**. Entry rules: `.claude/protocols/progress-management.md`.
> Entry format: `` YYYY-MM-DD [Actor:scope][s:UUID-8] **{🟢|🟡|🔴} title — status / committed `<hash>`** ``

## Current State
Project scaffolded from template; folder structure created and Midjourney best-practices research imported. Next phase: style establishment (find a personal `--sref` / moodboard aesthetic). No automation code yet.

> Solo project (Claude only) — §0 simplification in effect: entries use `[Claude:scope]`, `[s:UUID-8]` omitted. Rule 1 (commit hash on PASS) still applies.

## Roadmap
- [x] Scaffold from template + git init
- [x] Create folder structure (`docs/`, `prompts/`, `moodboards/`, `outputs/`, `automation/`)
- [x] Import Midjourney best-practices research → `docs/research/`
- [ ] **Style establishment**: explore `--sref` / moodboard, converge on a personal style → SSoT in `docs/style/`
- [ ] Lock base prompt templates per lane → `prompts/`
- [ ] Build Instagram auto-upload pipeline → `automation/`

## Entries (newest first)
2026-06-20 [Claude:style] **🟢 reference accounts analyzed + blend direction + reference pool imported — PASS / `PENDING_COMMIT`**
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
[strategy and order of operations]

## Context (Don't Lose)
[runtime observations, edge cases, failed approaches]
