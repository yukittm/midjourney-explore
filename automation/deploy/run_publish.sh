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
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO" || exit 1

set -a; [ -f automation/.env ] && . automation/.env; set +a

exec 9>"${TMPDIR:-/tmp}/igpub-publish.lock"
flock -n 9 || { echo "$(date -u +%FT%TZ) another run in progress; skip"; exit 0; }

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
