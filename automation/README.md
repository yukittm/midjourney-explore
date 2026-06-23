---
updated: 2026-06-23
status: active
type: guide
---

# automation

Instagram auto-upload pipeline (code). Empty until the automation phase begins.

## North star & policy (decided 2026-06-23; observation phase, not yet built)

**End goal:** near-full automation — theme/prompt generation → Claude-driven Midjourney operation
(Claude-in-Chrome) → Instagram publishing. **Roles:** the **user is the creative director** (reacts to
themes + selects images — "this / that"); **Claude autonomously generates the patterns/combinations**.
Selections double as the like/dislike training signal for the consistency stack.

**Hard constraints (from `docs/style/style-definition.md` + the V8.1 research):**
- **One-pass generation only** in the automated path. V8.1 realism is global (no per-region), so any look
  that needs compositing/inpaint (pure non-representational backgrounds) is **manual curation only** —
  the V8.1 web Editor runs on the V6.1 model, there is **no official MJ API**, and unofficial wrappers
  carry ToS/ban risk. See `.claude/agent-memory/researcher/reference_mj-api-automation-state.md`.
- **Consistency stack** to apply: trained Personalization `--p` (taste) + a fixed image `--sref`
  (`--sw`/`--sv 7`, palette) + a deterministic **post-grade LUT/preset** (the only exact color lock).
- **Home base deferred** — the register mix emerges from the user's selections, not pre-set.

Pipeline shape: pick `(subject, register ∈ {R1,R2,R3}, optional seed)` → kernel + `--sref` →
generate HD (one pass) → apply LUT → publish. (The `./2026-05-13_mj-moodboard-automation-idea-archived.md`
is an archived V7-era moodboard idea — historical, NOT the active plan.)

When code lands here, set the project's **Verification commands** (test/lint/build) in
`.claude/PROGRESS.md` and `CLAUDE.md`. Keep secrets in `.env` (git-ignored), never committed.
