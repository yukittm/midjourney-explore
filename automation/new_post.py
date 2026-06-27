#!/usr/bin/env python3
"""Scaffold a draft posting-queue entry from a picked image (e.g. one in outputs/selects/).

Creates  automation/assets/<date>_<slug>/01.jpg  +  a draft  automation/queue/<date>_<slug>.yml ,
then validates. Caption / alt_text stay EMPTY — fill them with the `caption` skill, set
`status: approved`, then run  plan.py . Run from the repo root.

  python automation/new_post.py --image outputs/selects/foo.jpg --slug flowing-color-surfer
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # make `import igpub` work

from igpub.scaffold import ScaffoldError, scaffold_post  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Scaffold a draft IG post from a picked image.")
    ap.add_argument("--image", required=True, help="path to the chosen JPEG (e.g. outputs/selects/foo.jpg)")
    ap.add_argument("--slug", required=True, help="lowercase kebab-case slug, e.g. flowing-color-surfer")
    ap.add_argument("--date", help="YYYY-MM-DD id prefix (default: today, UTC)")
    ap.add_argument("--media-type", default="image", help="only 'image' is supported here")
    ap.add_argument("--remove-select", action="store_true",
                    help="delete the source from outputs/selects/ after enqueue (keeps the staging invariant)")
    args = ap.parse_args()

    date_str = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    try:
        r = scaffold_post(image=args.image, slug=args.slug, date_str=date_str,
                          repo_root=os.getcwd(), media_type=args.media_type,
                          remove_select=args.remove_select)
    except ScaffoldError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    print(f"created draft  {r.queue_path}")
    print(f"        asset  {r.asset_key}  ({r.width}x{r.height})")
    if r.image_status == "out_of_range":
        print(f"  ⚠ aspect {r.width}x{r.height} is outside 4:5..1.91:1 — crop to a valid JPEG before approving.")
    if r.validation_errors:
        print("  validation (expected for a draft that still needs caption/crop):")
        for err in r.validation_errors:
            print(f"    - {err}")
    else:
        print("  validation: clean")

    if r.select_removed:
        print("  removed the source from outputs/selects/")
    elif r.source_in_selects:
        print("  ⚠ remember to remove the source from outputs/selects/ (it's now queued) — "
              "or re-run with --remove-select")

    print("\nnext: write caption + alt via the `caption` skill into the queue draft, set "
          "status: approved, then  python automation/plan.py --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
