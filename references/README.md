---
updated: 2026-06-25
status: active
type: guide
---

# references

Curated reference-image pool for visual taste (the `--sref` / style-anchor source material).

- **Import contract** — binaries are **not** scraped. The user **manually downloads** from Instagram,
  then `scripts/import_references.py` imports them into per-handle folders and records provenance in
  `manifest.jsonl` (sha256-keyed). Why scripted scraping is blocked: `.claude/PROGRESS.md` → "Context (Don't Lose)".
- **Tracked vs ignored** — image/video binaries are **git-ignored** (root `.gitignore`); `manifest.jsonl`
  is tracked, so provenance survives without bloating the repo.
- **Layout** — `<handle>/` per source (proper-noun names kept as-is) · `_unsorted/` = holding pen for files
  the importer cannot attribute (resolve, or leave pending).

See `docs/style/reference-accounts.md` for the accounts and what each contributes.
