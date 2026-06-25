#!/usr/bin/env python3
"""Validate every post in the queue. Exits non-zero if any fails — so a pre-commit hook / CI blocks
a bad post at approval time, not at publish time."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # make `import igpub` work

from igpub.queue import list_posts  # noqa: E402
from igpub.validate import validate_post  # noqa: E402


def main() -> int:
    repo_root = os.getcwd()
    posts = list_posts(repo_root)
    if not posts:
        print("queue empty — nothing to validate")
        return 0
    failed = 0
    for post in posts:
        errors = validate_post(post, repo_root=repo_root)
        rel = os.path.relpath(post.source_path, repo_root) if post.source_path else post.id
        if errors:
            failed += 1
            print(f"✗ {post.id} ({rel})")
            for e in errors:
                print(f"    - {e}")
        else:
            print(f"✓ {post.id}")
    print(f"\n{len(posts) - failed}/{len(posts)} valid")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
