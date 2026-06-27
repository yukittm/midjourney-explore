#!/usr/bin/env python3
"""Generate an Instagram-style feed-grid preview from the queue + published records, so you can see
how the posts will sit together on the profile BEFORE posting (color flow, anti-sameness, rhythm).

Writes  automation/feed-preview.html  (a self-contained 3-column grid; newest top-left) and, with
--open, opens it in the browser. Read-only — never touches the queue. Run from the repo root.

  python automation/feed_preview.py --open
"""
from __future__ import annotations

import argparse
import os
import sys
import webbrowser
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # make `import igpub` work

from igpub.feed import build_tiles, render_html  # noqa: E402
from igpub.queue import PUBLISHED_DIR, QUEUE_DIR, list_posts  # noqa: E402

OUT = "automation/feed-preview.html"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate the IG feed-grid preview (queue + published).")
    ap.add_argument("--out", default=OUT, help=f"output HTML path (default: {OUT})")
    ap.add_argument("--open", action="store_true", help="open the generated HTML in the browser")
    args = ap.parse_args()

    repo_root = os.getcwd()
    posts = list_posts(repo_root, QUEUE_DIR) + list_posts(repo_root, PUBLISHED_DIR)
    tiles = build_tiles(posts)

    missing = [t.id for t in tiles if t.image_rel and
               not os.path.isfile(os.path.join(repo_root, "automation", t.image_rel))]
    generated_at = "generated " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    html_str = render_html(tiles, generated_at=generated_at)

    out_path = os.path.join(repo_root, args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_str)

    print(f"wrote {args.out}  ({len(tiles)} tiles)")
    if missing:
        print(f"  ⚠ {len(missing)} tile(s) reference a missing image (will show broken): {', '.join(missing)}")
    if args.open:
        webbrowser.open(f"file://{out_path}")
    else:
        print(f"  open it: open {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
