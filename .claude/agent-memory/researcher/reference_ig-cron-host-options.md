---
name: ig-cron-host-options
description: Clock/host options for the once-daily IG auto-publish job (laptop-may-be-off, $0-5/mo, token-bearing) — winner/runner-up + verified 2026 facts
metadata:
  type: reference
---

For scheduling `automation/publish.py` (once/day, must run with laptop OFF, $0-5/mo, low ops). The job's only infra need: run Python on a schedule + inject ONE env var `IG_SYSTEM_USER_TOKEN` (verified `automation/igpub/config.py:20` reads env ONLY, never repo) → no host lock-in, migration is trivial. Token = Meta System User token, can be non-expiring (see [[ig-publishing-api]]).

Ranking (researched 2026-06, cite vendor pages on use):
- **WINNER: Hetzner CX22 VPS + system cron** (~€4.35/$5/mo; price adjust 15-Jun-2026). Runs existing Python unchanged, unconditional always-on, no cold-start/zip/rewrite. Secret = root-owned `/etc/igpub.env` chmod 600, cron does `set -a; . /etc/igpub.env; set +a` (NOT token in crontab line — visible via ps). Cost = small real bill + you patch the box.
- **RUNNER-UP: AWS Lambda + EventBridge SCHEDULER** (~$0 forever; Lambda perm free tier 1M req/mo). UPDATE 2026-06: EventBridge **Scheduler now has a PERMANENT 14M-invocation/mo free tier** (aws.amazon.com/eventbridge/pricing) — use Scheduler, NOT legacy Rules. (Old advice to prefer Rules "to avoid paid Scheduler" is OUTDATED; both are free at this scale, Scheduler is cleaner.) Secret = Lambda ENV VAR (free), NOT Secrets Manager ($0.40/secret/mo). Cost = zip Python+deps + AWS console setup + CARD required. NOTE: Lambda FS ephemeral → can't mutate git-YAML SSoT; needs SSoT→DynamoDB/S3 or git-push-back.
- **THIRD: Render cron** ($1/mo floor per job; native Python, dashboard env-var secret, managed-reliable). Cleanest no-own-a-box middle ground.

REJECTED / disqualified:
- **GitHub Actions cron** — STILL bad in 2025-26: 5-30min queue delays (no workaround, GitHub-side) + 60-day inactivity SILENT auto-disable (scheduled runs don't count as activity). Confirmed.
- **macOS launchd/cron** — fails hard req (laptop off/asleep = missed day). Keep only as local dry-run path.
- **Cloudflare Workers Cron** — free + reliable BUT Workers are JS/TS, Python needs Containers → rewrite, disqualifying.
- **cron-job.org / EasyCron** — free & reliable (cron-job.org 15+yr donation-funded) BUT only CALL a URL, don't run Python → need a separate HTTP host; a clock-for, not a host.
- Railway (cron less first-class, usage creep), Fly.io (no new-user free tier).

**$0 FULL-STACK host (UI + cron + secrets + persistence on ONE platform)** — researched 2026-06, distinct from clock-only ranking above. The git-YAML SSoT is the real constraint: it MUTATES on publish (move file + record media_id), so serverless ephemeral-FS hosts (Cloudflare/Vercel/Lambda/CloudRun) REQUIRE moving SSoT to a hosted store (KV/D1/R2/DynamoDB) or git-push-back. A VM keeps the git-file design unchanged.
- **CLOUDFLARE** = only listed platform doing UI+cron+secrets+persistence all free on one account, NO CARD. Pages(UI static) + Worker scheduled() (cron) + secrets(wrangler) + KV 1GB/D1 5GB/R2 zero-egress. CATCH: Workers JS/TS-native; Python = Pyodide OPEN BETA (python_workers flag, ~1s cold, requests via shim) → realistically rewrite just the publish path in JS, not all of igpub/. R2 could later replace GitHub Pages images.
- **ORACLE Always-Free VM** = only GENUINELY-FREE always-on VM; runs existing Python + system cron + git-file SSoT UNCHANGED. CATCH: card required; A1 halved to 2 OCPU/12GB (2026-06-15); ARM "Out of Capacity" common; you patch box + idle-reclaim risk.
- DEAD/degraded 2026: Fly.io (free tier removed, ~$2-5/mo min), Railway (no perm free, $5 trial then stops), Render (web sleeps 15min; cron PAID not free), PythonAnywhere (NEW accts post-2026-01-15 get NO scheduled tasks), Vercel Hobby (cron 1×/day only, random minute, Python 2nd-class), Deno Deploy (great free + Deno.cron but JS/TS ONLY). GCP CloudRun+Scheduler & AWS Lambda+Scheduler = $0 + run Python but CARD required + ephemeral FS.

**Jitter on post time**: NO API/ToS benefit — official Graph API treats scheduled == manual posts; "jitter helps look human" in the literature = scraping inter-request delays (0.8-3s), NOT publish timing. Engagement studies (Buffer 9.6M, RecurPost 2M) moved AWAY from exact-minute → audience-peak ~30min windows + consistency. Verdict: ±5-15min random jitter (`sleep(random.randint(0,900))` or off-round cron minute) is COSTLESS + mildly nicer "human feed" look, but FOLKLORE-adjacent, not evidence-backed. Don't over-build.
