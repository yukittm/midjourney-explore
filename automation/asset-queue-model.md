---
updated: 2026-06-27
status: active
type: design
---

# Asset + Posting-Queue Model

> Converged from a 4-agent design pass (data-model · storage/host · scheduling · extensibility/holes),
> 2026-06-25. **Adversarially verified 2026-06-25** (1 critical + 6 high folded in). Goal: a near-best, hole-free, highly-extensible model
> for managing post media + the posting queue, covering ALL Instagram post types. Extends
> [`ig-publish-pipeline.md`](ig-publish-pipeline.md). Reorganizing later is costly → settle it here.

## 0. Resolved decisions (the forks)
| Fork | Decision | Why |
|---|---|---|
| Per-post data model | **`Post → [Asset]`** — Post is a discriminator (`media_type`) over an **ordered `assets` list** | Every IG type = "N ordered assets + which fields apply" → new types are additive (enum + rule + call-mapping), core untouched |
| Image host | **Images → main-repo GitHub Pages** (`automation/assets/<id>/NN.jpg`, tracked) | $0, atomic (image+queue+provenance in one commit), git-versioned audit |
| Video host | **Video → Cloudflare R2** (`r2.dev` → custom domain later) — **DEFERRED to FULL (no video yet; images on Pages)** | Pages/LFS/git can't host video (size/bandwidth caps); R2 = zero-egress public URL Meta can fetch |
| Separate assets repo | **Retire `tim-bankrupt-assets` as primary** (was a push-scope workaround) | Main-repo Pages for images is cleaner (atomic, no cross-repo sync); fixes the asset-URL contradiction |
| Schedule storage | **Derived, never persisted** — calendar = pure fn(approved posts + `schedule.yml`) | Kills calendar-vs-queue drift; queue YAML stays the only SSoT |
| Token | **Regenerate the System User token as non-expiring** (drop refresh); `doctor` reads real `expires_at` + warns <14d | **Evidence** (`debug_token` on the SAVED token): it is **60-day** (`expires_at` = issued+60d ≈ 2026-08-24) → it WILL silently die, but a refresh job is the wrong fix; non-expiring regen (uncheck the 60-day box) matches the original design intent |

## 1. Data model — `Post → [Asset]`
**Post** (the queue row / publish unit): `id` · `schema_version` · `status` · `media_type`
(`image|carousel|reels|story`) · `publish_at` · **`assets: [Asset]`** (ordered) · `caption` · `hashtags[]` ·
`location_id` · `share_to_feed`(reels) · `audio_name`(reels) · `collaborators[]` · **`schedule_mode`** (auto|pinned|hold) ·
`priority` · `approved_at` · `schema_version` · **`result`** (runner-written).

**Asset** (per-asset / per-carousel-child — mirrors the Graph container-create shape):
`kind`(`image|video`) · `key` (host-agnostic asset key → adapter resolves to local path AND public URL) ·
`alt_text`(image) · `user_tags[]`(image) · `cover`(video) · `thumb_offset_ms`(video) ·
**`provenance`**`{mj_prompt, sref, sv, params, lut, source_image, model}` (PER-asset) · `result{container_id}`.

**Result** (per-post, with a retry envelope): `container_id` · `media_id` (idempotency key, set immediately) ·
`permalink` · `published_at` · `error` · `error_class` · `retry_count` · `next_retry_at` · `attempts[]`.

Key cuts: **per-asset** `alt_text`/`user_tags`/`provenance` (the API sets these at child-create time; a 10-child
carousel needs them per child). `media_type` is a **pure discriminator**. `STORY`/`REELS` need no new container —
a Story is `assets:[1]`, a Reel is `assets:[1 video]`. Plain feed `VIDEO` folds into `REELS`.

## 2. Storage, folder layout, naming
```
automation/
  assets/         # TRACKED images served by main-repo GitHub Pages
    <id>/01.jpg 02.jpg ...
  video/          # (DEFERRED to FULL) MP4 staging — BINARIES git-ignored; uploaded.json (R2 url+provenance) TRACKED
    <id>/clip.mp4  <id>/cover.jpg  <id>/uploaded.json
  queue/          # per-post YAML (one file = one post); the order/schedule/provenance SSoT
  published/<id>.yml          # flat archive (write-back: media_id/permalink/insights)
  igpub/          # core package
  config.yml      # account + per-media-type host map (gitignored)
  schedule.yml    # cadence policy (committed — editorial, version-worthy)
```
- **post-id = `YYYY-MM-DD_<slug>`** = the spine (queue filename, asset folder, provenance key). Sorts chronologically, collision-safe.
- `outputs/` (existing) = the **generation pool** (raw/graded keepers, binaries gitignored) — distinct from `automation/assets/` (the small, public, served subset). Keep both; different visibility/lifecycle.
- Host map (config): `host.image = {kind: github_pages, pages_base: https://yukittm.github.io/midjourney-explore}` (**main-repo Pages, source = branch `/` root** → URL = `pages_base + "/" + key`) · `host.video = {kind: r2, public_base: ...}` (added with video). **Per-host key→path resolution** (the adapter owns it): an image key **IS** the repo path (`automation/assets/<id>/01.jpg` → local = same, URL tail = same); a video key (`<id>/clip.mp4`) → local `automation/video/<id>/clip.mp4`, URL = `public_base + "/" + key`. The validator resolves the local path **per host** (so it can probe the real file) **and** asserts the URL tail — closing the silent-404 hole for BOTH hosts.

## 3. Scheduling — derived calendar
- **`schedule.yml`**: `slots[]` (HH:MM local + weekday filter + allowed media_types), `rate{max_per_24h, min_gap_minutes}`, `horizon_days`, `blackout[]` (YYYY-MM-DD dates to skip). Wall-clock + IANA `timezone` (DST-correct).
- **3 modes** (`Post.schedule_mode`): **pinned** (human `publish_at`, frozen, a hard reservation) · **auto** (default; assigner computes `publish_at`) · **hold** (excluded from calendar + publish). Pins are constraints the one assigner respects → no competing systems. (hold is a *mode*, not a status — orthogonal to the status lifecycle.)
- **`assign_slots(posts, schedule, now) → Plan`** = pure function: FIFO over `(priority, approved_at, filename)`, fill first free future slot that respects occupancy + rolling-24h cap + min_gap + media_type + blackout. Idempotent; the only writer of `publish_at` for autos. Reorder/insert = a one-line `priority`/`mode` edit, then re-plan.
- **Status lifecycle**: `draft → approved(unscheduled) → scheduled → publishing → published|failed` (hold is the orthogonal `schedule_mode`, above). The **approved-vs-scheduled split** makes "approved but never scheduled" a *visible, warned* backlog (not a silent dead post). `is_due` checks `status==scheduled && schedule_mode!=hold && publish_at(tz-aware)≤now`.
- **Retry**: `error_class` (transient/rate_limit/container_error/host_unreachable/fatal) → policy (backoff×3 / defer / 1-rebuild / short-retry / no-retry+alert). `media_id` short-circuit keeps retries idempotent.

## 4. Graph call-shape per type (what `graph.py`/`publish.py` build)
`POST /{ig-user-id}/media` (create container) → poll `status_code=FINISHED` (video/carousel/reels) → `POST /media_publish`.
| Type | Calls | Params |
|---|---|---|
| IMAGE | 1 | `image_url`, `caption`(+#tags), `alt_text`, `user_tags`, `location_id` |
| CAROUSEL | N children + 1 parent | child image: `image_url,is_carousel_item,alt_text,user_tags` · child video: `media_type=REELS,video_url,is_carousel_item` · parent: `media_type=CAROUSEL,children=<ids in asset order>,caption,collaborators` |
| REELS | 1 | `media_type=REELS,video_url,caption,cover_url\|thumb_offset,share_to_feed,audio_name,collaborators` |
| STORY | 1 | `media_type=STORIES,image_url\|video_url` (no caption/alt/stickers via API) |

## 5. Validation (commit-time, type-dispatched)
image: 1 image asset, JPEG, 4:5..1.91:1 · carousel: 2–10, image/video mix, **all children must share ONE aspect ratio → HARD REJECT on mismatch** (else IG silently crops every child to child-1's AR), video child needs cover/thumb · reels: 1 video, 9:16, MP4 H264+AAC, 5–90s · story: 1 asset, caption/hashtags forbidden. Cross: caption+#tags ≤2200, #≤30, @≤20, no leading `#`; ext matches `kind`; `alt_text/user_tags` image-only; video meta via injectable `read_video_meta` (ffprobe, degrades gracefully in CI).

## 6. Must-fix holes (status: ✓=shipped in MINIMAL · ⏭=deferred to FULL)
1. ✓ **Asset-key↔URL contract** (was 404 in prod): host-agnostic `key`; the adapter derives the URL **deterministically** (`pages_base + "/" + key`) and the validator resolves+probes the local file **per host** (image: key=repo path; video: `automation/video/`+key). (No separate "tail-match assertion" — the derivation is one function, so there is nothing to drift.)
2. ✓ **schema_version** on every record → forward migration of the permanent audit trail.
3. ✓/⏭ **Atomicity/double-post**: `container_id` is **saved before** `media_publish`; `media_id` written immediately. **MINIMAL: a stale `publishing`-row that already has a `container_id` is REFUSED on re-run** (it may be live → manual reconcile: check IG, set `media_id` by hand) — turns the crash-window into a safe STOP, not a double-post. ⏭ **FULL:** `run-lock` + claim-via-rename (Phase-1 concurrent clocks) and `reconcile.py` (auto-match recent media by caption + ~10-min `published_at` window).
4. ✓ **Pre-publish reachability probe** (HEAD; 2xx/3xx=reachable, 4xx/5xx=not-yet-propagated→retriable, network-error=fail-open) before the first Graph call. (⏭ content-type check → FULL.)
5. ✓ **tz-aware `publish_at` required** (`is_due` rejects naive + catches `ValueError`/`TypeError`; the runners coerce a naive `--now` to UTC) → no 3am crash.
6. ✓ **Caption length**: validator length-checks the **same assembled string** (`assemble_caption`) the publisher sends.
7. ✓ **`id` uniqueness** across queue ∪ published (`validate.py` runner via `duplicate_ids`); `move_to_published` **refuses to overwrite** an existing published record (`FileExistsError`).
8. ✓ **Rate limit read live** (`content_publishing_limit`) + a conservative self-cap (`DAILY_LIMIT`); the scheduler's per-24h cap is a ±24h approximation **backstopped** by this publish-time pre-check.
9. ⏭ **Token**: the action is **regenerate non-expiring** (uncheck the 60-day box) — NOT a refresh job. (Saved token verified **60-day** via `debug_token`, ≈ 2026-08-24.) A 20-line `doctor` (read `expires_at` + warn <14d) is **optional/deferred in MINIMAL**.

## 7. Extensibility seams (future need → the seam)
multiple accounts → `account` field + per-account token (default `primary`) · video/reels/story → already in the asset model + per-type poll budget · host swap (R2/Cloudinary/tunnel) → `AssetHost` adapter + config `kind` · scheduler swap → thin `publish.py` + run-lock contract · drafts/far-ahead → `status:draft` + horizon · cross-post (Threads) → `targets[]` + **`results` as a per-target map** (migrate via schema_version) · analytics write-back (reach/saves → selection) → `insights{}` on published record + a read-only `collect_insights` caller · delete/unpublish → `Status.deleted` + `graph.delete(media_id)`.

## 8. Build plan (additive; the core publish loop keeps its shape)
`models.py` (add `Asset`/`Provenance`; `Post.assets`; `STORY`; `schedule`/`priority`/`approved_at`/`schema_version`; result retry-envelope; back-compat `from_dict` synthesizing assets from old `images`) · `schedule.py` (NEW: load schedule.yml + `assign_slots` pure + `Plan.render`) · `validate.py` (type-dispatched) · `imaging.py` (video meta reader) · `graph.py` (reels/story/video-child containers + alt_text/user_tags/location params) · `publish.py` (`_build_containers` dispatch; `is_due`→SCHEDULED **+ migrate old `approved`+`publish_at`→`scheduled`, `approved` w/o `publish_at`→`approved` backlog**; **`--id` refuses `draft`/`hold`/already-`published`**; catch naive-`datetime` `TypeError`; pre-publish HEAD reachability probe; retry hook) · the 3 thin root CLIs `validate.py`/`plan.py`/`publish.py` (NEW; no single `cli.py`) · infra: **`config.yml` pages_base→main-repo Pages**, **`.gitignore` `automation/video/**/*.mp4|*.mov`**, **enable Pages (source `/` root)** · `schedule.yml`+`config.example.yml`+`_EXAMPLE.yml` (rewrite to `assets:`) · docs (this + `ig-publish-pipeline.md` + `outputs/README.md`). **Deferred to FULL:** `reconcile.py`, R2 host + `upload_video`, full `error_class` taxonomy, the rest of the CLI.

## 9. Items to verify (most RESOLVED post-launch, 2026-06-27)
- ✅ Graph field-exactness: `content_publishing_limit` shape confirmed live (100/24h); `alt_text`-per-child + carousel-video-child=`REELS` confirmed.
- ✅ Host: main-repo Pages **live** (source = branch `/` root; serving `automation/assets/`, HTTP-200 verified on 2 posts); `tim-bankrupt-assets` no longer primary. R2 (user-auth) still deferred until video starts.
- ⏳ **Token — STILL OPEN:** 2 posts published on the saved **60-day** token; regenerate non-expiring before ≈ 2026-08-24 (2-min Business-Settings step).
- `result` cardinality: **RESOLVED → single + retry-envelope now**; migrate to a per-target map via `schema_version` only when Threads/cross-post is actually built (a per-target map today = YAGNI for one account).

## 10. MINIMAL (now) vs FULL (deferred)
**MINIMAL — ships the first posts (images + carousels; no video):** `Asset`/`Provenance` model + `Post.assets` + `STORY` enum + `schema_version` + back-compat `from_dict` (synthesize assets from old `images`; the approved→scheduled migration) · `schedule.py` (`assign_slots` pure + `plan`) · type-dispatched `validate.py` (image/carousel; hard-reject mixed AR; `duplicate_ids`) · `publish.py` (`is_due`→SCHEDULED + `id_publishable` `--id` gate + `TypeError`-safe + HEAD probe + **stale-`publishing` STOP** + container-id-saved-before-publish; `move_to_published` no-overwrite) · runners coerce naive `--now`→UTC · raise the rate self-cap · **non-expiring token** (regen) + optional 20-line `doctor` · infra fixes (config pages_base, `.gitignore` video, Pages root). CLI subset: the 3 root scripts `validate.py` + `plan.py` + `publish.py`. **Status: implemented + independently cross-checked (3 review agents → blockers fixed); 75 tests green (3 yaml round-trip skipped locally → CI); validated in production on 2 published posts (2026-06-25, 2026-06-27).**
**FULL — when video/Reels or scale actually arrives:** R2 host adapter + `upload_video` + `automation/video/` lane + `uploaded.json` · `reconcile.py` · full `error_class` taxonomy + retry policies · the rest of the CLI (`new/status/calendar/hold/pin/doctor`) · `targets[]` + per-target `results` map (cross-post) · `insights{}` write-back.
