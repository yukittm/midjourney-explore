# Auto-publish deployment (Phase 1, $0)

Unattended publishing of approved+due posts. **No manual publish step.** A clock (launchd on this
Mac) runs `run_publish.sh` every 60s; it publishes anything due and commits+pushes the result so
GitHub Pages and the remote record stay in sync.

```
clock (launchd, every 60s)
  └─ run_publish.sh  ── mkdir lock (single instance; macOS has no flock)
       ├─ source automation/.env            # IG token (+ optional GitHub push token)
       ├─ python automation/publish.py      # publishes DUE + status:approved posts
       └─ git add/commit/push               # ONLY if a post was actually published —
                                            # an idle tick ("nothing to publish") touches no git,
                                            # so it never sweeps in-progress queue edits
```

The human gate stays `status: approved` in the committed queue (set via Feed Studio). The clock
never publishes a draft. Scheduling = the derived calendar's window slot (`automation/schedule.yml`),
so posts fire at a human-ish minute inside the daytime window, not on a robotic boundary.

**Why poll every 60s, not every 15 min:** `publish_at` carries a jittered, human-ish minute (e.g.
`15:02`). A coarse poll would round the *actual* post time up to the next tick and throw the jitter
away; a 60s poll fires at the planned minute. It is free — when nothing is due the run is a
sub-second local file read with **no Graph API call** ([publish.py](../publish.py) only calls the API
once a post is actually due). `StartInterval` counts from load time, so ticks never land on a round
`:00` either.

---

## One-time setup

### 1. Secrets — `automation/.env` (gitignored, `chmod 600`)

```sh
IG_SYSTEM_USER_TOKEN=<Meta System User token>
GIT_PUSH_TOKEN=<GitHub fine-grained PAT, contents:write on yukittm/midjourney-explore>
```

- `IG_SYSTEM_USER_TOKEN` — already used by the manual path. **Regenerate as NON-EXPIRING before
  ≈2026-08-24** (the current 60-day token expires then; see token note below). Assistant never
  touches this — generate it in Meta Business Settings yourself.
- `GIT_PUSH_TOKEN` — needed for headless `git push` (a launchd job has no interactive git
  credentials). Create at GitHub → Settings → Developer settings → Fine-grained tokens, scoped to
  this one repo with **Contents: Read and write**. Without it the publish still happens and is
  committed locally, but the push fails (logged) until the next run with a token set.

### 1.5. macOS TCC — REQUIRED if the repo is under ~/Desktop, ~/Documents, or ~/Downloads

macOS protects those three folders: a launchd agent canNOT read files inside them by default, so
`run_publish.sh` fails with `Operation not permitted` (the job runs, but every tick errors). This repo
lives under `~/Desktop/`, so you must do ONE of:

- **Grant Full Disk Access to the interpreter** (fast): System Settings → Privacy & Security → Full
  Disk Access → `+` → `Cmd+Shift+G` → `/bin/bash` → add + enable. Then reload the agent
  (`launchctl bootout …` then `bootstrap …`, step 2). *Tradeoff: all bash scripts then get FDA.*
- **Move the repo off the protected folders** (cleaner, no special permission): e.g. `~/dev/…`, and
  update the two absolute paths in the plist. A future Linux host (Oracle VM) has no TCC at all.

Symptom check: `tail automation/deploy/igpub.log` shows `Operation not permitted` → TCC, not a code bug.

### 2. Install the launchd agent

Edit the two absolute paths in `com.tim-bankrupt.igpublish.plist` if your checkout differs from
`/Users/tatsumiyuuki/Desktop/dev/midjourney-explore`, then:

```sh
cp automation/deploy/com.tim-bankrupt.igpublish.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.tim-bankrupt.igpublish.plist
```

It runs immediately (`RunAtLoad`) and every 60s thereafter. Logs → `automation/deploy/igpub.log`
(gitignored).

### 3. Verify

```sh
tail -f automation/deploy/igpub.log        # watch a run
launchctl list | grep igpublish            # confirm it's loaded
bash automation/deploy/run_publish.sh      # run once by hand (will publish anything due NOW)
```

To stop / reload:

```sh
launchctl unload ~/Library/LaunchAgents/com.tim-bankrupt.igpublish.plist
```

---

## Caveats & the upgrade path

- **The Mac must be awake at fire time.** Asleep → the post fires on the next wake (a bit late,
  never dropped — `is_due` re-checks each run). For true always-on, move `run_publish.sh` to an
  Oracle Cloud Always-Free VM (also $0) running the same script under cron — the script is
  host-agnostic. That's the only change; no code rewrite.
- **One writer.** launchd on a single Mac = single writer to the git-YAML queue, so there are no
  concurrent-commit races today. When a hosted UI becomes a second writer, the queue moves behind a
  `QueueStore` seam onto a networked store (see `automation/ig-publish-pipeline.md` → store roadmap).
- **Idempotent.** `publish_one` claims `status: publishing` before the API call and records
  `media_id`, so a crash or double-fire never double-posts.
