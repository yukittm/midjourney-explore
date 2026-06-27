"""Feed Studio — pure logic (no I/O, no network): path-safety, candidate classification axes, and
board assembly. The server (`automation/studio.py`) does the FS/HTTP; this stays unit-testable.
"""
from __future__ import annotations

import os
import re
from urllib.parse import quote

from .contact import build_candidates
from .feed import build_tiles

# image roots the server is allowed to read, by short key
ALLOWED_ROOTS = {
    "candidates": "outputs/candidates",
    "selects": "outputs/selects",
    "assets": "automation/assets",
}
AXES = ("subject", "aspect", "flat")
_IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif")


def safe_path(repo_root: str, root_key: str, name: str) -> str | None:
    """Resolve (root_key, name) to an absolute path, or None if root is unknown or the path escapes
    its root (realpath-prefix containment — defends the local file route against traversal)."""
    rel = ALLOWED_ROOTS.get(root_key)
    if rel is None or not name:
        return None
    root = os.path.realpath(os.path.join(repo_root, rel))
    full = os.path.realpath(os.path.join(root, name))
    try:
        if os.path.commonpath([full, root]) != root:
            return None
    except ValueError:
        return None
    return full


def slugify(text: str) -> str:
    """A scaffold-safe kebab slug (matches scaffold.SLUG_RE) from arbitrary text; 'post' if empty."""
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "post"


def _img_url(root_key: str, name: str) -> str:
    return f"/img?root={root_key}&name={quote(name)}"


def _aspect_bucket(dims: "tuple[int, int] | None") -> str:
    if not dims or dims[1] == 0:
        return "unknown"
    r = dims[0] / dims[1]
    if r < 0.95:
        return "portrait"
    if r > 1.05:
        return "landscape"
    return "square"


def classify(filenames, axis: str, dims: dict | None = None) -> list[tuple[str, list[str]]]:
    """Group candidate filenames by the chosen axis. Returns [(label, [filename,...]), ...]."""
    names = sorted(f for f in filenames if f.lower().endswith(_IMG_EXT))
    if axis == "flat":
        return [("All images", names)] if names else []
    if axis == "aspect":
        dims = dims or {}
        order = ["portrait", "square", "landscape", "unknown"]
        buckets: dict[str, list[str]] = {}
        for f in names:
            buckets.setdefault(_aspect_bucket(dims.get(f)), []).append(f)
        return [(b, buckets[b]) for b in order if b in buckets]
    # default: subject (prompt prefix), biggest sets first
    groups: dict[str, list[str]] = {}
    for c in build_candidates(names):
        groups.setdefault(c.subject, []).append(c.filename)
    return sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))


def reconcile_order(saved_order, selects_names) -> list[str]:
    """The persisted selects order, dropping files that no longer exist and putting any NEW selects
    (not in the saved order) at the FRONT — a freshly staged image is the newest post (grid top-left)."""
    present = {n for n in selects_names if n.lower().endswith(_IMG_EXT)}
    ordered = [n for n in (saved_order or []) if n in present]
    seen = set(ordered)
    return sorted(n for n in present if n not in seen) + ordered


def assemble_board(candidate_names, selects_names, posts, axis: str = "subject",
                   dims: dict | None = None, selects_order=None) -> dict:
    """Build the JSON the frontend renders. The feed grid is ONE Instagram-style projection, newest
    top-left: the draggable `select` tiles (user order) on top, then any committed upcoming posts, then
    the locked `live` published tiles. The pool (raw candidates) is returned separately for its own tab."""
    if axis not in AXES:
        axis = "subject"
    sel_stems = {os.path.splitext(n)[0] for n in selects_names if n.lower().endswith(_IMG_EXT)}

    def _in_selects(name: str) -> bool:
        cs = slugify(os.path.splitext(name)[0])
        return any(s == cs or s.startswith(cs + "-") for s in sel_stems)

    pool = [{"label": label,
             "items": [{"name": n, "url": _img_url("candidates", n), "in_selects": _in_selects(n)}
                       for n in items]}
            for label, items in classify(candidate_names, axis, dims)]

    ordered_selects = reconcile_order(selects_order, selects_names)
    grid = [{"key": n, "kind": "select", "draggable": True, "url": _img_url("selects", n),
             "status": "select", "lane": "upcoming", "when": "", "caption": "",
             "slug": os.path.splitext(n)[0]}   # select filenames are already kebab slugs
            for n in ordered_selects]
    for t in build_tiles(posts, include_drafts=True):   # committed upcoming (incl. draft) + live, locked
        url = (_img_url("assets", t.image_rel[len("assets/"):])
               if t.image_rel and t.image_rel.startswith("assets/") else None)
        grid.append({"key": t.id, "kind": "post", "draggable": False, "url": url,
                     "status": t.status, "lane": t.lane, "when": t.when, "caption": t.caption_line})

    return {"axis": axis, "axes": list(AXES), "pool": pool, "grid": grid,
            "counts": {"pool": sum(len(g["items"]) for g in pool),
                       "selects": len(ordered_selects),
                       "live": sum(1 for t in grid if t["lane"] == "live")}}
