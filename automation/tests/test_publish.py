import os
import sys
import unittest
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from igpub.models import MediaType, Post, Status  # noqa: E402
from igpub.publish import is_due, publish_one  # noqa: E402


class FakeGraph:
    def __init__(self, fail_publish=False):
        self.calls = []
        self.fail_publish = fail_publish

    def create_image_container(self, url, caption):
        self.calls.append(("img", url)); return "C1"

    def create_carousel_child(self, url):
        self.calls.append(("child", url)); return f"CH{sum(1 for c in self.calls if c[0]=='child')}"

    def create_carousel(self, children, caption):
        self.calls.append(("carousel", tuple(children))); return "CP"

    def container_status(self, cid):
        return "FINISHED"

    def publish(self, cid):
        self.calls.append(("publish", cid))
        if self.fail_publish:
            raise RuntimeError("boom")
        return "MEDIA123"

    def permalink(self, mid):
        return "https://instagram.com/p/abc"


class FakeHost:
    def url_for(self, p):
        return "https://u.github.io/r/" + p


def make(**kw):
    base = dict(id="x", status=Status.APPROVED, media_type=MediaType.IMAGE,
                publish_at="2026-07-02T19:00:00+09:00", images=["automation/assets/x/01.jpg"])
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

    def test_idempotent_skip(self):
        post = make()
        post.result.media_id = "ALREADY"
        g = FakeGraph()
        publish_one(post, g, FakeHost(), lambda p: None, lambda p: None)
        self.assertEqual(g.calls, [])             # no API calls when already published

    def test_failure_marks_failed_and_not_moved(self):
        moved = []
        post = make()
        with self.assertRaises(RuntimeError):
            publish_one(post, FakeGraph(fail_publish=True), FakeHost(), lambda p: None,
                        lambda p: moved.append(p.id), poll_interval=0, sleep=_NOSLEEP)
        self.assertEqual(post.status, Status.FAILED)
        self.assertTrue(post.result.error)
        self.assertEqual(moved, [])

    def test_carousel(self):
        post = make(media_type=MediaType.CAROUSEL, images=["a.jpg", "b.jpg"])
        g = FakeGraph()
        publish_one(post, g, FakeHost(), lambda p: None, lambda p: None, poll_interval=0, sleep=_NOSLEEP)
        kinds = [c[0] for c in g.calls]
        self.assertEqual(kinds.count("child"), 2)
        self.assertIn("carousel", kinds)
        self.assertEqual(post.result.media_id, "MEDIA123")


class TestIsDue(unittest.TestCase):
    def test_due_past(self):
        self.assertTrue(is_due(make(publish_at="2020-01-01T00:00:00+00:00"), datetime.now(timezone.utc)))

    def test_not_due_future(self):
        self.assertFalse(is_due(make(publish_at="2999-01-01T00:00:00+00:00"), datetime.now(timezone.utc)))

    def test_not_approved(self):
        self.assertFalse(is_due(make(status=Status.DRAFT, publish_at="2020-01-01T00:00:00+00:00"),
                                datetime.now(timezone.utc)))


if __name__ == "__main__":
    unittest.main()
