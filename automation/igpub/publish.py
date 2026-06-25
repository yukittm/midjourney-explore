"""Publish orchestration — the flow runs over INJECTED dependencies (graph client, image host,
save/move callbacks), so it is unit-testable with fakes (no network, no YAML).

Order matters for safety:
  1. skip if a media_id already exists (idempotent — never double-post);
  2. claim the row (status=PUBLISHING + save) BEFORE any API call;
  3. create container(s) → poll to FINISHED (bounded; ERROR/EXPIRED/timeout = failure) → publish;
  4. write the returned media_id immediately (the idempotency key), then status=PUBLISHED + move;
  5. on any failure → status=FAILED + error + save (loud, not silent).
"""
from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Callable

from .models import MediaType, Post, Status

DAILY_LIMIT = 25  # Meta content-publishing limit per rolling 24h (safe planning floor)

_FINISHED = "FINISHED"
_FAILED_STATES = {"ERROR", "EXPIRED"}


class PublishError(RuntimeError):
    pass


def is_due(post: Post, now: datetime) -> bool:
    if post.status != Status.APPROVED or not post.publish_at:
        return False
    try:
        dt = datetime.fromisoformat(post.publish_at)
    except ValueError:
        return False
    return dt <= now


def _wait_finished(graph, container_id: str, timeout_s: int, interval_s: int,
                   sleep: Callable[[float], None] = time.sleep) -> None:
    waited = 0
    while True:
        status = graph.container_status(container_id)
        if status == _FINISHED:
            return
        if status in _FAILED_STATES:
            raise PublishError(f"container {container_id} status={status}")
        if waited >= timeout_s:
            raise PublishError(
                f"container {container_id} not FINISHED after {timeout_s}s (last={status or 'IN_PROGRESS'})")
        sleep(interval_s)
        waited += interval_s


def _full_caption(post: Post) -> str:
    tags = " ".join(f"#{h}" for h in post.hashtags)
    return f"{post.caption}\n\n{tags}".strip() if tags else post.caption


def publish_one(post: Post, graph, host, save_fn, move_fn, *,
                poll_timeout: int = 300, poll_interval: int = 5,
                sleep: Callable[[float], None] = time.sleep) -> Post:
    """Publish one post. Idempotent: a post that already has a media_id is left untouched."""
    if post.result.media_id:
        return post  # already published — never double-post

    post.status = Status.PUBLISHING   # claim before any API call (anti double-post on re-run)
    save_fn(post)
    try:
        urls = [host.url_for(p) for p in post.images]
        if post.media_type == MediaType.CAROUSEL:
            children = [graph.create_carousel_child(u) for u in urls]
            for child in children:
                _wait_finished(graph, child, poll_timeout, poll_interval, sleep)
            container = graph.create_carousel(children, _full_caption(post))
        else:
            container = graph.create_image_container(urls[0], _full_caption(post))
        post.result.container_id = container
        _wait_finished(graph, container, poll_timeout, poll_interval, sleep)

        media_id = graph.publish(container)
        post.result.media_id = media_id   # idempotency key — recorded immediately
        try:
            post.result.permalink = graph.permalink(media_id)
        except Exception:  # noqa: BLE001 — permalink is best-effort; don't fail a live post over it
            post.result.permalink = ""
        post.result.published_at = datetime.now(timezone.utc).isoformat()
        post.result.error = None
        post.status = Status.PUBLISHED
        save_fn(post)
        move_fn(post)
    except Exception as e:  # noqa: BLE001
        post.status = Status.FAILED
        post.result.error = str(e)
        save_fn(post)
        raise
    return post
