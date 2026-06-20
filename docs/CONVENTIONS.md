---
updated: 2026-06-20
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
status: active        # active | draft | deprecated
type: <role>          # index | reference | research | style | guide
---
```

- `updated` — date of last meaningful edit.
- `status` — `active` (current) · `draft` (in progress, not yet authoritative) · `deprecated` (kept for history only).
- `type` — document role.

### Exemptions (no project frontmatter)

- `CLAUDE.md`, `AGENTS.md` — operating contracts.
- `.claude/agents/*`, `.claude/protocols/*` — runtime / own schema (protocols already carry their own frontmatter).
- `docs/research/<dated-bundle>/` files — external research snapshots; keep their source frontmatter as-is (the `docs/research/README.md` index is a project doc and DOES carry frontmatter).
- Non-Markdown: `.jsonl`, `.py`, images, video.

## Naming

- Folders & files: kebab-case `.md`.
- Dated material: `YYYY-MM-DD_description`.
- Reference handles / proper nouns: keep as-is.

## Source of truth

- `docs/style/` — the project's own visual style (SSoT).
- `docs/research/` — external reference, read-only.
- `.claude/PROGRESS.md` — progress SSoT.
