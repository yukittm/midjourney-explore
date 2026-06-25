"""Validation — run at commit time (pre-commit / CI) so bad posts are rejected at approval,
not at 3am. `validate_meta` is pure (no FS); `validate_images` touches the FS via an injectable
size reader (for testability)."""
from __future__ import annotations

import os
from typing import Callable

from .imaging import aspect_ok, read_jpeg_size
from .models import MediaType, Post

CAPTION_MAX = 2200
HASHTAG_MAX = 30
CAROUSEL_MAX = 10

SizeReader = Callable[[str], "tuple[int, int]"]


def validate_meta(post: Post) -> list[str]:
    """Pure checks that need no image bytes."""
    errors: list[str] = []
    if not post.id:
        errors.append("id is required")
    if not post.publish_at:
        errors.append("publish_at is required")

    if not post.images:
        errors.append("at least one image is required")
    elif post.media_type == MediaType.IMAGE and len(post.images) != 1:
        errors.append(f"image post needs exactly 1 image, got {len(post.images)}")
    elif post.media_type == MediaType.CAROUSEL and not (2 <= len(post.images) <= CAROUSEL_MAX):
        errors.append(f"carousel needs 2..{CAROUSEL_MAX} images, got {len(post.images)}")

    full_len = len(post.caption) + sum(len(h) + 2 for h in post.hashtags)  # '#' + space per tag
    if full_len > CAPTION_MAX:
        errors.append(f"caption+hashtags {full_len} chars > {CAPTION_MAX}")
    if len(post.hashtags) > HASHTAG_MAX:
        errors.append(f"{len(post.hashtags)} hashtags > {HASHTAG_MAX}")
    for h in post.hashtags:
        if h.startswith("#"):
            errors.append(f"hashtag '{h}' must not include the leading '#'")
    return errors


def validate_images(post: Post, repo_root: str = ".", size_reader: SizeReader = read_jpeg_size) -> list[str]:
    """FS checks: each image exists, is a JPEG, and fits the IG aspect range."""
    errors: list[str] = []
    for rel in post.images:
        path = os.path.join(repo_root, rel)
        if not os.path.isfile(path):
            errors.append(f"image not found: {rel}")
            continue
        if not rel.lower().endswith((".jpg", ".jpeg")):
            errors.append(f"image must be .jpg/.jpeg (IG accepts JPEG only): {rel}")
            continue
        try:
            w, h = size_reader(path)
        except Exception as e:  # noqa: BLE001 — surface any read failure as a validation error
            errors.append(f"could not read image size for {rel}: {e}")
            continue
        if not aspect_ok(w, h):
            errors.append(f"aspect ratio out of 4:5..1.91:1 for {rel} ({w}x{h})")
    return errors


def validate_post(post: Post, repo_root: str = ".", size_reader: SizeReader = read_jpeg_size) -> list[str]:
    return validate_meta(post) + validate_images(post, repo_root, size_reader)
