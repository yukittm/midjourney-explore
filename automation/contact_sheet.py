#!/usr/bin/env python3
"""Generate a visual contact-sheet of the raw candidate pool (outputs/candidates/) so you can triage
variations at a glance and decide which to crop into outputs/selects/.

Writes  outputs/candidates/contact-sheet.html  (grouped by subject) and, with --open, opens it.
Read-only — never moves or crops files. Run from the repo root.

  python automation/contact_sheet.py --open
"""
from __future__ import annotations

import argparse
import os
import sys
import webbrowser
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # make `import igpub` work

from igpub.contact import build_candidates, group, render_html  # noqa: E402

CANDIDATES_DIR = "outputs/candidates"
OUT = "outputs/candidates/contact-sheet.html"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate the candidate-pool contact-sheet for triage.")
    ap.add_argument("--dir", default=CANDIDATES_DIR, help=f"candidates folder (default: {CANDIDATES_DIR})")
    ap.add_argument("--out", default=OUT, help=f"output HTML path (default: {OUT})")
    ap.add_argument("--open", action="store_true", help="open the generated HTML in the browser")
    args = ap.parse_args()

    repo_root = os.getcwd()
    src_dir = os.path.join(repo_root, args.dir)
    if not os.path.isdir(src_dir):
        print(f"error: not a directory: {args.dir}", file=sys.stderr)
        return 2

    names = [f for f in os.listdir(src_dir) if not f.startswith(".")]
    cands = build_candidates(names)
    groups = group(cands)

    # HTML sits inside the candidates dir → reference images by bare filename.
    out_path = os.path.join(repo_root, args.out)
    img_prefix = "" if os.path.dirname(out_path) == src_dir else \
        (os.path.relpath(src_dir, os.path.dirname(out_path)) + "/")
    generated_at = "generated " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    html_str = render_html(groups, total=len(cands), generated_at=generated_at, img_prefix=img_prefix)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_str)

    print(f"wrote {args.out}  ({len(cands)} images, {len(groups)} subjects)")
    if args.open:
        webbrowser.open(f"file://{out_path}")
    else:
        print(f"  open it: open {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
