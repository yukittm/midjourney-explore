---
updated: 2026-06-25
status: draft
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
- **Account:** IG Business/Creator + linked FB Page, **OWN account** → **no App Review** (app stays in Development mode, Standard Access); **non-expiring System User token** (no 60-day refresh machinery).
- **Image host = Cloudflare R2 + custom domain** — the #1 invariant, fixed now. NOT Notion (file URLs expire in ~1h → Graph fetch fails), NOT bare `r2.dev` (rate-limited), NOT S3 presigned (expire). GitHub Pages = low-volume fallback only.
- **Phasing:** Phase 0 = manual (run by hand / current status quo) · Phase 1 = scheduled-auto.
- **Clock = decided at build time** — Hetzner VPS cron (~$4.6/mo; Phase 0→1 is a true "add a crontab line" swap) **vs** AWS Lambda + EventBridge (free, 99.99% SLA, but a runtime port, not a swap). **NOT** GitHub Actions cron (10–30 min+ delays, dropped at peak, silent **60-day idle auto-disable**); **NOT** local-cron-alone (only fires when the Mac is awake).

## Components
- **Queue** — one **YAML file per post**: `automation/queue/<YYYY-MM-DD>_<slug>.yml`. **Approval = a commit** that sets `status: approved` + `publish_at`. On success the file moves to `automation/published/`. **git history = the approval/audit trail.**
- **Assets** — final graded JPEGs uploaded to **R2** (public, served via custom domain). The queue file holds the public R2 URL(s).
- **Publisher** — `automation/publish.py` (~100 lines, Python + `requests`). For each **due + approved** item:
  1. create media container(s) (`POST /{ig-user-id}/media`, `image_url` = R2 URL + caption; carousel = N child containers → 1 parent `media_type=CAROUSEL`);
  2. for carousel/Reels, **poll `status_code` with backoff + a hard timeout**; treat **`ERROR`/`EXPIRED`/timeout as a failed post that alerts** (never an unbounded loop);
  3. `POST /{ig-user-id}/media_publish`;
  4. **write the returned `media_id` immediately** = the **idempotency key** (on startup, skip any record that already has a `media_id`; the file-move is cosmetic, not the dedupe guarantee);
  5. flip `status: published` / move file; **ping a healthcheck URL** (dead-man's-switch).
  - **Pre-check `GET /{ig-user-id}/content_publishing_limit`** before publishing; defer if the ~25/24h quota is exhausted (matters when flushing a backlog).
- **Validation** — `automation/validate.py`, run as a **pre-commit hook / CI check on the queue file** (NOT only at runtime): caption ≤2200 chars, ≤30 hashtags, carousel ≤10, **aspect 4:5–1.91:1** (read JPEG dims), JPEG-only, required fields + URLs present. A bad post is rejected **at approval**, not at 3am.
- **Secrets** — the non-expiring System User token lives in **macOS Keychain** (Phase 0) / the **clock-host's secret store** (Phase 1) — never a committed file; **scrub `access_token` from all logs**; `.gitignore` + a `gitleaks` guard.
- **Monitoring** — failures write `error` to the record + send an email alert; the **healthcheck ping** (e.g. healthchecks.io free) fires an alert if the runner goes silent. This single mitigation closes DIY's only real gap vs a managed SaaS.

## Queue schema (per-post YAML)
`id` · `status` (draft→approved→publishing→published|failed) · `media_type` (image|carousel|reels) ·
`publish_at` (ISO 8601 + TZ) · `image_urls` (R2) · `caption` (≤2200) · `hashtags` (≤30) · `alt_text` ·
`provenance` {mj_prompt, sref, lut} · `result` {container_id, media_id, published_at, error}.

## Scope & caveats
- **The auto-pipeline covers: single images + carousels (≤10) + silent / pre-baked-audio Reels.**
- **Trending/licensed-audio Reels CANNOT be auto-published via ANY API** (Graph or Buffer). → Those **stay manual** (native app). The marketing strategy's "Reels-first cold start" → **cold-start trending-audio Reels are manual for now**; the pipeline carries images/carousels (+ silent Reels). See [[../docs/marketing/ig-growth-strategy]].
- Rate limit ~25/24h shared across formats (pre-checked); carousel ≤10 is an API-wide cap.

## Data flow
```
[Claude] prompts + draft captions ─► you run Midjourney (browser) ─► select keepers ─► (opt) LUT grade
                                                                                  │ final JPEG
                                                                                  ▼
                                                  upload to Cloudflare R2 (public, custom domain)
                                                                                  │ public JPEG URL
                                                                                  ▼
        commit  automation/queue/<id>.yml  (image_urls + caption + #tags + publish_at, status: draft)
                                                                                  │
                        pre-commit/CI validate.py (caption/hashtags/aspect/JPEG)  │ must pass
                                                                                  ▼
                       ── HUMAN APPROVES ──► commit  status: approved   ◄── THE GATE (git history = audit)
                                                                                  │
   Phase 0: you run `python publish.py` by hand   │   Phase 1: VPS cron / Lambda fires publish.py
                                                                                  ▼
   publish.py: content_publishing_limit pre-check → create container → poll (bounded, handle ERROR/EXPIRED)
   → media_publish → write media_id (idempotency) → status: published / move file → healthcheck ping
                                          (on any failure → status: failed + error + email alert)
                                                                                  ▼
                                                            Instagram (owner's own account)
```

## Build roadmap
**Phase 0 — manual (build the durable core; publishing stays by-hand meanwhile):**
1. *(assistant)* scaffold `automation/{queue,published}/`, `config.yml`, the YAML schema; `.gitignore` + gitleaks.
2. *(assistant)* `publish.py` + `validate.py` + a CI validation workflow.
3. *(user — auth only)* Meta: confirm IG↔Page link; create a **System User**; generate the **non-expiring token** with `instagram_business_basic` + `instagram_business_content_publish` (+ `pages_show_list`, `business_management`); record the IG user ID.
4. *(user)* Cloudflare **R2** bucket + **custom domain**; confirm a public JPEG URL fetches as raw bytes. *(Needs a domain — ~$10/yr if not already owned.)*
5. *(user + assistant)* Phase-0 test: hand-run `publish.py` on one approved post → verify it goes live, the write-back lands, and a deliberate bad URL hits the failed+alert path.

**Phase 1 — scheduled-auto (flip the clock):**
6. *(decide at build time)* clock = Hetzner VPS cron **or** AWS Lambda+EventBridge; deploy `publish.py` there; token in the host's secret store; wire the healthcheck.
7. flip to scheduled; verify auto-publish from the approved queue; **rollback = disable the clock** (manual path still works).

## Open decisions / dependencies
- **Clock** (VPS vs Lambda) — at build time.
- **Custom domain for R2** — need a domain (~$10/yr) or reuse an existing one. **Confirm before Phase 0 step 4.**
- **Healthcheck service** — free (healthchecks.io or similar).

## Cost
R2 free tier · Graph API free · Python free · **clock = ~$4.6/mo (VPS) or $0 (Lambda)** · domain ~$10/yr if not owned. **No paid external API is called without explicit consent.**
