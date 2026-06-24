---
name: mj-sv-style-reference-version
description: The correct --sv (style reference version) story on Midjourney V8.1 — overturns the doc's "sv7 rejected, omit sv" claim
metadata:
  type: reference
---

Web-verified 2026-06-23 across docs.midjourney.com (Style Reference article, via search snippets), updates.midjourney.com (V8 Alpha / V8.1-default posts), blakecrosley.com, geekycuriosity.substack.com. High confidence.

**`--sv 7` is the DEFAULT style-reference / moodboard version on the V8 family (incl. V8.1) — NOT rejected.** The recurring authoritative sentence: the new sref/moodboard version `--sv 7` is "4x faster and 4x cheaper than the previous version, and supports `--hd`, `--p`, `--stylize`, and `--exp`." So on V8.1 an image `--sref` runs on `--sv 7` by default AND is `--hd`-compatible.

Valid `--sv` on the V8 family: **only `--sv 6` and `--sv 7`** (1–5 incompatible). Niji 7 only supports `--sv 6`.

**Resolving the "Unsupported Style Reference version 7 for --version 8.1" in-app error (2026-06-23):** that error is a CONTEXT mismatch, not "sv7 is banned on V8.1." `--sv 7` does NOT work with numeric/random sref CODES — random/numeric codes accept only `--sv 4` (legacy) or `--sv 6`. `--sv 7` works with **image-URL srefs** (and codes designed for it). The live error almost certainly came from pairing `--sv 7` with a numeric code (or a `--sv`/version desync), not from V8.1 forbidding sv7.

Practical rule for THIS project (image-URL sref on V8.1): you may **omit `--sv`** (default = sv7, which is what you want) OR explicitly set `--sv 7` — both are correct and `--hd`-compatible. The doc's "OMIT `--sv` because sv7 is rejected and sv6 breaks --hd" reasoning is WRONG even though "omit `--sv`" happens to land on the right behavior.

`--sv 4` = legacy V6/pre-2025-06-16 code algorithm; using it interprets codes via the old system (associated with V7-era). `--sv 6` = V6.1 algorithm, works with codes. See [[mj-v81-key-facts]].
