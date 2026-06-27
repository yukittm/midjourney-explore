import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from igpub.feed import build_tiles, counts, render_html  # noqa: E402
from igpub.models import MediaType, Post, Result, Status, image_asset  # noqa: E402


def post(pid, status, *, publish_at="", published_at="", caption="", priority=0,
         key="automation/assets/x/01.jpg"):
    return Post(id=pid, status=status, media_type=MediaType.IMAGE, publish_at=publish_at,
                assets=[image_asset(key)], caption=caption, priority=priority,
                result=Result(published_at=published_at or None))


class TestFeedOrder(unittest.TestCase):
    def test_excludes_draft_hold_failed(self):
        posts = [post("d", Status.DRAFT), post("f", Status.FAILED)]
        self.assertEqual(build_tiles(posts), [])

    def test_lane_order_upcoming_above_live(self):
        tiles = build_tiles([
            post("live1", Status.PUBLISHED, published_at="2026-06-27T16:00:00+00:00"),
            post("sched1", Status.SCHEDULED, publish_at="2026-07-01T09:00:00+00:00"),
            post("appr1", Status.APPROVED),
        ])
        ids = [t.id for t in tiles]
        self.assertEqual(ids, ["appr1", "sched1", "live1"])  # approved → scheduled → published
        self.assertEqual([t.lane for t in tiles], ["upcoming", "upcoming", "live"])

    def test_scheduled_newest_first(self):
        tiles = build_tiles([
            post("early", Status.SCHEDULED, publish_at="2026-07-01T09:00:00+00:00"),
            post("late", Status.SCHEDULED, publish_at="2026-07-05T09:00:00+00:00"),
        ])
        self.assertEqual([t.id for t in tiles], ["late", "early"])

    def test_published_newest_first(self):
        tiles = build_tiles([
            post("old", Status.PUBLISHED, published_at="2026-06-20T10:00:00+00:00"),
            post("new", Status.PUBLISHED, published_at="2026-06-27T10:00:00+00:00"),
        ])
        self.assertEqual([t.id for t in tiles], ["new", "old"])

    def test_mixed_timezone_offsets_sort_correctly(self):
        # 2026-07-01T09:00+09:00 (00:00 UTC) is EARLIER than 2026-07-01T09:00+00:00 (09:00 UTC)
        tiles = build_tiles([
            post("jst", Status.SCHEDULED, publish_at="2026-07-01T09:00:00+09:00"),
            post("utc", Status.SCHEDULED, publish_at="2026-07-01T09:00:00+00:00"),
        ])
        self.assertEqual([t.id for t in tiles], ["utc", "jst"])  # utc is later → first

    def test_image_rel_strips_automation_prefix(self):
        t = build_tiles([post("p", Status.PUBLISHED, published_at="2026-06-27T10:00:00+00:00",
                              key="automation/assets/p/01.jpg")])[0]
        self.assertEqual(t.image_rel, "assets/p/01.jpg")

    def test_deleted_from_ig_excluded(self):
        p = post("gone", Status.PUBLISHED, published_at="2026-06-27T10:00:00+00:00")
        p.deleted_from_ig = True
        live = post("here", Status.PUBLISHED, published_at="2026-06-26T10:00:00+00:00")
        self.assertEqual([t.id for t in build_tiles([p, live])], ["here"])

    def test_counts(self):
        tiles = build_tiles([
            post("a", Status.APPROVED),
            post("s", Status.SCHEDULED, publish_at="2026-07-01T09:00:00+00:00"),
            post("p", Status.PUBLISHED, published_at="2026-06-27T10:00:00+00:00"),
        ])
        self.assertEqual(counts(tiles), {"total": 3, "upcoming": 2, "live": 1})


class TestRenderHtml(unittest.TestCase):
    def test_renders_tiles_and_escapes_caption(self):
        tiles = build_tiles([post("p", Status.PUBLISHED, published_at="2026-06-27T10:00:00+00:00",
                                  caption="teal & gold <not a tag>")])
        out = render_html(tiles, generated_at="gen now")
        self.assertIn("assets/x/01.jpg", out)
        self.assertIn("teal &amp; gold &lt;not a tag&gt;", out)  # escaped
        self.assertNotIn("<not a tag>", out)
        self.assertIn("gen now", out)

    def test_empty_grid_message(self):
        out = render_html([], generated_at="")
        self.assertIn("No approved / scheduled / published posts yet.", out)

    def test_no_image_placeholder(self):
        from igpub.models import Asset
        p = Post(id="v", status=Status.PUBLISHED, media_type=MediaType.REELS,
                 assets=[Asset(kind="video", key="x.mp4")],
                 result=Result(published_at="2026-06-27T10:00:00+00:00"))
        out = render_html(build_tiles([p]))
        self.assertIn("no image", out)


if __name__ == "__main__":
    unittest.main()
