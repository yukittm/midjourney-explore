---
name: igpub-idempotency-model
description: How the IG publish pipeline guards against double-posting, and the known crash-window gap in that guard
metadata:
  type: project
---

The IG publish pipeline's anti-double-post guarantee rests on `post.result.media_id`: `publish_one` (automation/igpub/publish.py) skips any post that already has a persisted `media_id`. The runner's `--id` path treats `PUBLISHING` and `FAILED` as re-publishable (`_PUBLISHABLE` in automation/publish.py).

**Why:** MINIMAL build only implements image+carousel. The design header claims "never double-post" and "container-id recorded before publish."

**How to apply:** When reviewing changes to publish.py, watch the ordering gap: `graph.publish()` returns the media_id at ~line 105 but it is only persisted via `save_fn` at ~line 114. A crash in that window leaves a post published-on-IG but marked unpublished in the queue, and a `--id` retry of a `PUBLISHING` post re-drives from scratch → double-post. The per-asset `container_id` stored for carousel children is written but never read back for recovery, so it is not a real idempotency record. Any "reduce double-post risk" work should reconcile against IG (poll container / recent media) before re-publishing, not rely on in-memory state persisted after the irreversible API call. This was flagged in the first adversarial review (2026-06-25) as the highest-severity finding.
