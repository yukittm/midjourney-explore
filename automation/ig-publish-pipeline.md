---
updated: 2026-06-27
status: active
type: design
---

# IG Auto-Publish Pipeline — Design (Option 1: self-owned DIY)

> **Decided 2026-06-25.** Chosen over the no-code path (Notion + Make.com) per the user's distrust of
> connectors as runtime infrastructure. Backed by 4 independent agent designs + 1 adversarial
> cross-check (2026-06-24/25). **Manual-first → scheduled-auto**; the **human approves the queue**; the
> **user does all auth**; the **assistant never enters credentials**.

## Locked decisions
- **Self-owned DIY**: git-file queue + a small Python publisher + own host + own clock. **No connector on the publish path.**
- **Trigger (locked):** fully **scheduled auto-publish from a human-APPROVED queue**.
- **Account:** IG Business/Creator + linked FB Page, **OWN account** → **no App Review** (app stays in Development mode, Standard Access); **non-expiring System User token** (no 60-day refresh machinery). *(Status 2026-06-27: the token in use today is a **60-day** one, ≈2026-08-24 — confirm/regen non-expiring before then; see `.claude/PROGRESS.md`.)*
- **Image host = GitHub Pages** (decided 2026-06-25) — images committed to the **public main repo**, served at `https://<user>.github.io/<repo>/...`. Chosen for **$0 / no domain / no extra account / no upload step / permanent URL / git-versioned provenance** (image + queue + provenance in one commit). **Swappable via the host adapter** — R2 (free `r2.dev` or +custom domain) or Cloudinary later, **especially for video/Reels** (Pages is weak for video). NOT Notion (URLs expire ~1h → Graph fetch fails), NOT S3 presigned (expire).
- **Phasing:** Phase 0 = manual hand-run — **DONE** (2 published posts, 2026-06-25 / 06-27). Phase 1 = scheduled-auto via **local launchd** (decided 2026-06-29; deploy artifacts built in `automation/deploy/`) — the intended operating mode (the user wants minimum unattended auto-publish, not a manual cadence).
- **Clock = local launchd (decided 2026-06-29), $0.** Minimum unattended auto-publish, no new account/host; the wrapper handles git-persistence. **Upgrade path (still $0): Oracle Cloud Always-Free VM** under cron if always-on is needed (host-agnostic script, no code change). Alternatives weighed + rejected: AWS Lambda + EventBridge (free + always-on but a runtime port + more setup) — viable later; Hetzner VPS cron (~$4.6/mo — costs money, the Oracle free VM dominates it); **NOT** GitHub Actions cron (10–30 min+ delays, dropped at peak, silent **60-day idle auto-disable**).

## Components
- **Queue** — one **YAML file per post**: `automation/queue/<YYYY-MM-DD>_<slug>.yml`. **Approval = a commit** that sets `status: approved` + `publish_at`. On success the file moves to `automation/published/`. **git history = the approval/audit trail.**
- **Assets** — final graded JPEGs committed under `automation/assets/<id>/` and served by **GitHub Pages**. The queue file holds repo-relative asset keys; the host adapter derives the public Pages URL (`igpub/hosting.py`).
- **Publisher** — `automation/publish.py` (~100 lines, Python + `requests`). For each **due + approved** item:
  1. create media container(s) (`POST /{ig-user-id}/media`, `image_url` = the host's public Pages URL + caption; carousel = N child containers → 1 parent `media_type=CAROUSEL`);
  2. for carousel/Reels, **poll `status_code` with backoff + a hard timeout**; treat **`ERROR`/`EXPIRED`/timeout as a failed post that alerts** (never an unbounded loop);
  3. `POST /{ig-user-id}/media_publish`;
  4. **write the returned `media_id` immediately** = the **idempotency key** (on startup, skip any record that already has a `media_id`; the file-move is cosmetic, not the dedupe guarantee);
  5. flip `status: published` / move file; **ping a healthcheck URL** (dead-man's-switch).
  - **Pre-check `GET /{ig-user-id}/content_publishing_limit`** before publishing; defer if the ~100/24h quota is exhausted (matters when flushing a backlog).
- **Validation** — `automation/validate.py`, run as a **pre-commit hook / CI check on the queue file** (NOT only at runtime): caption ≤2200 chars, ≤30 hashtags, carousel ≤10, **aspect 4:5–1.91:1** (read JPEG dims), JPEG-only, required fields + URLs present. A bad post is rejected **at approval**, not at 3am.
- **Secrets** — the non-expiring System User token lives in the **`IG_SYSTEM_USER_TOKEN` env var** (from `automation/.env`, gitignored + chmod 600; sourced by the launchd wrapper in Phase 1) — never a committed file; the headless `git push` uses a **`GIT_PUSH_TOKEN`** (fine-grained GitHub PAT) in the same `.env`; **scrub `access_token` from all logs** (the Graph client never logs it); `.gitignore` + a **CI secret-scan** (`.github/workflows/validate.yml`: Meta token-pattern + `.env`/`config.yml`-not-tracked).
- **Monitoring** — failures write `error` to the record + send an email alert; the **healthcheck ping** (e.g. healthchecks.io free) fires an alert if the runner goes silent. This single mitigation closes DIY's only real gap vs a managed SaaS.

## Queue schema (per-post YAML)
A post is an ordered list of `assets` discriminated by `media_type`. Full spec + per-type examples:
[`asset-queue-model.md`](asset-queue-model.md).
`id` · `schema_version` · `status` (draft→approved→scheduled→publishing→published|failed) ·
`media_type` (image|carousel|reels|story) · `publish_at` (ISO 8601 + offset; set by `plan.py` for auto posts) ·
`schedule_mode` (auto|pinned|hold) · `priority` · `assets` [{kind, key, alt_text, user_tags, provenance}] ·
`caption` (≤2200) · `hashtags` (≤30) · `result` {container_id, media_id, permalink, published_at, error}.
The calendar is **DERIVED** from approved posts + `schedule.yml` (run `automation/plan.py`); the queue stays the SSoT.

## Scope & caveats
- **The auto-pipeline covers: single images + carousels (≤10) + silent / pre-baked-audio Reels.**
- **Trending/licensed-audio Reels CANNOT be auto-published via ANY API** (Graph or Buffer). → Those **stay manual** (native app). The marketing strategy's "Reels-first cold start" → **cold-start trending-audio Reels are manual for now**; the pipeline carries images/carousels (+ silent Reels). See [[../docs/marketing/ig-growth-strategy]].
- Rate limit ~100/24h shared across formats (pre-checked); carousel ≤10 is an API-wide cap.

## Data flow
```
[Claude] prompts + draft captions ─► you run Midjourney (browser) ─► select keepers ─► (opt) LUT grade
                                                                                  │ final JPEG
                                                                                  ▼
                                       commit JPEG under automation/assets/ (served by GitHub Pages)
                                                                                  │ public JPEG URL
                                                                                  ▼
        commit  automation/queue/<id>.yml  (image_urls + caption + #tags + publish_at, status: draft)
                                                                                  │
                        pre-commit/CI validate.py (caption/hashtags/aspect/JPEG)  │ must pass
                                                                                  ▼
                       ── HUMAN APPROVES ──► commit  status: approved   ◄── THE GATE (git history = audit)
                                                                                  │
   Phase 0: you run `python publish.py` by hand   │   Phase 1: launchd runs run_publish.sh (publish + commit/push)
                                                                                  ▼
   publish.py: content_publishing_limit pre-check → create container → poll (bounded, handle ERROR/EXPIRED)
   → media_publish → write media_id (idempotency) → status: published / move file → healthcheck ping
                                          (on any failure → status: failed + error + email alert)
                                                                                  ▼
                                                            Instagram (owner's own account)
```

## Extensibility & UI-readiness
MVP ships **headless** (git queue + CLI), but the architecture stays **UI-ready** so a front-end can be
added later **without reworking the core**. Standing principle for this project: **clean, flexible,
low-maintenance design** that makes customization and a future UI a bolt-on, not a rewrite.
- **Layered** — a headless core package `automation/igpub/` (models · queue read/write · validate ·
  Graph publish · status transitions) with **no interface assumptions**, behind a small stable internal
  API. `publish.py` / `validate.py` are **thin CLI callers**; a future UI (local web app, TUI, or a
  read-only dashboard) is **another thin caller of the same core** → zero core changes.
- **Queue = the data contract** — the per-post YAML schema IS the API any front-end reads/writes; the
  git queue is the single source of truth **for now (Phase 0/1)**. See *Store roadmap* below — it is a
  phase store behind a future `QueueStore` seam, **not** a permanent invariant.
- **Side-effects behind adapters** — Graph API + the image-host (commit for Pages / upload for R2)
  each sit behind a small interface, so they are swappable + mockable (host/clock change without
  touching core logic; unit-testable). **Git persistence is an OPS concern, not app logic**: the
  deploy wrapper (`automation/deploy/run_publish.sh`) commits+pushes the queue→published move after a
  run — Python stays git-free. **Store access is NOT yet behind an adapter** (`queue.py` hardcodes
  the filesystem); extracting a `QueueStore` Protocol is the next architectural step before a hosted
  UI (see *Store roadmap*).

### Store roadmap
- **Phase 0/1 (now): git-YAML** — one Mac = one writer, so commits never race; git history = the
  audit trail; $0; assets+queue+provenance in one commit. Correct for the current scale; **do not
  migrate to a DB now** (over-engineering for ~1 post/day).
- **Next architectural step (before a hosted UI): a `QueueStore` Protocol** — mirror the existing
  `ImageHost`/`GraphClient` adapter pattern. Wrap today's filesystem logic as `FsQueueStore` and route
  all callers (`plan.py`, `publish.py`, `studio.py`, `scaffold.py`) through it. Cheap now (small
  surface, 130+ tests as a net), expensive later (every new caller deepens the coupling). This is the
  single highest-leverage future-proofing seam — both no-bias architecture audits ranked it #1.
- **At the hosted-UI milestone: a networked store** (e.g. Supabase = managed Postgres + Storage, free
  tier) implementing the same `QueueStore` Protocol — needed once a web UI becomes a *second writer*
  alongside the clock (git working-tree commits don't support concurrent writers). Swapping the store
  impl behind the seam = no core changes.
- **Config-driven** — account id, defaults, cadence in `config.yml` → behavior customizable without code edits.
- **Module boundaries** — `igpub/{models,queue,validate,publish,adapters}/` · `cli/` · (future) `web/`.
  Adding a UI = a new front-end module over the unchanged core.

## Build roadmap
**Phase 0 — ✅ DONE (durable core built; steps 1–5 complete; proven on 2 published posts 2026-06-25 + 2026-06-27; manual `publish.py` cadence ongoing):**
1. *(assistant)* scaffold `automation/{queue,published}/`, `config.yml`, the YAML schema; `.gitignore` + the CI secret-scan.
2. *(assistant)* `publish.py` + `validate.py` + a CI validation workflow.
3. *(user — auth only)* Meta: confirm IG↔Page link; create a **System User**; generate the **non-expiring token** with `instagram_business_basic` + `instagram_business_content_publish` (+ `pages_show_list`, `business_management`); record the IG user ID.
4. *(user)* Enable **GitHub Pages** on the (public) repo serving `automation/assets/`; confirm a sample JPEG URL fetches as raw bytes. *(No domain, $0.)*
5. *(user + assistant)* Phase-0 test: hand-run `publish.py` on one approved post → verify it goes live, the write-back lands, and a deliberate bad URL hits the failed+alert path.

**Phase 1 — scheduled-auto (flip the clock):**
- **Repo side DONE (2026-06-29):** `publish.py` (no `--id`) is already a due-poller; **human-like time spread** is implemented via a **`window:` slot** in `schedule.yml` (`window: ["08:00","23:30"]` JST → each day's post fires at a *deterministic-random* time inside the window — global audience, avoids JST deep night, not on the dot; written into `publish_at` so it's auditable). A fixed `time:` slot + the optional `jitter:` block is the alternative. No `publish.py` change is needed to go clock-driven.
- **Clock = local launchd, $0 (decided 2026-06-29).** Minimum unattended auto-publish with no new
  account/host. The deploy artifacts ship in `automation/deploy/`: `run_publish.sh` (flock + source
  `.env` + `publish.py` + **git add/commit/push** to persist the result), the launchd plist, and a
  setup `README.md`. **The git-persistence step closes a verified gap** — without it an auto-run would
  mutate local files that never reach GitHub/Pages.
- **BLOCKER before the standing clock runs unattended:** regenerate the token **non-expiring** (the
  saved one is 60-day, ≈2026-08-24) — a ~2-min Business-Settings step (user-only; assistant never
  touches the token). Until then the 60-day token works.
6. *(user)* set `GIT_PUSH_TOKEN` (fine-grained GitHub PAT, contents:write) in `automation/.env` for
   headless push; install the launchd agent (`automation/deploy/README.md`).
7. set `config.yml: healthcheck_url` (free healthchecks.io dead-man's-switch); the clock is now live;
   verify auto-publish from the approved queue; **rollback = `launchctl unload`** (manual path still
   works). *No fire-time human gate — approval = the commit that set `status: approved`.*
   - **Always-on upgrade (still $0):** move `run_publish.sh` to an Oracle Cloud Always-Free VM under
     cron — the script is host-agnostic, no code change. Needed only if the Mac-asleep delay matters.
   - *Deferred (not needed at 1/day, assets are pushed days ahead so Pages lag rarely bites): treating a HEAD-probe miss as keep-SCHEDULED-retry instead of FAILED. Revisit if a fire-time propagation lag actually causes a miss.*

## Open decisions / dependencies
- **Clock = local launchd (decided), $0** — Oracle Always-Free VM is the always-on upgrade if needed.
- **Host = GitHub Pages on the public main repo (decided)** — $0, no domain. The **video/Reels host is deferred** (Pages is weak for video) → R2/Cloudinary when auto-Reels lands.
- **Healthcheck service** — free (healthchecks.io or similar).

## Cost
GitHub Pages free · Graph API free · Python free · **clock = $0 (local launchd; Oracle Always-Free VM also $0 for always-on)** · **no domain needed**. **No paid external API is called without explicit consent.**
