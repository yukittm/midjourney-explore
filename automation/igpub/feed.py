"""Instagram-style feed-grid PREVIEW — pure ordering + HTML rendering (no I/O, no network).

Projects how the profile feed will look once the queue is posted: newest at top-left, 3 across.
Order top→bottom = approved-but-unscheduled (will post soonest) → scheduled (by publish_at desc)
→ published (by published_at desc). draft / hold / publishing / failed are excluded from the
projection. The CLI (`automation/feed_preview.py`) loads the records, writes the HTML, opens it.
"""
from __future__ import annotations

import html
from dataclasses import dataclass
from datetime import datetime, timezone

from .models import Post, Status

# statuses that belong on the projected feed
_LANE = {
    Status.APPROVED: ("upcoming", 2),
    Status.SCHEDULED: ("upcoming", 1),
    Status.PUBLISHED: ("live", 0),
}
_NEG_INF = float("-inf")


@dataclass
class FeedTile:
    id: str
    image_rel: str | None    # path relative to the HTML file (which lives in automation/), or None
    status: str
    lane: str                # "upcoming" | "live"
    when: str                # human label: publish_at / published_at / "unscheduled"
    caption_line: str        # first caption line (raw; escaped at render time)


def _ts(s: str | None) -> float:
    if not s:
        return _NEG_INF
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return _NEG_INF
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


def _first_caption_line(caption: str, limit: int = 64) -> str:
    line = (caption or "").strip().splitlines()[0] if (caption or "").strip() else ""
    return line if len(line) <= limit else line[: limit - 1] + "…"


def _image_rel(post: Post) -> str | None:
    """First image asset's key made relative to automation/ (where the HTML file lives)."""
    for a in post.assets:
        if a.kind == "image" and a.key:
            return a.key[len("automation/"):] if a.key.startswith("automation/") else a.key
    return None


def build_tiles(posts: list[Post], include_drafts: bool = False) -> list[FeedTile]:
    """Filter to the projected feed and order it as IG will show it (newest first). `include_drafts`
    (used by Feed Studio, not the static preview) also surfaces DRAFT posts as upcoming tiles so a
    just-committed select doesn't vanish from the grid."""
    lanes = dict(_LANE)
    if include_drafts:
        lanes[Status.DRAFT] = ("upcoming", 3)   # least-scheduled → top of the upcoming block
    rows = []
    for p in posts:
        if p.status not in lanes:
            continue
        if getattr(p, "deleted_from_ig", False):   # removed from the live grid post-publish
            continue
        lane, rank = lanes[p.status]
        if p.status == Status.PUBLISHED:
            when = p.result.published_at or ""
            sort_ts = _ts(when)
        elif p.status == Status.SCHEDULED:
            when = p.publish_at or ""
            sort_ts = _ts(when)
        else:  # APPROVED or DRAFT — no scheduled time yet
            when = "draft" if p.status == Status.DRAFT else "unscheduled"
            sort_ts = _NEG_INF
        rows.append((rank, sort_ts, p.priority, p, lane, when))
    # newest first: lane rank desc, then time desc, then priority desc, then id desc (stable)
    rows.sort(key=lambda r: (r[0], r[1], r[2], r[3].id), reverse=True)
    return [
        FeedTile(id=p.id, image_rel=_image_rel(p), status=p.status.value, lane=lane,
                 when=when, caption_line=_first_caption_line(p.caption))
        for (_rank, _ts_, _prio, p, lane, when) in rows
    ]


def counts(tiles: list[FeedTile]) -> dict:
    return {
        "total": len(tiles),
        "upcoming": sum(1 for t in tiles if t.lane == "upcoming"),
        "live": sum(1 for t in tiles if t.lane == "live"),
    }


def render_html(tiles: list[FeedTile], *, generated_at: str = "") -> str:
    """Self-contained HTML (inline CSS, no deps). Tiles are 4:5 (the post AR); upcoming posts carry a
    dashed accent + status badge so the projection reads clearly against the live grid."""
    c = counts(tiles)
    cells = []
    for t in tiles:
        cap = html.escape(t.caption_line) or "<span class='muted'>— no caption yet —</span>"
        when = html.escape(t.when)
        badge = html.escape(t.status)
        if t.image_rel:
            media = f"<img loading='lazy' src='{html.escape(t.image_rel)}' alt=''>"
        else:
            media = "<div class='noimg'>no image</div>"
        cells.append(
            f"<figure class='tile {t.lane}'>{media}"
            f"<figcaption><span class='badge {t.lane}'>{badge}</span>"
            f"<span class='when'>{when}</span>"
            f"<span class='cap'>{cap}</span>"
            f"<span class='id'>{html.escape(t.id)}</span></figcaption></figure>"
        )
    grid = "\n".join(cells) or "<p class='muted'>No approved / scheduled / published posts yet.</p>"
    gen = html.escape(generated_at)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Feed preview — @tim.bankrupt</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin:0; background:#0b0b0d; color:#e8e8ea;
         font:14px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }}
  header {{ position:sticky; top:0; background:#0b0b0dcc; backdrop-filter:blur(8px);
            padding:14px 18px; border-bottom:1px solid #222; }}
  h1 {{ font-size:15px; margin:0 0 4px; font-weight:600; }}
  .meta {{ color:#9a9aa2; font-size:12px; }}
  .legend span {{ margin-right:14px; }}
  .dot {{ display:inline-block; width:8px; height:8px; border-radius:2px; margin-right:5px; vertical-align:middle; }}
  .dot.upcoming {{ background:#f5b301; }} .dot.live {{ background:#3aa3ff; }}
  .wrap {{ max-width:880px; margin:0 auto; padding:16px; }}
  .grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:3px; }}
  figure {{ margin:0; position:relative; aspect-ratio:4/5; background:#16161a; overflow:hidden; }}
  figure img {{ width:100%; height:100%; object-fit:cover; display:block; }}
  .noimg {{ display:flex; align-items:center; justify-content:center; height:100%; color:#666; font-size:12px; }}
  figure.upcoming {{ outline:2px dashed #f5b30188; outline-offset:-2px; }}
  figcaption {{ position:absolute; inset:auto 0 0 0; padding:18px 6px 5px;
    background:linear-gradient(transparent,#000a 55%); font-size:10px; opacity:0; transition:.15s;
    display:flex; flex-direction:column; gap:1px; }}
  figure:hover figcaption {{ opacity:1; }}
  .badge {{ position:absolute; top:5px; left:5px; padding:1px 5px; border-radius:3px; font-size:9px;
    font-weight:600; opacity:.92; }}
  .badge.upcoming {{ background:#f5b301; color:#222; }} .badge.live {{ background:#3aa3ff; color:#04121f; }}
  .when {{ color:#cfcfd6; }} .cap {{ color:#fff; }} .id {{ color:#8a8a92; }}
  .muted {{ color:#777; }}
</style></head>
<body>
<header>
  <h1>Feed preview — @tim.bankrupt</h1>
  <div class="meta">{c['total']} tiles · <span class="legend"><span class="dot upcoming"></span>{c['upcoming']} upcoming (approved/scheduled) <span class="dot live"></span>{c['live']} live</span> · newest top-left · tiles shown at 4:5 (post AR){' · ' + gen if gen else ''}</div>
</header>
<div class="wrap"><div class="grid">
{grid}
</div></div>
</body></html>
"""
