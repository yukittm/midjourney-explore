"""Domain models — pure data + (de)serialization, no I/O."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum


class Status(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"      # the gate: only approved posts are ever published
    PUBLISHING = "publishing"  # claimed by the runner (anti double-post)
    PUBLISHED = "published"
    FAILED = "failed"


class MediaType(str, Enum):
    IMAGE = "image"
    CAROUSEL = "carousel"
    REELS = "reels"


@dataclass
class Result:
    container_id: str | None = None
    media_id: str | None = None        # set immediately after publish == idempotency key
    permalink: str | None = None
    published_at: str | None = None
    error: str | None = None

    @classmethod
    def from_dict(cls, d: dict | None) -> "Result":
        d = d or {}
        return cls(
            container_id=d.get("container_id"),
            media_id=d.get("media_id"),
            permalink=d.get("permalink"),
            published_at=d.get("published_at"),
            error=d.get("error"),
        )


@dataclass
class Post:
    id: str
    status: Status
    media_type: MediaType
    publish_at: str                                    # ISO 8601 with offset, e.g. ...+09:00
    images: list[str] = field(default_factory=list)    # repo-relative local JPEG paths
    caption: str = ""
    hashtags: list[str] = field(default_factory=list)  # without the leading '#'
    alt_text: str = ""
    provenance: dict = field(default_factory=dict)     # mj_prompt / sref / lut
    result: Result = field(default_factory=Result)
    source_path: str | None = None                     # queue file it came from (not serialized)

    @classmethod
    def from_dict(cls, d: dict, source_path: str | None = None) -> "Post":
        return cls(
            id=d["id"],
            status=Status(d.get("status", "draft")),
            media_type=MediaType(d.get("media_type", "image")),
            publish_at=d.get("publish_at", "") or "",
            images=list(d.get("images") or []),
            caption=d.get("caption", "") or "",
            hashtags=list(d.get("hashtags") or []),
            alt_text=d.get("alt_text", "") or "",
            provenance=dict(d.get("provenance") or {}),
            result=Result.from_dict(d.get("result")),
            source_path=source_path,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "status": self.status.value,
            "media_type": self.media_type.value,
            "publish_at": self.publish_at,
            "images": list(self.images),
            "caption": self.caption,
            "hashtags": list(self.hashtags),
            "alt_text": self.alt_text,
            "provenance": dict(self.provenance),
            "result": asdict(self.result),
        }
