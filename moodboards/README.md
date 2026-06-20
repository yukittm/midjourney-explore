---
updated: 2026-06-20
status: active
type: guide
---

# moodboards

Registry of Midjourney moodboards used by the project.

Why a registry: a moodboard's **snapshot code** (`--profile <code>`) persists across deletion but
**changes every time an image is added/removed**, and the `m...ID` form invalidates on deletion.
To keep outputs reproducible, record the snapshot code + the exact image list at each generation run.

Per-moodboard file (`<lane>.md`) should capture:

- Lane / purpose (editorial / fashion / texture / still-life ...)
- Current snapshot code + date captured
- Image list (filenames or source URLs) at that snapshot
- Notes: what aesthetic it averages toward, known drift

See `docs/research/2026-05-11_midjourney-prompt-best-practices/03_image-prompts-and-moodboard.md`
and `06_moodboard-semantics-and-starter-recipe.md`.
