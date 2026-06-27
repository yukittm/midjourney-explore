"""Scaffold a draft posting-queue entry from a picked image.

Turns a chosen image (typically from `outputs/selects/`) into
`automation/assets/<id>/01.jpg` + a draft `automation/queue/<id>.yml`, then leaves
caption/alt_text empty for the human (the `caption` skill). It exists to make the
id ↔ asset-dir ↔ key triple agree by construction and to write the record through the
model (so the file shape can't drift from `models.Post`).

Safety: every precondition is checked BEFORE any file is written; a mid-write failure
removes the partial asset dir so a retry isn't blocked. Non-JPEG sources are refused
(detected by content, never the filename) — IG accepts JPEG only and we never write
non-JPEG bytes under a `.jpg` name.

Pure-ish logic lives here behind a small surface; `automation/new_post.py` is the CLI.
"""
from __future__ import annotations

import os
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime

from .imaging import aspect_ok, read_jpeg_size
from .models import MediaType, Post, Status, image_asset

ASSETS_DIR = "automation/assets"
QUEUE_DIR = "automation/queue"
SELECTS_DIR = "outputs/selects"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ScaffoldError(Exception):
    """A precondition failed; nothing was written."""


@dataclass
class ScaffoldResult:
    id: str
    queue_path: str
    asset_key: str
    image_status: str               # "ok" | "out_of_range"
    width: int
    height: int
    validation_errors: list = field(default_factory=list)  # validate_post on the new draft
    source_in_selects: bool = False
    select_removed: bool = False


def validate_slug(slug: str) -> None:
    if not slug or not SLUG_RE.match(slug):
        raise ScaffoldError(
            f"invalid slug {slug!r} — use lowercase kebab-case [a-z0-9-], e.g. 'flowing-color-surfer'")


def validate_date(date_str: str) -> None:
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ScaffoldError(f"invalid date {date_str!r} — use YYYY-MM-DD (zero-padded)")
    if dt.strftime("%Y-%m-%d") != date_str:   # strptime is lenient ('2026-7-2'); require zero-padding
        raise ScaffoldError(
            f"date {date_str!r} must be zero-padded YYYY-MM-DD (did you mean {dt.strftime('%Y-%m-%d')}?)")


def make_id(date_str: str, slug: str) -> str:
    return f"{date_str}_{slug}"


def _classify_image(path: str) -> "tuple[str, int, int]":
    """Return ('ok'|'out_of_range', w, h). Raise ScaffoldError for a non-JPEG (detected by CONTENT)."""
    try:
        w, h = read_jpeg_size(path)
    except ValueError as e:
        raise ScaffoldError(
            f"source is not a JPEG ({e}) — IG accepts JPEG only; convert/crop to a 4:5..1.91:1 JPEG "
            f"first: {path}")
    return ("ok" if aspect_ok(w, h) else "out_of_range", w, h)


def _is_under(path: str, directory: str) -> bool:
    try:
        root = os.path.realpath(directory)
        return os.path.commonpath([os.path.realpath(path), root]) == root
    except ValueError:   # e.g. different drives on Windows
        return False


def scaffold_post(*, image: str, slug: str, date_str: str, repo_root: str = ".",
                  media_type: str = "image", remove_select: bool = False) -> ScaffoldResult:
    """Create a draft queue entry from `image`. Raises ScaffoldError (nothing written) on any
    precondition failure; re-raises other exceptions only after cleaning up a partial asset dir."""
    # 1) Preconditions — NOTHING is written until all pass.
    try:
        import yaml  # noqa: F401 — fail early; save_post imports it lazily and would crash mid-write
    except ImportError:
        raise ScaffoldError("PyYAML required — pip install -r automation/requirements.txt")
    if media_type != "image":
        raise ScaffoldError(
            f"only --media-type image is supported here, got {media_type!r} — carousel/reels/story: "
            "hand-author from automation/queue/_EXAMPLE.yml for now")
    validate_slug(slug)
    validate_date(date_str)
    if not os.path.isfile(image):
        raise ScaffoldError(f"image not found: {image}")
    image_status, w, h = _classify_image(image)   # raises on non-JPEG

    post_id = make_id(date_str, slug)
    assets_dir = os.path.join(repo_root, ASSETS_DIR, post_id)
    queue_path = os.path.join(repo_root, QUEUE_DIR, post_id + ".yml")
    if os.path.exists(queue_path):
        raise ScaffoldError(f"queue entry already exists: {queue_path}")
    if os.path.exists(assets_dir):
        raise ScaffoldError(
            f"asset dir already exists (collision or partial leftover from a failed run): {assets_dir} "
            "— remove it and retry")

    asset_key = f"{ASSETS_DIR}/{post_id}/01.jpg"

    # 2) Writes — create the asset dir + image + yml; clean up the dir on any failure.
    created_dir = False
    try:
        os.makedirs(assets_dir, exist_ok=False)
        created_dir = True
        shutil.copy2(image, os.path.join(assets_dir, "01.jpg"))
        post = Post(id=post_id, status=Status.DRAFT, media_type=MediaType.IMAGE,
                    assets=[image_asset(asset_key)], caption="", hashtags=[])
        post.source_path = queue_path   # save_post raises without this
        os.makedirs(os.path.dirname(queue_path), exist_ok=True)
        from .queue import save_post     # local import keeps yaml lazy + avoids any import cycle
        save_post(post)
    except Exception:
        if created_dir:
            shutil.rmtree(assets_dir, ignore_errors=True)
        if os.path.exists(queue_path):
            os.remove(queue_path)
        raise

    # 3) Validate the new draft (an image still needing a crop reports errors here — expected).
    from .validate import validate_post
    validation_errors = validate_post(post, repo_root=repo_root)

    # 4) Optional selects reconciliation (keep "selects = picked-but-not-queued" true).
    source_in_selects = _is_under(image, os.path.join(repo_root, SELECTS_DIR))
    select_removed = False
    if remove_select and source_in_selects:
        os.remove(image)
        select_removed = True

    return ScaffoldResult(
        id=post_id, queue_path=queue_path, asset_key=asset_key, image_status=image_status,
        width=w, height=h, validation_errors=validation_errors,
        source_in_selects=source_in_selects, select_removed=select_removed)
