---
updated: 2026-06-25
status: active
type: guide
---

# outputs

Generated images and their metadata.

- `candidates/` — raw generations under evaluation.
- Image/video binaries are **git-ignored** (see root `.gitignore`); metadata `.md`/`.json`
  sidecars are tracked so the provenance survives even when the binary doesn't.
- For each kept output, store a metadata sidecar with: prompt, `--v`, `--ar`, `--s`/`--c`,
  `--sref` code(s), `--seed`, and date.

Naming: `YYYY-MM-DD_<lane>_<slug>.{png,md}` (binary + sidecar share the stem).
