---
updated: 2026-06-25
status: active
type: guide
---

# outputs

Generated images and their metadata.

- `candidates/` — raw generations under evaluation (the full **generation pool**).
- `selects/` — **curation staging**: the images you've chosen to post next, before they
  become queue entries. Human-only — the pipeline never reads it; it self-empties as you
  enqueue. See [selects/README.md](selects/README.md).
- The small curated **publish subset** is copied into `automation/assets/<id>/` (tracked,
  served by GitHub Pages) when a post is queued — see
  [asset-queue-model.md](../automation/asset-queue-model.md) §2.
- **Lifecycle:** `candidates/` → `selects/` → (enqueue) `automation/queue/<id>.yml` +
  `automation/assets/<id>/` → (publish) `automation/published/<id>.yml`. A select leaves
  `selects/` at **enqueue**, not at publish; the posted image lives permanently in
  `automation/assets/<id>/` (no "posted" copy under `outputs/`).
- Image/video binaries are **git-ignored** (see root `.gitignore`); metadata `.md`/`.json`
  sidecars are tracked so the provenance survives even when the binary doesn't.
- For each kept output, store a metadata sidecar with: prompt, `--v`, `--ar`, `--s`/`--c`,
  `--sref` code(s), `--seed`, and date.

Naming: `YYYY-MM-DD_<lane>_<slug>.{png,md}` (binary + sidecar share the stem).
