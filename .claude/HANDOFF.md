---
created: 2026-06-27
type: handoff
status: temporary
lifecycle: read on the next session → confirm continuity → archive to /archive/ (then drop the PROGRESS pointer)
---

# Session Handoff — repo move (2026-06-27)

**Why this file exists:** the project was **moved** from `~/midjourney-explore` →
`~/Desktop/dev/midjourney-explore` (to sit with the other dev projects). This is a **temporary**
continuity note for the FIRST session opened from the new path. Once you've confirmed the state below,
**archive this file to `/archive/`** and remove the pointer at the top of `.claude/PROGRESS.md`.

**How to use it:** new session → Session Start Protocol → read `.claude/PROGRESS.md` → it points here →
read this → confirm → archive. (`PROGRESS.md` remains the SSoT; this is just the orientation + the move
context + the immediate next steps.)

> ⚠️ The `~/.claude/projects/-Users-tatsumiyuuki-midjourney-explore/` session history + auto-memory are
> **path-keyed to the OLD path** and do NOT follow the move (they stay orphaned-but-harmless under the old
> key). The repo's own `.claude/` (PROGRESS, rules, this file) moved intact — continuity lives there.

---

## Current state — one-screen snapshot (2026-06-27)

- **Style method (validated this session, in `prompting.md`):** keep-style × change-subject = **§9c: image
  `--sref` ONLY + subject-first rich prompt + low `--s`** (Remix/image-prompt drags COMPOSITION — that was the
  cactus/cosmic "collapse"). **§9b = same-layout swaps only.** Plus **§5c scale↔abstraction**, **§6b figures**
  (style figures intentionally / de-clone multiples). `style-definition.md` stays **draft** (promotion bar:
  R1/R2 + both light treatments must clear the gate on a fresh-subject set — not yet met).
- **Instagram:** handle **@tim.bankrupt**; pipeline PROVEN (manual `publish.py` cadence). **1 LIVE post** =
  `long-way-home` (https://www.instagram.com/p/DaDhalyn6iM/). Post #1 `color-window` was published then
  **DELETED** from IG (color too similar to #2 → anti-sameness signal: vary palette/subject next).
- **Exploration areas** (`exploration-map.md`): **A cactus = PARKED** (unfinished), **C cosmic = DONE**
  (lone figure on a gravity-defying flowing-color Möbius ribbon — the "reality-defying" lane VALIDATED:
  remove the floor → form floats/twists), **B architecture = NEXT**, D/F/G open, E prisms skipped.
- **Candidate pool:** `outputs/candidates/` now holds **185 MJ images** (git-ignored = local working pool).
  User is pruning the unwanted ones. Published images live (tracked) in `automation/assets/<id>/`.

## Next tasks (pick up here)

1. **② caption-writing SKILL** — codify the new caption direction (one line, ~80/20 axis-absorb, casual,
   anti-sameness, approach-based). `ig-growth-strategy.md` §10 has a pointer flagging this.
2. **① Area B (architecture) exploration** — frame → cross-review (agents) → prompts. The just-posted villa
   (`long-way-home`) is a good architecture×style reference.
3. **Prune `outputs/candidates/`** (user) → then formalize keepers to `YYYY-MM-DD_<lane>_<slug>.{jpg,md}` +
   provenance sidecars (prompt/sref/params).
4. **Token** — regenerate **non-expiring** before ≈2026-08-24 (currently a 60-day token; 2 publishes worked on it).
5. **`CLAUDE.md` ↔ `AGENTS.md` Quick-mode drift** — CLAUDE says Quick = A+C+D; AGENTS says "preserve all 5,
   don't downgrade to A+C+D." Reconcile (align one way) or annotate as deliberate — **user decision pending**.
6. Deferred: Phase-1 scheduled-auto clock (VPS vs Lambda); optional `Status.deleted` first-class seam;
   optional published `INDEX.md` (numbered post-log) — user chose to keep the `date_slug` ID scheme as-is.

## Working rules reinforced this session (see `.claude/rules/LESSONS.md`)

- **Frame the exploration BEFORE generating prompts** (decide variable/constant); **cross-review with agents
  every time** (solo drifts); **confirm understanding in chat before writing**.
- **Keep a cumulative constraint checklist across prompt rounds — never regress a prior fix.**
- **View the MJ tab via Claude-in-Chrome** (not Downloads). **No labels inside copyable prompt blocks.**
- MJ craft: realism kernel + reward gate; `--no` uses single tokens (multi-word splits); ~74-token influence
  cap (front-load load-bearing cues).

## Key paths (relative to repo root)
`.claude/PROGRESS.md` (SSoT) · `docs/style/{prompting,style-definition,exploration-map}.md` ·
`docs/marketing/ig-growth-strategy.md` · `automation/` (pipeline; `.env` = token, gitignored) ·
`outputs/candidates/` (pool, local) · `automation/assets/<id>/` (published images) ·
`automation/published/<id>.yml` (post records).

## Verification command
`PYTHONPATH=automation python3 -m unittest discover -s automation/tests` (75 tests; `pip install -r automation/requirements.txt` first).
