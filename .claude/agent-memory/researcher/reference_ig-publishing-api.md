---
name: ig-publishing-api
description: IG Content Publishing API facts for the project's automation goal — self-owned account stays in Dev mode WITHOUT App Review; publish flow, limits, tokens, hosting
metadata:
  type: reference
---

For the project's "auto-publish curated MJ outputs to IG" goal (CLAUDE.md), the Meta Graph API Content Publishing path:

- **App Review NOT required for own-account-only automation.** An app that uses a self-token and only ever touches the *owner's own* IG account stays in **Development mode** indefinitely and needs no App Review and no Business Verification. App Review + **Advanced Access** are only needed to publish to accounts you don't own/manage. The owner must hold a role (admin/developer/Instagram Tester) on the app. This is the load-bearing setup answer — single-user owner-posting is the easy path. (Sources: zernio.com/blog/instagram-api, postproxy, Meta overview docs, fetched 2026-06-24.)
- **Permission renames (Jan 27 2025):** old `instagram_basic` / `instagram_content_publish` → new `instagram_business_basic` / `instagram_business_content_publish`. Basic Display API fully shut down (Dec 4 2024 / Sept 2024 per source) — dead, do not use.
- **Publish flow:** `POST /{ig-user-id}/media` (image_url + caption [+ optional alt_text, added 2025-03-24]) returns a container ID → `POST /{ig-user-id}/media_publish` with creation_id. **Image must be a public URL** (no binary upload). **JPEG only** (no PNG/WebP/GIF). Feed aspect ratio 4:5 → 1.91:1 (1:1 ok). Caption ≤ 2,200 chars, ≤ 30 hashtags.
- **Formats:** single image, video, **Reels** (`media_type=REELS`, video_url), **carousel** (child containers `is_carousel_item=true` → parent `media_type=CAROUSEL` + children list; max 10 items), **Stories** (`media_type=STORIES`). All same 2-step flow.
- **Rate limit:** ~**25 published posts / rolling 24h** per IG account (some secondary sources say 50 or 100 — 25 is the most-cited current figure; carousel = 1 post). Query `GET /{ig-user-id}/content_publishing_limit` for live usage.
- **Tokens:** long-lived user token = **60 days**, no auto-refresh; refresh a token ≥24h old via `GET graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token`; expired-past-60d = full re-auth. For unattended automation prefer a **Meta System User token** (Business Settings → Users → System Users, Admin role, can be **non-expiring**) — best fit for this project's set-and-forget goal.
- **Make.com** has native IG-for-Business modules wrapping this exact flow (OAuth connection, same 2 permissions). **Buffer/Later** are managed alternatives — both auto-publish Reels + carousels (≤10 imgs); Reels with licensed music/AR may fall back to reminder-only (Meta API limit, affects all tools).
- **Image hosting** for the public URL: Cloudinary (generous free tier, common choice), S3 (watch signed-URL ~1h expiry), GitHub Pages (stable public URLs, good for a personal repo-based pipeline). Avoid Google Drive/Dropbox "share" links and imgur — not reliably direct-servable JPEGs.

See [[web-access-constraints]] — Meta developers.facebook.com pages return only nav chrome on WebFetch; use search snippets / secondary sources (zernio, postproxy, elfsight) for verbatim wording.
