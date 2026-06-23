---
updated: 2026-06-23
status: active
type: guide
---

# moodboards

> **Note (2026-06-23): the moodboard is no longer the project's color tool.** Per
> `docs/style/style-definition.md`, color now comes from a **single bold image `--sref`** (a moodboard
> *averages* its images toward a muted centre and **can't be weighted**). Cross-image *taste* is held by
> a **trained Personalization `--p`** profile, not a per-image moodboard. This folder is retained only
> for historical moodboard records (e.g. `blend-v1`/`blend-v2`) and any future trained-`--p` notes — it
> is not part of the live generation recipe.

Registry of Midjourney moodboards / trained `--p` profiles used by the project (historical + taste-layer).

Per-record file (`<name>.md`) should capture:

- Purpose (historical color experiment / trained taste profile)
- The code (`--p` / snapshot) + date captured (note: a moodboard snapshot code **changes** when images
  are added/removed; the `m...ID` form invalidates on deletion)
- Image list (filenames or source URLs) at that snapshot
- Notes: what it averages toward, known drift

See `docs/research/2026-06-21_midjourney-v8.1-current.md` (current mechanics; §1 on why the moodboard
mutes color, §3C on trained `--p` as the taste layer).
