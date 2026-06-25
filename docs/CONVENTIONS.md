---
updated: 2026-06-25
status: active
type: index
---

# Doc Conventions

Minimal, self-contained conventions for this project's docs. Inspired by the marketing-ops
`doctrine/conventions.md` standard, kept intentionally light — **no linter** (manual discipline).

## Frontmatter

Every hand-authored Markdown doc under `docs/**` and each folder `README.md` carries:

```yaml
---
updated: YYYY-MM-DD
status: active        # active | draft | deprecated | archived
type: <role>          # index | reference | research | style | guide
---
```

- `updated` — date of last meaningful edit.
- `status` — `active` (current) · `draft` (in progress, not yet authoritative) · `deprecated` (kept for history only) · `archived` (moved to `/archive/` — superseded, kept for provenance).
- `type` — document role.

### Exemptions (no project frontmatter)

- `CLAUDE.md`, `AGENTS.md` — operating contracts.
- `.claude/agents/*`, `.claude/protocols/*` — runtime / own schema (protocols already carry their own frontmatter).
- `docs/research/<dated-bundle>/` and `/archive/<dated-bundle>/` files — external / archived snapshots; keep their source frontmatter as-is (the `docs/research/README.md` and `/archive/README.md` indexes are project docs and DO carry frontmatter).
- Non-Markdown: `.jsonl`, `.py`, images, video.

## Naming

- Folders & files: kebab-case `.md`.
- Dated material: `YYYY-MM-DD_description`.
- Reference handles / proper nouns: keep as-is.

## Archiving (superseded / legacy material)

Superseded material is **moved, never deleted, never left in the live tree**. Single home: top-level
**`/archive/`** (sub-folders under it are fine). When archiving an item:

1. **`git mv`** it into `/archive/` (preserve provenance — never delete + recreate).
2. Add a row to **`/archive/README.md`**: *item · archived date · why · superseded-by*.
3. Add a self-identifying **banner** at the top of the moved doc (just under any frontmatter), so it
   stands alone even if `/archive/README.md` is not read:
   `> **⚠️ ARCHIVED YYYY-MM-DD — <why>.** Superseded by <path>. Historical / sourcing only.`
4. Set `status: archived` if the doc carries project frontmatter; for external/source snapshots keep the
   original frontmatter as-is (the banner does the marking).
5. **Repoint every live reference** to the new `/archive/...` path.

Goal: after a memory reset, a future reader can tell — from the file itself **and** from
`/archive/README.md` — **what** it is, **when** + **why** it was archived, and **what replaced it**.

**Dated bundles** (a multi-file snapshot archived as one unit) may carry a single banner in their folder
`README.md` instead of one per file — the bundle is treated as one archived item.

## Source of truth

- `docs/style/` — the project's own visual style (SSoT).
- `docs/marketing/` — own marketing/growth decisions (publish phase): strategy, profile, captions (SSoT).
- `docs/research/` — external reference, read-only (current only).
- `automation/` — own IG publish-pipeline design + code (SSoT for the publish mechanics).
- `/archive/` — superseded / legacy material (see `/archive/README.md`).
- `.claude/PROGRESS.md` — progress SSoT.
