"""Queue I/O — load/list/save per-post YAML files and move published items.

The git queue is the single source of truth; this is the only module that touches the FS for the
queue, behind a small surface a UI could reuse unchanged.
"""
from __future__ import annotations

import glob
import os

from .models import Post

QUEUE_DIR = "automation/queue"
PUBLISHED_DIR = "automation/published"


def load_post(path: str) -> Post:
    import yaml  # lazy — move_to_published + the runners can import this module without PyYAML
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return Post.from_dict(data, source_path=path)


def list_posts(repo_root: str = ".", queue_dir: str = QUEUE_DIR) -> list[Post]:
    base = os.path.join(repo_root, queue_dir)
    paths = sorted(glob.glob(os.path.join(base, "*.yml")) + glob.glob(os.path.join(base, "*.yaml")))
    posts: list[Post] = []
    for p in paths:
        if os.path.basename(p).startswith("_"):   # _EXAMPLE.yml etc. are ignored by the runner
            continue
        posts.append(load_post(p))
    return posts


def save_post(post: Post) -> None:
    if not post.source_path:
        raise ValueError("post has no source_path to save to")
    import yaml  # lazy (see load_post)
    with open(post.source_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(post.to_dict(), f, sort_keys=False, allow_unicode=True)


def move_to_published(post: Post, repo_root: str = ".") -> str:
    """Move the queue file into PUBLISHED_DIR; returns the new path."""
    if not post.source_path:
        raise ValueError("post has no source_path")
    dest_dir = os.path.join(repo_root, PUBLISHED_DIR)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, os.path.basename(post.source_path))
    if os.path.exists(dest):  # an id collision would silently clobber a published archive record
        raise FileExistsError(f"refusing to overwrite an existing published record: {dest}")
    os.replace(post.source_path, dest)
    post.source_path = dest
    return dest
