"""Domain models — pure data + (de)serialization, no I/O.

A Post is a discriminated container (`media_type`) over an ordered list of `Asset`s. This single
shape covers every IG post type (image · mixed carousel · reels · story); adding a type is additive
(an enum value + a validation branch + a Graph call-mapping), never a core rewrite. See
`automation/asset-queue-model.md`.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum

SCHEMA_VERSION = 1


class Status(str, Enum):
    DRAFT = "draft"            # work in progress
    APPROVED = "approved"      # human-approved, but not yet placed on the calendar
    SCHEDULED = "scheduled"    # has a publish_at slot — the ONLY state is_due() will publish
    PUBLISHING = "publishing"  # claimed by the runner (anti double-post)
    PUBLISHED = "published"
    FAILED = "failed"


class MediaType(str, Enum):
    IMAGE = "image"
    CAROUSEL = "carousel"
    REELS = "reels"
    STORY = "story"


# schedule_mode — how publish_at is decided (orthogonal to status)
MODE_AUTO = "auto"      # the assigner computes publish_at from schedule.yml
MODE_PINNED = "pinned"  # human-fixed publish_at; the assigner never moves it
MODE_HOLD = "hold"      # excluded from the calendar AND from publishing
VALID_MODES = (MODE_AUTO, MODE_PINNED, MODE_HOLD)


@dataclass
class Asset:
    """One image or video. A post's `assets` list is ordered; each maps to a Graph child container."""
    kind: str = "image"                              # "image" | "video"
    key: str = ""                                    # host-agnostic key → adapter resolves path AND URL
    alt_text: str = ""                               # image only
    user_tags: list = field(default_factory=list)    # image only (product/user tags)
    cover: str | None = None                         # video only — cover-image key
    thumb_offset_ms: int | None = None               # video only
    provenance: dict = field(default_factory=dict)    # PER-asset (mj_prompt/sref/sv/params/lut/...)
    result: dict = field(default_factory=dict)        # per-child container_id etc.

    @classmethod
    def from_dict(cls, d: dict) -> "Asset":
        d = d or {}
        return cls(
            kind=d.get("kind", "image") or "image",
            key=d.get("key", "") or "",
            alt_text=d.get("alt_text", "") or "",
            user_tags=list(d.get("user_tags") or []),
            cover=d.get("cover"),
            thumb_offset_ms=d.get("thumb_offset_ms"),
            provenance=dict(d.get("provenance") or {}),
            result=dict(d.get("result") or {}),
        )

    def to_dict(self) -> dict:
        out: dict = {"kind": self.kind, "key": self.key}
        if self.kind == "image":
            if self.alt_text:
                out["alt_text"] = self.alt_text
            if self.user_tags:
                out["user_tags"] = list(self.user_tags)
        else:  # video
            if self.cover:
                out["cover"] = self.cover
            if self.thumb_offset_ms is not None:
                out["thumb_offset_ms"] = self.thumb_offset_ms
        if self.provenance:
            out["provenance"] = dict(self.provenance)
        if self.result:
            out["result"] = dict(self.result)
        return out


def image_asset(key: str, alt_text: str = "", provenance: dict | None = None) -> Asset:
    """Terse constructor for the common case (an image with optional alt text + provenance)."""
    return Asset(kind="image", key=key, alt_text=alt_text, provenance=dict(provenance or {}))


@dataclass
class Result:
    container_id: str | None = None
    media_id: str | None = None        # set immediately after publish == idempotency key
    permalink: str | None = None
    published_at: str | None = None
    error: str | None = None
    error_class: str | None = None     # transient | rate_limit | container_error | host_unreachable | fatal
    retry_count: int = 0
    next_retry_at: str | None = None
    attempts: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict | None) -> "Result":
        d = d or {}
        return cls(
            container_id=d.get("container_id"),
            media_id=d.get("media_id"),
            permalink=d.get("permalink"),
            published_at=d.get("published_at"),
            error=d.get("error"),
            error_class=d.get("error_class"),
            retry_count=int(d.get("retry_count") or 0),
            next_retry_at=d.get("next_retry_at"),
            attempts=list(d.get("attempts") or []),
        )


def assemble_caption(post: "Post") -> str:
    """The EXACT caption string sent to the API (caption + a blank line + space-joined #hashtags).
    Used by both the validator (length check) and the publisher (so they never disagree)."""
    tags = " ".join(f"#{h}" for h in post.hashtags)
    return f"{post.caption}\n\n{tags}".strip() if tags else post.caption


@dataclass
class Post:
    id: str
    status: Status
    media_type: MediaType
    publish_at: str = ""                               # ISO 8601 WITH offset, e.g. ...+09:00
    assets: list[Asset] = field(default_factory=list)   # ordered
    caption: str = ""
    hashtags: list[str] = field(default_factory=list)   # without the leading '#'
    location_id: str | None = None
    share_to_feed: bool = True                          # reels: also show in the main feed
    audio_name: str | None = None                       # reels: pre-licensed/original audio only
    collaborators: list = field(default_factory=list)
    schedule_mode: str = MODE_AUTO                      # auto | pinned | hold
    priority: int = 0                                   # higher = assigned a slot first
    approved_at: str | None = None
    deleted_from_ig: bool = False                       # manually removed from IG post-publish (curation)
    schema_version: int = SCHEMA_VERSION
    result: Result = field(default_factory=Result)
    source_path: str | None = None                      # queue file it came from (not serialized)

    @property
    def images(self) -> list[str]:
        """Back-compat read accessor: image asset keys, in order."""
        return [a.key for a in self.assets if a.kind == "image"]

    @property
    def videos(self) -> list[str]:
        return [a.key for a in self.assets if a.kind == "video"]

    @classmethod
    def from_dict(cls, d: dict, source_path: str | None = None) -> "Post":
        ver = int(d.get("schema_version", 0) or 0)   # absent → 0 (legacy, pre-Asset model)
        status = Status(d.get("status", "draft"))

        # assets: new canonical 'assets:' list, else synthesize from legacy 'images:'
        # (carrying the old top-level alt_text/provenance onto each synthesized image asset).
        raw_assets = d.get("assets")
        if raw_assets:
            assets = [Asset.from_dict(a) for a in raw_assets]
        else:
            legacy_alt = d.get("alt_text", "") or ""
            legacy_prov = dict(d.get("provenance") or {})
            assets = [Asset(kind="image", key=img, alt_text=legacy_alt, provenance=dict(legacy_prov))
                      for img in (d.get("images") or [])]

        # Legacy migration: pre-schema_version, 'approved' + publish_at meant "due". is_due() now
        # gates on SCHEDULED, so promote those legacy rows; 'approved' with no publish_at stays a
        # backlog item (NOT silently due).
        if ver < 1 and status == Status.APPROVED and d.get("publish_at"):
            status = Status.SCHEDULED

        return cls(
            id=d["id"],
            status=status,
            media_type=MediaType(d.get("media_type", "image")),
            publish_at=d.get("publish_at", "") or "",
            assets=assets,
            caption=d.get("caption", "") or "",
            hashtags=list(d.get("hashtags") or []),
            location_id=d.get("location_id"),
            share_to_feed=bool(d.get("share_to_feed", True)),
            audio_name=d.get("audio_name"),
            collaborators=list(d.get("collaborators") or []),
            schedule_mode=d.get("schedule_mode", MODE_AUTO) or MODE_AUTO,
            priority=int(d.get("priority") or 0),
            approved_at=d.get("approved_at"),
            deleted_from_ig=bool(d.get("deleted_from_ig", False)),
            schema_version=SCHEMA_VERSION,
            result=Result.from_dict(d.get("result")),
            source_path=source_path,
        )

    def to_dict(self) -> dict:
        out: dict = {
            "id": self.id,
            "schema_version": self.schema_version,
            "status": self.status.value,
            "media_type": self.media_type.value,
            "publish_at": self.publish_at,
            "assets": [a.to_dict() for a in self.assets],
            "caption": self.caption,
            "hashtags": list(self.hashtags),
        }
        if self.location_id:
            out["location_id"] = self.location_id
        if self.media_type == MediaType.REELS:
            out["share_to_feed"] = self.share_to_feed
            if self.audio_name:
                out["audio_name"] = self.audio_name
        if self.collaborators:
            out["collaborators"] = list(self.collaborators)
        out["schedule_mode"] = self.schedule_mode
        out["priority"] = self.priority
        if self.approved_at:
            out["approved_at"] = self.approved_at
        if self.deleted_from_ig:
            out["deleted_from_ig"] = True
        out["result"] = asdict(self.result)
        return out
