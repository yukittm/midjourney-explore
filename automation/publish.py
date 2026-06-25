#!/usr/bin/env python3
"""Publish due+approved posts (or one --id) to Instagram via the Graph API.

Phase 0: run by hand (`python automation/publish.py --id <id>`). Phase 1: a scheduler runs it.
The human-approval gate is `status: approved` in the committed queue — nothing else is published.
The token comes from the IG_SYSTEM_USER_TOKEN env var (never the repo).
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # make `import igpub` work

from igpub.config import get_token, load_config  # noqa: E402
from igpub.graph import GraphClient  # noqa: E402
from igpub.hosting import build_host  # noqa: E402
from igpub.publish import DAILY_LIMIT, is_due, publish_one  # noqa: E402
from igpub.queue import list_posts, move_to_published, save_post  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Publish approved IG posts from the queue.")
    ap.add_argument("--id", help="publish only this post id (ignores publish_at)")
    ap.add_argument("--now", help="ISO time to treat as 'now' (default: real now, UTC)")
    args = ap.parse_args()

    repo_root = os.getcwd()
    config = load_config(repo_root)
    ig_user_id = config.get("ig_user_id")
    if not ig_user_id:
        print("config error: ig_user_id missing — copy automation/config.example.yml -> config.yml")
        return 2

    graph = GraphClient(ig_user_id, get_token(), config.get("graph_version", "v21.0"))
    host = build_host(config)
    poll = config.get("poll", {}) or {}
    now = datetime.fromisoformat(args.now) if args.now else datetime.now(timezone.utc)

    posts = list_posts(repo_root)
    targets = [p for p in posts if p.id == args.id] if args.id else [p for p in posts if is_due(p, now)]
    if not targets:
        print("nothing to publish")
        return 0

    try:  # pre-flight the 24h limit; defer rather than fail if exhausted (matters on a backlog flush)
        used = graph.publishing_limit()
        if used >= DAILY_LIMIT:
            print(f"content publishing limit reached ({used}/{DAILY_LIMIT} in 24h) — deferring")
            return 0
    except Exception:  # noqa: BLE001 — don't block publishing on the limit check
        pass

    published = failed = 0
    for post in targets:
        try:
            publish_one(post, graph, host, save_post, lambda p: move_to_published(p, repo_root),
                        poll_timeout=poll.get("timeout_seconds", 300),
                        poll_interval=poll.get("interval_seconds", 5))
            published += 1
            print(f"✓ published {post.id} -> {post.result.media_id}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"✗ failed {post.id}: {e}")

    hc = config.get("healthcheck_url")
    if hc:  # dead-man's-switch ping (best-effort)
        try:
            import requests
            requests.get(hc, timeout=10)
        except Exception:  # noqa: BLE001
            pass

    print(f"\npublished {published}, failed {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
