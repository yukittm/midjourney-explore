"""Pure logic for the image-classifier tag store (no I/O, no network — unit-testable). The CLI
(automation/classify.py) and the Studio do pixel-hashing + JSON/file I/O; this module only
transforms dicts.

Model: the store is {"schema_version":1, "images": {<content-hash>: record}}. A record carries
  filenames:[...]  subject  scene  color:{dominant,accent,vector}  source("vision"|"human")  tagged_at
Tags are STICKY and identity is the CONTENT HASH (filenames change on re-download/variation):
- subject/scene come from an in-session VISION pass, written once, never re-tagged, and a
  source=="human" record is never clobbered.
- color is a recomputable cache (overwrite-on-recompute is fine; it's deterministic).
"""
from __future__ import annotations


def empty_store() -> dict:
    return {"schema_version": 1, "images": {}}


def index_by_filename(store: dict) -> dict:
    """{filename: record} for the Studio's filename-keyed grouping/lookup."""
    out: dict = {}
    for rec in (store.get("images") or {}).values():
        for fn in rec.get("filenames", []):
            out[fn] = rec
    return out


def reattach_filenames(store: dict, disk_hashes: dict) -> dict:
    """Sync each known hash's filenames to what's on disk (auto-heals renames / re-downloads).
    disk_hashes: {hash: [filenames]}."""
    imgs = store.get("images") or {}
    for h, fns in disk_hashes.items():
        if h in imgs:
            imgs[h]["filenames"] = sorted(fns)
    return store


def plan_subject_scene_work(disk_hashes: dict, store: dict) -> list:
    """Hashes present on disk but lacking a subject (color is computed separately, so it doesn't
    gate this). Returns [{"hash":h, "filenames":[...]}] — the in-session vision work-list."""
    imgs = store.get("images") or {}
    todo = []
    for h, fns in sorted(disk_hashes.items()):
        rec = imgs.get(h)
        if not rec or not rec.get("subject"):
            todo.append({"hash": h, "filenames": sorted(fns)})
    return todo


def merge_subject_scene(store: dict, results: dict, *, now: str = "") -> tuple:
    """Apply {hash: {subject, scene}} non-destructively. Skip source=="human" (locked) and any hash
    that already has a subject (sticky/idempotent). Returns (store, n_written)."""
    imgs = store.setdefault("images", {})
    n = 0
    for h, r in results.items():
        rec = imgs.setdefault(h, {})
        if rec.get("source") == "human" or rec.get("subject"):
            continue
        rec["subject"] = r.get("subject")
        rec["scene"] = r.get("scene")
        rec["source"] = "vision"
        if now:
            rec["tagged_at"] = now
        n += 1
    return store, n


def set_color(store: dict, h: str, filenames, color: dict) -> dict:
    """Write/overwrite the computed color cache for a hash (recomputable; never touches subject/scene
    or the source lock)."""
    rec = store.setdefault("images", {}).setdefault(h, {})
    rec["color"] = color
    if filenames:
        rec["filenames"] = sorted(set(rec.get("filenames", [])) | set(filenames))
    return store


def stale_hashes(store: dict, present_hashes) -> list:
    """Hashes in the store whose images are no longer on disk (report, don't auto-delete)."""
    present = set(present_hashes)
    return sorted(h for h in (store.get("images") or {}) if h not in present)
