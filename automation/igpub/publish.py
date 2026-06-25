"""Publish orchestration — the flow runs over INJECTED dependencies (graph client, image host,
save/move callbacks, optional reachability probe), so it is unit-testable with fakes (no network,
no YAML).

Order matters for safety:
  1. skip if a media_id already exists (idempotent — never double-post);
  2. refuse a held post; refuse not-yet-implemented types (reels/story) loudly;
  3. claim the row (status=PUBLISHING + save) BEFORE any API call;
  4. resolve + reachability-probe each asset URL (Pages/R2 propagation lag = retriable, not a silent ERROR);
  5. create container(s) → poll to FINISHED (bounded; ERROR/EXPIRED/timeout = failure) → publish;
  6. write the returned media_id immediately (the idempotency key), then status=PUBLISHED + move;
  7. on any failure → status=FAILED + error + save (loud, not silent).
"""
from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Callable, Optional

from .models import MODE_HOLD, MediaType, Post, Status, assemble_caption

DAILY_LIMIT = 50  # self-imposed planning cap (Meta's real content-publishing limit is ~100/24h)

_FINISHED = "FINISHED"
_FAILED_STATES = {"ERROR", "EXPIRED"}

# Reachability probe: given a public URL, return True if it is fetchable (HEAD 200). Optional —
# default None skips the probe (e.g. in unit tests with fake hosts).
HeadCheck = Callable[[str], bool]


class PublishError(RuntimeError):
    pass


def is_due(post: Post, now: datetime) -> bool:
    """True only for a SCHEDULED, non-held post whose tz-aware publish_at is in the past."""
    if post.status != Status.SCHEDULED or post.schedule_mode == MODE_HOLD or not post.publish_at:
        return False
    try:
        dt = datetime.fromisoformat(post.publish_at)
    except (ValueError, TypeError):
        return False
    if dt.tzinfo is None:        # naive publish_at is invalid — reject, never crash comparing to tz-aware now
        return False
    return dt <= now


def id_publishable(post: Post) -> "tuple[bool, str]":
    """Gate for the manual `--id` path: --id overrides the SCHEDULE, never the approval gate.
    Returns (ok, reason). Refuses draft / hold / already-published; allows approved/scheduled/failed/
    publishing (a stale PUBLISHING that already has a container is caught separately by publish_one)."""
    if post.result.media_id:
        return False, f"already published ({post.result.media_id})"
    if post.schedule_mode == MODE_HOLD:
        return False, "on hold (schedule_mode=hold)"
    if post.status == Status.DRAFT:
        return False, "status=draft (approve it first)"
    if post.status == Status.PUBLISHED:
        return False, "status=published"
    return True, ""


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


def publish_one(post: Post, graph, host, save_fn, move_fn, *,
                poll_timeout: int = 300, poll_interval: int = 5,
                sleep: Callable[[float], None] = time.sleep,
                head_check: Optional[HeadCheck] = None) -> Post:
    """Publish one post. Idempotent: a post that already has a media_id is left untouched."""
    if post.result.media_id:
        return post  # already published — never double-post
    if post.status == Status.PUBLISHING and post.result.container_id:
        # A prior run already created a container and may have published before it could record the
        # media_id (the crash window). Re-publishing blind would risk a DOUBLE POST → stop and ask for
        # a manual reconcile: check Instagram, and if it went live set result.media_id by hand.
        raise PublishError(
            f"post {post.id} is mid-publish (container {post.result.container_id}, no media_id) — check "
            f"Instagram and set result.media_id manually if it went live; refusing to avoid a double-post")
    if post.schedule_mode == MODE_HOLD:
        raise PublishError(f"post {post.id} is on hold (schedule_mode=hold); not publishing")
    if post.media_type in (MediaType.REELS, MediaType.STORY):
        raise PublishError(
            f"media_type={post.media_type.value} is not implemented yet (MINIMAL = image/carousel only)")

    post.status = Status.PUBLISHING   # claim before any API call (anti double-post on re-run)
    save_fn(post)
    try:
        # resolve each asset's public URL + probe reachability BEFORE any Graph call
        resolved = []
        for a in post.assets:
            url = host.url_for(a.key)
            if head_check is not None and not head_check(url):
                raise PublishError(f"asset URL not reachable yet (host propagation?): {url}")
            resolved.append((a, url))

        caption = assemble_caption(post)
        if post.media_type == MediaType.CAROUSEL:
            children: list[str] = []
            for a, url in resolved:
                child = graph.create_carousel_child(url, alt_text=a.alt_text)
                a.result["container_id"] = child
                children.append(child)
            for child in children:
                _wait_finished(graph, child, poll_timeout, poll_interval, sleep)
            container = graph.create_carousel(children, caption)
        else:  # IMAGE
            a, url = resolved[0]
            container = graph.create_image_container(url, caption, alt_text=a.alt_text)
        post.result.container_id = container
        save_fn(post)   # persist the container id BEFORE media_publish → re-run hits the crash-window stop
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
