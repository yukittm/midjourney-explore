---
updated: 2026-06-27
status: active
type: guide
---

# outputs/selects — curation staging (human-only)

The middle tier between the raw generation pool and the formal posting queue. Drop the
images you want to post **next** here. This is a **human staging area** — the publish
pipeline never reads this folder; publishing is driven only by the yml records in
`automation/queue/`.

## Lifecycle (where a select goes)

```
outputs/candidates/   raw downloads (everything; binaries git-ignored)
   ↓  you pick
outputs/selects/      ← chosen, not yet processed   (this folder)
   ↓  enqueue (one command):
      python automation/new_post.py --image outputs/selects/<file>.jpg --slug <kebab> [--remove-select]
      → creates automation/assets/<id>/01.jpg + a draft automation/queue/<id>.yml
      (then write caption/alt by hand via the `caption` skill).
      NOTE: the image must be a cropped 4:5..1.91:1 JPEG (PNG/out-of-range is flagged).
automation/queue/<id>.yml      draft → approved → scheduled → publishing
   ↓  publish.py
automation/published/<id>.yml  record moves here after posting
automation/assets/<id>/01.jpg  the posted image lives here permanently
```

## Rules

- **Leave `selects/` at enqueue, not at publish.** Once an image becomes a queue entry
  (`automation/queue/<id>.yml` + the committed asset), remove it from `selects/` — from
  then on the yml `status` is the single source of truth for its state. This keeps
  `selects/` showing only "picked but not yet queued." (`new_post.py --remove-select`
  does this for you.)
- **No "posted" copy here.** The posted truth = `automation/published/<id>.yml` +
  `automation/assets/<id>/`. Don't mirror the lifecycle into `outputs/`.
- **Binaries are git-ignored** (root `.gitignore`); only this README is tracked. Keep a
  provenance sidecar (`.md`) with prompt/`--sref`/params next to a keeper if you want the
  recipe preserved (same convention as `outputs/`).

See `automation/asset-queue-model.md` for the queue/record model.
