#!/usr/bin/env bash
# Auto-publish runner — invoked by launchd (or any cron). Polls the queue for DUE posts, publishes
# them via the Graph API, then PERSISTS the result back to git (commit + push) so GitHub Pages and
# the remote record stay in sync. $0, single-instance (flock). The human gate is `status: approved`
# in the committed queue — nothing else is published.
#
# Secrets (from automation/.env, gitignored, chmod 600):
#   IG_SYSTEM_USER_TOKEN  (required)  — Meta System User token (regenerate NON-EXPIRING before ≈2026-08-24)
#   GIT_PUSH_TOKEN        (optional)  — GitHub fine-grained PAT w/ contents:write, for headless push
set -uo pipefail
# launchd runs with a minimal PATH; make git (Homebrew or Apple) + python3 resolvable.
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:${PATH:-}"
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO" || exit 1

set -a; [ -f automation/.env ] && . automation/.env; set +a

# Single instance. macOS has no flock, so use an atomic mkdir lock. A hard crash (SIGKILL) can leave
# the lockdir behind; reclaim it if older than 30 min (a real run can't exceed the ~5-min poll timeout).
LOCKDIR="${TMPDIR:-/tmp}/igpub-publish.lock.d"
if [ -d "$LOCKDIR" ] && [ -z "$(find "$LOCKDIR" -maxdepth 0 -mmin -30 2>/dev/null)" ]; then
  echo "$(date -u +%FT%TZ) reclaiming stale lock $LOCKDIR"; rmdir "$LOCKDIR" 2>/dev/null || true
fi
if ! mkdir "$LOCKDIR" 2>/dev/null; then
  echo "$(date -u +%FT%TZ) another run in progress; skip"; exit 0
fi
trap 'rmdir "$LOCKDIR" 2>/dev/null' EXIT

echo "$(date -u +%FT%TZ) publish run"
python3 automation/publish.py || true   # publishes any due post; non-zero exit only on a failed post

# Persist any state change (queue->published move + media_id write-back) so Pages/remote stay synced.
if [ -n "$(git status --porcelain automation/queue automation/published automation/assets 2>/dev/null)" ]; then
  git add automation/queue automation/published automation/assets
  git -c user.name="igpub-bot" -c user.email="noreply@anthropic.com" \
      commit -q -m "auto-publish: $(date -u +%FT%TZ)"
  if [ -n "${GIT_PUSH_TOKEN:-}" ]; then
    git push -q "https://x-access-token:${GIT_PUSH_TOKEN}@github.com/yukittm/midjourney-explore.git" HEAD:master \
      && echo "pushed" || echo "push failed (retries next run)"
  else
    git push -q && echo "pushed" \
      || echo "push failed — set GIT_PUSH_TOKEN in automation/.env for reliable headless push"
  fi
fi
