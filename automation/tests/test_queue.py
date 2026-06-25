import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    import yaml  # noqa: F401
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False

from igpub.models import MediaType, Post, Status  # noqa: E402


@unittest.skipUnless(HAVE_YAML, "PyYAML not installed (runs in CI / after pip install)")
class TestQueueRoundTrip(unittest.TestCase):
    def test_save_then_load(self):
        from igpub.queue import load_post, save_post

        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "2026-07-02_x.yml")
            post = Post(
                id="2026-07-02_x", status=Status.APPROVED, media_type=MediaType.IMAGE,
                publish_at="2026-07-02T19:00:00+09:00",
                images=["automation/assets/x/01.jpg"], caption="hi", hashtags=["a"],
                source_path=path,
            )
            save_post(post)
            loaded = load_post(path)
            self.assertEqual(loaded.id, "2026-07-02_x")
            self.assertEqual(loaded.status, Status.APPROVED)
            self.assertEqual(loaded.media_type, MediaType.IMAGE)
            self.assertEqual(loaded.images, ["automation/assets/x/01.jpg"])
            self.assertEqual(loaded.hashtags, ["a"])

    def test_move_to_published(self):
        from igpub.queue import move_to_published

        with tempfile.TemporaryDirectory() as d:
            qdir = os.path.join(d, "automation", "queue")
            os.makedirs(qdir)
            path = os.path.join(qdir, "2026-07-02_x.yml")
            with open(path, "w") as f:
                f.write("id: x\n")
            post = Post(id="x", status=Status.PUBLISHED, media_type=MediaType.IMAGE,
                        publish_at="", source_path=path)
            dest = move_to_published(post, repo_root=d)
            self.assertTrue(os.path.isfile(dest))
            self.assertFalse(os.path.isfile(path))
            self.assertIn(os.path.join("automation", "published"), dest)


if __name__ == "__main__":
    unittest.main()
