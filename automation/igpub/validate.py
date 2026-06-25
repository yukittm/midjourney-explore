"""Validation — run at commit time (pre-commit / CI) so bad posts are rejected at approval, not at
3am. `validate_meta` is pure (no FS); `validate_assets` touches the FS via an injectable size reader.

Type-dispatched by `media_type`: each IG post type has its own asset-count/kind rule, and a carousel
additionally requires all image children to share ONE aspect ratio (IG otherwise crops every child to
the first child's AR — a silent wrong-output, so we HARD REJECT a mismatch)."""
from __future__ import annotations

import os
from typing import Callable

from .imaging import aspect_ok, read_jpeg_size
from .models import MediaType, Post, VALID_MODES, assemble_caption

CAPTION_MAX = 2200
HASHTAG_MAX = 30
CAROUSEL_MIN = 2
CAROUSEL_MAX = 10
_AR_TOL = 0.02  # carousel children must share one aspect ratio within this tolerance

SizeReader = Callable[[str], "tuple[int, int]"]


def _kinds(post: Post) -> str:
    return ",".join(a.kind for a in post.assets) or "(none)"


def _local_path(asset, repo_root: str) -> str:
    """Resolve an asset key to its on-disk path, per host convention (image key IS the repo path;
    video key lives under automation/video/)."""
    if asset.kind == "image":
        return os.path.join(repo_root, asset.key)
    return os.path.join(repo_root, "automation", "video", asset.key)


def validate_meta(post: Post) -> list[str]:
    """Pure checks that need no media bytes."""
    errors: list[str] = []
    if not post.id:
        errors.append("id is required")
    if post.status.value == "scheduled" and not post.publish_at:
        errors.append("publish_at is required for a scheduled post")
    if post.schedule_mode not in VALID_MODES:
        errors.append(f"schedule_mode must be one of {list(VALID_MODES)}, got {post.schedule_mode!r}")

    n = len(post.assets)
    mt = post.media_type
    if n == 0:
        errors.append("at least one asset is required")
    elif mt == MediaType.IMAGE:
        if n != 1 or post.assets[0].kind != "image":
            errors.append(f"image post needs exactly 1 image asset, got {n} [{_kinds(post)}]")
    elif mt == MediaType.CAROUSEL:
        if not (CAROUSEL_MIN <= n <= CAROUSEL_MAX):
            errors.append(f"carousel needs {CAROUSEL_MIN}..{CAROUSEL_MAX} assets, got {n}")
    elif mt == MediaType.REELS:
        if n != 1 or post.assets[0].kind != "video":
            errors.append(f"reels needs exactly 1 video asset, got {n} [{_kinds(post)}]")
    elif mt == MediaType.STORY:
        if n != 1:
            errors.append(f"story needs exactly 1 asset, got {n}")

    if mt == MediaType.STORY and (post.caption or post.hashtags):
        errors.append("story posts cannot carry caption/hashtags via the API (remove them)")

    # caption length: check the SAME assembled string the publisher will send.
    if mt != MediaType.STORY:
        full = len(assemble_caption(post))
        if full > CAPTION_MAX:
            errors.append(f"caption+hashtags {full} chars > {CAPTION_MAX}")
    if len(post.hashtags) > HASHTAG_MAX:
        errors.append(f"{len(post.hashtags)} hashtags > {HASHTAG_MAX}")
    for h in post.hashtags:
        if h.startswith("#"):
            errors.append(f"hashtag '{h}' must not include the leading '#'")

    for i, a in enumerate(post.assets):
        if a.kind not in ("image", "video"):
            errors.append(f"asset[{i}] kind must be image|video, got {a.kind!r}")
        if not a.key:
            errors.append(f"asset[{i}] key is required")
        if a.kind == "video" and (a.alt_text or a.user_tags):
            errors.append(f"asset[{i}] alt_text/user_tags are image-only")
    return errors


def validate_assets(post: Post, repo_root: str = ".", size_reader: SizeReader = read_jpeg_size) -> list[str]:
    """FS checks: each image exists, is a JPEG, fits the IG aspect range; carousel children share one AR.
    (Video deep-validation — codec/duration — is deferred to the FULL build.)"""
    errors: list[str] = []
    ratios: list[tuple[str, float]] = []
    for a in post.assets:
        if a.kind != "image":
            continue
        path = _local_path(a, repo_root)
        if not os.path.isfile(path):
            errors.append(f"image not found: {a.key}")
            continue
        if not a.key.lower().endswith((".jpg", ".jpeg")):
            errors.append(f"image must be .jpg/.jpeg (IG accepts JPEG only): {a.key}")
            continue
        try:
            w, h = size_reader(path)
        except Exception as e:  # noqa: BLE001 — surface any read failure as a validation error
            errors.append(f"could not read image size for {a.key}: {e}")
            continue
        if not aspect_ok(w, h):
            errors.append(f"aspect ratio out of 4:5..1.91:1 for {a.key} ({w}x{h})")
        else:
            ratios.append((a.key, w / h))

    if post.media_type == MediaType.CAROUSEL and len(ratios) >= 2:
        base_key, base = ratios[0]
        for key, r in ratios[1:]:
            if abs(r - base) > _AR_TOL:
                errors.append(
                    f"carousel children must share one aspect ratio — {key} ({r:.3f}) differs from "
                    f"{base_key} ({base:.3f}); pre-crop to match (IG would crop all to the first child)")
    return errors


def validate_post(post: Post, repo_root: str = ".", size_reader: SizeReader = read_jpeg_size) -> list[str]:
    return validate_meta(post) + validate_assets(post, repo_root, size_reader)


def duplicate_ids(posts) -> list[str]:
    """Ids appearing more than once across the given posts (call with queue ∪ published) — an id
    collision would clobber a published archive record on move, so the validator rejects it."""
    counts: dict = {}
    for p in posts:
        counts[p.id] = counts.get(p.id, 0) + 1
    return sorted(pid for pid, n in counts.items() if n > 1)
