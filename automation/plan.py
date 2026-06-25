#!/usr/bin/env python3
"""Derive the posting calendar: assign publish_at slots to APPROVED auto-mode posts from
schedule.yml, then (with --apply) write them back. The queue stays the SSoT; this is a pure
function of (approved posts + schedule.yml). PINNED posts keep their time; HOLD posts are skipped.
Idempotent — re-running does not move already-scheduled posts."""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # make `import igpub` work

from igpub.queue import list_posts, save_post  # noqa: E402
from igpub.schedule import assign_slots, load_schedule  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Plan the IG posting calendar from schedule.yml.")
    ap.add_argument("--apply", action="store_true",
                    help="write the assigned publish_at + status=scheduled back to the queue files")
    ap.add_argument("--now", help="ISO time to treat as 'now' (default: real now, UTC)")
    args = ap.parse_args()

    repo_root = os.getcwd()
    posts = list_posts(repo_root)
    schedule = load_schedule(repo_root)
    now = datetime.fromisoformat(args.now) if args.now else datetime.now(timezone.utc)
    if now.tzinfo is None:        # a naive --now would shift the whole horizon by the host offset → treat as UTC
        now = now.replace(tzinfo=timezone.utc)

    before = {p.id: (p.status, p.publish_at) for p in posts}
    plan = assign_slots(posts, schedule, now)
    print(plan.render() if plan.assignments or plan.unscheduled else "no approved posts to schedule")

    if args.apply:
        changed = 0
        for p in posts:
            if (p.status, p.publish_at) != before.get(p.id):
                save_post(p)
                changed += 1
        print(f"\napplied: wrote {changed} queue file(s)")
    else:
        print("\n(dry-run — pass --apply to write publish_at back to the queue)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
