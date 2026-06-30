#!/usr/bin/env python3
"""Classify the candidate image pool (outputs/candidates/) by reading the IMAGES.

Two signals, two mechanisms:
  • COLOR  — computed from pixels (igpub/color.py): deterministic, free, idempotent. `classify.py color`.
  • SUBJECT + SCENE — semantic, so an in-session VISION pass (Claude/an agent reads the image files).
    NO API call here (cost/consent rule): `classify.py emit` writes a work-list of untagged images;
    Claude tags them and writes results; `classify.py ingest` merges them in non-destructively.

Tags are sticky and keyed by CONTENT HASH (filenames change on MJ re-download/variation). Store =
outputs/candidates/.classes.json (gitignored, like .order.json). Run from the repo root.

  python automation/classify.py color           # compute/refresh color for images missing it
  python automation/classify.py emit            # write .classify-todo.json (untagged subject/scene)
  python automation/classify.py ingest          # merge .classify-results.json into the store
  python automation/classify.py status
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # make `import igpub` work

from igpub import classify_logic as L  # noqa: E402
from igpub import color as C  # noqa: E402

CAND = "outputs/candidates"
STORE = os.path.join(CAND, ".classes.json")
TODO = os.path.join(CAND, ".classify-todo.json")
RESULTS = os.path.join(CAND, ".classify-results.json")
_EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif")


def _imgs(d):
    return sorted(f for f in os.listdir(d) if f.lower().endswith(_EXT)) if os.path.isdir(d) else []


def _pixel_hash(path: str) -> str:
    from PIL import Image
    with Image.open(path) as im:
        im = im.convert("RGB")
        return hashlib.sha256(repr(im.size).encode() + im.tobytes()).hexdigest()


def _disk_hashes(repo_root: str) -> dict:
    """{hash: [filenames]} for every candidate image (pixel-identical files share a hash)."""
    base = os.path.join(repo_root, CAND)
    out: dict = {}
    for f in _imgs(base):
        out.setdefault(_pixel_hash(os.path.join(base, f)), []).append(f)
    return out


def _load(repo_root: str) -> dict:
    p = os.path.join(repo_root, STORE)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    return L.empty_store()


def _save(repo_root: str, store: dict) -> None:
    p = os.path.join(repo_root, STORE)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(store, fh, indent=1, ensure_ascii=False)
    os.replace(tmp, p)


def cmd_color(repo_root: str, args) -> int:
    store = _load(repo_root)
    dh = _disk_hashes(repo_root)
    store = L.reattach_filenames(store, dh)
    imgs = store.get("images") or {}
    base = os.path.join(repo_root, CAND)
    done = 0
    for h, fns in dh.items():
        if not args.all and imgs.get(h, {}).get("color"):
            continue
        col = C.palette_of(os.path.join(base, fns[0]))
        L.set_color(store, h, fns, col)
        done += 1
    _save(repo_root, store)
    print(f"color computed for {done} image(s); {len(dh)} total in pool")
    return 0


def cmd_emit(repo_root: str, args) -> int:
    store = _load(repo_root)
    dh = _disk_hashes(repo_root)
    todo = L.plan_subject_scene_work(dh, store)
    base = os.path.join(repo_root, CAND)
    for t in todo:
        t["path"] = os.path.join(CAND, t["filenames"][0])  # repo-relative path for the vision reader
    with open(os.path.join(repo_root, TODO), "w", encoding="utf-8") as fh:
        json.dump({"todo": todo}, fh, indent=1, ensure_ascii=False)
    print(f"{len(todo)} image(s) need subject/scene → {TODO}")
    print("Next: an in-session vision pass reads each path, writes "
          f"{RESULTS} as {{\"results\":{{<hash>:{{subject,scene}}}}}}, then: classify.py ingest")
    return 0


def cmd_ingest(repo_root: str, args) -> int:
    p = os.path.join(repo_root, RESULTS)
    if not os.path.exists(p):
        print(f"no {RESULTS} to ingest"); return 2
    with open(p, encoding="utf-8") as fh:
        results = (json.load(fh) or {}).get("results") or {}
    store = _load(repo_root)
    store = L.reattach_filenames(store, _disk_hashes(repo_root))
    store, n = L.merge_subject_scene(store, results, now=datetime.now(timezone.utc).isoformat())
    _save(repo_root, store)
    print(f"ingested {n} subject/scene tag(s)")
    return 0


def cmd_status(repo_root: str, args) -> int:
    store = _load(repo_root)
    dh = _disk_hashes(repo_root)
    imgs = store.get("images") or {}
    with_subj = sum(1 for h in dh if imgs.get(h, {}).get("subject"))
    with_col = sum(1 for h in dh if imgs.get(h, {}).get("color"))
    stale = L.stale_hashes(store, dh.keys())
    print(f"pool: {len(dh)} unique images")
    print(f"  subject/scene tagged: {with_subj}   untagged: {len(dh) - with_subj}")
    print(f"  color computed:       {with_col}")
    if stale:
        print(f"  stale records (no file on disk): {len(stale)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Classify the candidate image pool by content.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pc = sub.add_parser("color"); pc.add_argument("--all", action="store_true", help="recompute even if cached")
    sub.add_parser("emit"); sub.add_parser("ingest"); sub.add_parser("status")
    args = ap.parse_args()
    repo_root = os.getcwd()
    return {"color": cmd_color, "emit": cmd_emit, "ingest": cmd_ingest, "status": cmd_status}[args.cmd](repo_root, args)


if __name__ == "__main__":
    raise SystemExit(main())
