import os
import sys
import unittest
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from igpub.models import MODE_HOLD, MediaType, Post, Status, image_asset  # noqa: E402
from igpub.publish import PublishError, id_publishable, is_due, publish_one  # noqa: E402


class FakeGraph:
    def __init__(self, fail_publish=False, status="FINISHED"):
        self.calls = []
        self.fail_publish = fail_publish
        self._status = status

    def create_image_container(self, url, caption, alt_text=""):
        self.calls.append(("img", url, alt_text)); return "C1"

    def create_carousel_child(self, url, alt_text=""):
        self.calls.append(("child", url, alt_text))
        return f"CH{sum(1 for c in self.calls if c[0]=='child')}"

    def create_carousel(self, children, caption):
        self.calls.append(("carousel", tuple(children))); return "CP"

    def container_status(self, cid):
        return self._status

    def publish(self, cid):
        self.calls.append(("publish", cid))
        if self.fail_publish:
            raise RuntimeError("boom")
        return "MEDIA123"

    def permalink(self, mid):
        return "https://instagram.com/p/abc"


class FakeHost:
    def url_for(self, key):
        return "https://u.github.io/r/" + key


def make(images=("automation/assets/x/01.jpg",), **kw):
    assets = kw.pop("assets", None) or [image_asset(i) for i in images]
    base = dict(id="x", status=Status.SCHEDULED, media_type=MediaType.IMAGE,
                publish_at="2026-07-02T19:00:00+09:00", assets=assets)
    base.update(kw)
    return Post(**base)


_NOSLEEP = lambda s: None  # noqa: E731


class TestPublishOne(unittest.TestCase):
    def test_image_success(self):
        saved, moved = [], []
        post = make()
        publish_one(post, FakeGraph(), FakeHost(), lambda p: saved.append(p.status),
                    lambda p: moved.append(p.id), poll_interval=0, sleep=_NOSLEEP)
        self.assertEqual(post.status, Status.PUBLISHED)
        self.assertEqual(post.result.media_id, "MEDIA123")
        self.assertEqual(moved, ["x"])
        self.assertIn(Status.PUBLISHING, saved)   # claimed before the publish call

    def test_alt_text_forwarded(self):
        post = make(assets=[image_asset("automation/assets/x/01.jpg", alt_text="a flowing wave")])
        g = FakeGraph()
        publish_one(post, g, FakeHost(), lambda p: None, lambda p: None, poll_interval=0, sleep=_NOSLEEP)
        img = [c for c in g.calls if c[0] == "img"][0]
        self.assertEqual(img[2], "a flowing wave")

    def test_idempotent_skip(self):
        post = make()
        post.result.media_id = "ALREADY"
        g = FakeGraph()
        publish_one(post, g, FakeHost(), lambda p: None, lambda p: None)
        self.assertEqual(g.calls, [])             # no API calls when already published

    def test_hold_refused(self):
        post = make(schedule_mode=MODE_HOLD)
        with self.assertRaises(PublishError):
            publish_one(post, FakeGraph(), FakeHost(), lambda p: None, lambda p: None)

    def test_reels_not_implemented(self):
        post = make(media_type=MediaType.REELS)
        with self.assertRaises(PublishError):
            publish_one(post, FakeGraph(), FakeHost(), lambda p: None, lambda p: None)

    def test_head_check_blocks_unreachable(self):
        post = make()
        with self.assertRaises(PublishError):
            publish_one(post, FakeGraph(), FakeHost(), lambda p: None, lambda p: None,
                        poll_interval=0, sleep=_NOSLEEP, head_check=lambda u: False)

    def test_failure_marks_failed_and_not_moved(self):
        moved = []
        post = make()
        with self.assertRaises(RuntimeError):
            publish_one(post, FakeGraph(fail_publish=True), FakeHost(), lambda p: None,
                        lambda p: moved.append(p.id), poll_interval=0, sleep=_NOSLEEP)
        self.assertEqual(post.status, Status.FAILED)
        self.assertTrue(post.result.error)
        self.assertEqual(moved, [])

    def test_container_error_marks_failed_not_moved(self):
        moved = []
        post = make()
        with self.assertRaises(PublishError):
            publish_one(post, FakeGraph(status="ERROR"), FakeHost(), lambda p: None,
                        lambda p: moved.append(p.id), poll_interval=0, sleep=_NOSLEEP)
        self.assertEqual(post.status, Status.FAILED)
        self.assertTrue(post.result.error)
        self.assertEqual(moved, [])

    def test_stale_publishing_with_container_refused(self):
        # crash-window: a prior run created a container + may have published before recording media_id.
        post = make(status=Status.PUBLISHING)
        post.result.container_id = "C-stale"
        g = FakeGraph()
        with self.assertRaises(PublishError):
            publish_one(post, g, FakeHost(), lambda p: None, lambda p: None)
        self.assertEqual(g.calls, [])   # refused before any API call → no double-post

    def test_carousel(self):
        post = make(media_type=MediaType.CAROUSEL, images=["a.jpg", "b.jpg"])
        g = FakeGraph()
        publish_one(post, g, FakeHost(), lambda p: None, lambda p: None, poll_interval=0, sleep=_NOSLEEP)
        kinds = [c[0] for c in g.calls]
        self.assertEqual(kinds.count("child"), 2)
        self.assertIn("carousel", kinds)
        self.assertEqual(post.result.media_id, "MEDIA123")


class TestIdPublishable(unittest.TestCase):
    def test_draft_refused(self):
        self.assertFalse(id_publishable(make(status=Status.DRAFT))[0])

    def test_hold_refused(self):
        self.assertFalse(id_publishable(make(schedule_mode=MODE_HOLD))[0])

    def test_published_status_refused(self):
        self.assertFalse(id_publishable(make(status=Status.PUBLISHED))[0])

    def test_already_media_id_refused(self):
        p = make()
        p.result.media_id = "M"
        self.assertFalse(id_publishable(p)[0])

    def test_approved_ok(self):
        self.assertTrue(id_publishable(make(status=Status.APPROVED))[0])

    def test_scheduled_ok(self):
        self.assertTrue(id_publishable(make(status=Status.SCHEDULED))[0])

    def test_failed_ok(self):
        self.assertTrue(id_publishable(make(status=Status.FAILED))[0])


class TestIsDue(unittest.TestCase):
    def test_due_past_scheduled(self):
        self.assertTrue(is_due(make(status=Status.SCHEDULED, publish_at="2020-01-01T00:00:00+00:00"),
                               datetime.now(timezone.utc)))

    def test_not_due_future(self):
        self.assertFalse(is_due(make(status=Status.SCHEDULED, publish_at="2999-01-01T00:00:00+00:00"),
                                datetime.now(timezone.utc)))

    def test_approved_but_unscheduled_not_due(self):
        self.assertFalse(is_due(make(status=Status.APPROVED, publish_at="2020-01-01T00:00:00+00:00"),
                                datetime.now(timezone.utc)))

    def test_naive_publish_at_not_due(self):   # no offset → rejected, never a TypeError crash
        self.assertFalse(is_due(make(status=Status.SCHEDULED, publish_at="2020-01-01T00:00:00"),
                                datetime.now(timezone.utc)))

    def test_hold_not_due(self):
        self.assertFalse(is_due(make(status=Status.SCHEDULED, schedule_mode=MODE_HOLD,
                                     publish_at="2020-01-01T00:00:00+00:00"),
                                datetime.now(timezone.utc)))


if __name__ == "__main__":
    unittest.main()
