"""Schedule assignment — DERIVED, never persisted. The queue YAML stays the single source of truth;
the calendar is a PURE FUNCTION of the approved posts + schedule.yml. `assign_slots()` is the only
writer of publish_at for AUTO posts; PINNED posts keep their human publish_at (and are reserved);
HOLD posts are skipped. Re-running is idempotent — existing reservations are respected.

Rolling-window math is done in UTC; slot wall-clock times are resolved in the configured IANA tz
(so DST is handled by zoneinfo, not by hand)."""
from __future__ import annotations

import os
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

from .models import MODE_AUTO, MODE_PINNED, Post, Status

SCHEDULE_PATH = "automation/schedule.yml"

_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

DEFAULT_SCHEDULE = {
    "timezone": "Asia/Tokyo",
    "slots": [{"time": "19:00"}],
    "rate": {"max_per_24h": 22, "min_gap_minutes": 180},
    "horizon_days": 21,
    "blackout": [],
    "jitter": {"min_minutes": 0, "max_minutes": 0},  # OFF by default; production enables it in schedule.yml
}


def load_schedule(repo_root: str = ".", path: str = SCHEDULE_PATH) -> dict:
    full = os.path.join(repo_root, path)
    if not os.path.isfile(full):
        return dict(DEFAULT_SCHEDULE)
    import yaml  # lazy — assign_slots() is pure and must import without PyYAML
    with open(full, "r", encoding="utf-8") as f:
        loaded = yaml.safe_load(f) or {}
    merged = dict(DEFAULT_SCHEDULE)
    merged.update(loaded)
    return merged


def _tz(name: str):
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name)
    except Exception:  # noqa: BLE001 — degrade to UTC only if the tz database is unavailable
        return timezone.utc


def _parse_aware(s: str) -> Optional[datetime]:
    try:
        dt = datetime.fromisoformat(s)
    except (ValueError, TypeError):
        return None
    return dt if dt.tzinfo else None


@dataclass
class Plan:
    assignments: list = field(default_factory=list)   # list[(Post, datetime in local tz)]
    unscheduled: list = field(default_factory=list)    # list[Post] with no free slot in the horizon

    def render(self) -> str:
        lines = [f"{'publish_at (local)':<32}id"]
        for post, dt in self.assignments:
            lines.append(f"{dt.isoformat():<32}{post.id}  [{post.media_type.value}]")
        if self.unscheduled:
            lines.append(f"-- {len(self.unscheduled)} unscheduled (no free slot within horizon):")
            for p in self.unscheduled:
                lines.append(f"   {p.id} [{p.media_type.value}]")
        return "\n".join(lines)


def _hm_to_min(s: str) -> int:
    h, m = str(s).split(":")
    return int(h) * 60 + int(m)


def _slot_datetime(slot: dict, day, tz) -> datetime:
    """A slot's local datetime for `day`. `time: "19:00"` → that exact minute. `window: ["08:00","23:30"]`
    → a DETERMINISTIC-random minute inside the window, seeded by the day (so each day differs and re-plan
    is stable). The window is the human-like spread (global audience → any time except JST deep night)."""
    win = slot.get("window")
    if win and len(win) == 2:
        lo, hi = _hm_to_min(win[0]), _hm_to_min(win[1])
        if hi < lo:
            lo, hi = hi, lo
        m = random.Random(f"slotwin|{day.isoformat()}|{lo}-{hi}").randint(lo, hi)
        return datetime(day.year, day.month, day.day, m // 60, m % 60, tzinfo=tz)
    hh, mm = str(slot.get("time", "19:00")).split(":")
    return datetime(day.year, day.month, day.day, int(hh), int(mm), tzinfo=tz)


def _candidate_slots(schedule: dict, now_local: datetime, tz) -> list[tuple[datetime, list]]:
    """Future slot datetimes (local, tz-aware) over the horizon, each with its allowed media types."""
    slots = schedule.get("slots") or DEFAULT_SCHEDULE["slots"]
    horizon = int(schedule.get("horizon_days", 21))
    blackout = set(schedule.get("blackout") or [])
    out: list[tuple[datetime, list]] = []
    start = now_local.date()
    for day_offset in range(horizon + 1):
        day = start + timedelta(days=day_offset)
        if day.isoformat() in blackout:
            continue
        dow = _DAYS[day.weekday()]
        for slot in slots:
            allowed_days = [d.lower() for d in (slot.get("days") or _DAYS)]
            if dow not in allowed_days:
                continue
            cand = _slot_datetime(slot, day, tz)
            if cand <= now_local:
                continue
            allowed_types = [t.lower() for t in (slot.get("media_types") or [])]
            out.append((cand, allowed_types))
    out.sort(key=lambda x: x[0])
    return out


def _jittered(cand_local: datetime, post_id: str, jcfg: dict, now_local: datetime) -> datetime:
    """Nudge a slot off its exact minute by a DETERMINISTIC per-post-per-day offset (human-like — posts
    don't fire on the dot). Seeded by post id + slot date, so it's identical across re-plans and is
    written into publish_at (fully auditable). Never pushed into the past. min==max==0 → no jitter."""
    lo = int((jcfg or {}).get("min_minutes", 0))
    hi = int((jcfg or {}).get("max_minutes", 0))
    if lo == 0 and hi == 0:
        return cand_local
    if hi < lo:
        lo, hi = hi, lo
    off = random.Random(f"{post_id}|{cand_local.date().isoformat()}").randint(lo, hi)
    jittered = cand_local + timedelta(minutes=off)
    return jittered if jittered > now_local else cand_local


def assign_slots(posts: list[Post], schedule: dict, now: datetime) -> Plan:
    """Place AUTO posts into the next free slots; reserve PINNED/already-SCHEDULED times. Mutates the
    placed posts in place (publish_at + status=SCHEDULED) so the caller can save them; returns a Plan."""
    tz = _tz(schedule.get("timezone", "Asia/Tokyo"))
    now_local = now.astimezone(tz)
    rate = schedule.get("rate") or {}
    max_per_24h = int(rate.get("max_per_24h", 22))
    min_gap_s = int(rate.get("min_gap_minutes", 180)) * 60
    jcfg = schedule.get("jitter") or {}

    plan = Plan()
    taken: list[datetime] = []  # occupied times, UTC-aware

    # 1) reservations: pinned + already-scheduled posts hold their publish_at
    for p in posts:
        if p.schedule_mode == MODE_PINNED or p.status == Status.SCHEDULED:
            dt = _parse_aware(p.publish_at)
            if not dt:
                continue
            taken.append(dt.astimezone(timezone.utc))
            if p.status == Status.APPROVED and p.schedule_mode == MODE_PINNED:
                p.status = Status.SCHEDULED
            plan.assignments.append((p, dt.astimezone(tz)))

    # 2) autos to place: approved, auto-mode, not yet scheduled
    autos = [p for p in posts if p.status == Status.APPROVED and p.schedule_mode == MODE_AUTO]
    autos.sort(key=lambda p: (-p.priority, p.approved_at or "~", p.id))  # priority desc, then FIFO

    candidates = _candidate_slots(schedule, now_local, tz)
    for p in autos:
        placed = False
        for cand_local, allowed in candidates:
            if allowed and p.media_type.value not in allowed:
                continue
            cand_utc = cand_local.astimezone(timezone.utc)
            if any(abs((cand_utc - t).total_seconds()) < min_gap_s for t in taken):
                continue
            # per-24h cap: a ±24h-window approximation (exact at the default 1 slot/day). The HARD
            # backstop against Meta's real limit is the publish-time content_publishing_limit pre-check
            # (publish.py runner); a rigorous rolling-window planner is deferred to the FULL build.
            if sum(1 for t in taken if abs((cand_utc - t).total_seconds()) < 24 * 3600) >= max_per_24h:
                continue
            fire_local = _jittered(cand_local, p.id, jcfg, now_local)  # human-like offset, recorded
            p.publish_at = fire_local.isoformat()
            p.status = Status.SCHEDULED
            taken.append(fire_local.astimezone(timezone.utc))
            plan.assignments.append((p, fire_local))
            placed = True
            break
        if not placed:
            plan.unscheduled.append(p)

    plan.assignments.sort(key=lambda x: x[1])
    return plan
