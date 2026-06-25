---
updated: 2026-06-25
status: active
type: guide
---

# scripts

One-off / utility scripts — **not** the product pipeline.

- `import_references.py` — imports manually-downloaded reference images into `references/` with a
  `manifest.jsonl` provenance record.

**Boundary:** the **IG publish-pipeline code** (`publish.py`, `validate.py`, the `igpub/` core) lives in
**`automation/`** (see `automation/ig-publish-pipeline.md`), not here. `scripts/` stays for standalone utilities.
