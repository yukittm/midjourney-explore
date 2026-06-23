---
name: mj-api-automation-state
description: As of June 2026, Midjourney has NO public API (Enterprise API still "investigating" since 2025-07); automation = unofficial APIs (PiAPI/GoAPI/ImaginePro/useapi) which wrap Discord/web, ToS-violating
metadata:
  type: reference
---

State of Midjourney programmatic access / editing automation, verified June 2026:

- **No official public API.** Midjourney Enterprise API has been "starting to investigate" since 2025-07-16 (updates.midjourney.com/enterprise-api-survey/) — still application-only, no GA, no public keys, enterprise-targeted. Source: https://updates.midjourney.com/enterprise-api-survey/
- **Web app is primary interface.** midjourney.com (not Discord) is primary since ~2024; has prompt bar, gallery, Explore feed, and the in-canvas **Editor** (inpaint/Repaint, Pan, Zoom Out, Remix) + **Retexture** (reskin geometry, keep composition).
- **V8.1**: default since 2026-06-10, released 2026-04-30. Caveat: V8.1 images CAN be put in the Editor, but Editor still runs on **V6.1** internally; Discord "Vary Region" is NOT available on V8.1 images (must use web Editor). MJ roadmap: "moving onto V8 edit, inpainting, outpainting model upgrades" (not yet shipped).
- **Retexture access-gated**: needs 10k+ images generated OR yearly membership OR 12 consecutive monthly months.
- **Editing IS scriptable via unofficial APIs**: PiAPI exposes Imagine/Upscale/Variation/Reroll/Describe/Seed/Blend/**Inpaint**/**Outpaint**/**Pan**. Inpaint endpoint takes `origin_task_id` + base64 `mask` (not GUI brush) + optional `prompt` → fully headless, no human brush needed. Retexture specifically is NOT a clearly-exposed unofficial endpoint (inpaint/zoom/pan are; retexture is web-Editor-only as of search).
- **Unofficial APIs wrap Discord-bot/browser-emulation against a real MJ account → violate MJ ToS → account-ban risk.** This is the gray area. Hosted-account variants (PiAPI hosted, useapi flat $10/mo) shift the ToS risk to the provider's farmed accounts.
- See [[web-access-constraints]] for source-reachability notes (docs.midjourney 403, updates.midjourney OK).
