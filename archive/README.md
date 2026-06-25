---
updated: 2026-06-25
status: archived
type: index
---

# archive

Superseded / historical material — **not current**. Kept for provenance and sourcing only. Do **not**
use as current guidance; the live sources of truth are `docs/style/` (the project's own style) and
`docs/research/2026-06-21_midjourney-v8.1-current.md` (current MJ mechanics).

Everything that becomes legacy lands **here** (sub-folders allowed), each row recording **when** and
**why** it was archived and **what replaced it** — so a future reader (even after a memory reset) never
loses the thread. Procedure: see `docs/CONVENTIONS.md` → "Archiving".

## Index

| Item | Archived | Why archived | Superseded by |
|---|---|---|---|
| `2026-05-11_midjourney-prompt-best-practices/` | 2026-06-23 | V7-era bundle; MJ moved to V8.1, so its V7 parameter specifics are no longer current (kept for the sourced record + still-useful conceptual mechanics). | `docs/research/2026-06-21_midjourney-v8.1-current.md` |
| `2026-05-13_mj-moodboard-automation-idea.md` | 2026-06-23 | V7-era moodboard-automation idea (carried from marketing-ops); superseded by the current one-pass automation policy. | `automation/README.md` |
| `2026-06-25_moodboards-retired.md` | 2026-06-25 | Moodboard retired as the color tool (color now via a single bold `--sref`); the `moodboards/` folder held only a README and advertised a dead mechanism. | `--sref` color route + `docs/style/`; future `--p` notes → `docs/style/` or a new `profiles/`. |

## How to add to the archive

When a doc is superseded: `git mv` it here → add a row above (item · archived date · why · superseded-by)
→ add a `> **⚠️ ARCHIVED YYYY-MM-DD — <why>.** Superseded by <path>.` banner at the top of the moved doc
→ repoint every live reference to the new `/archive/...` path. Never delete; never leave it in the live
tree. (Full rule: `docs/CONVENTIONS.md`.)
