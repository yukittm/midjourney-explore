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

from igpub.models import MediaType, Post, Status, image_asset  # noqa: E402


@unittest.skipUnless(HAVE_YAML, "PyYAML not installed (runs in CI / after pip install)")
class TestQueueRoundTrip(unittest.TestCase):
    def test_save_then_load(self):
        from igpub.queue import load_post, save_post

        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "2026-07-02_x.yml")
            post = Post(
                id="2026-07-02_x", status=Status.APPROVED, media_type=MediaType.IMAGE,
                publish_at="2026-07-02T19:00:00+09:00",
                assets=[image_asset("automation/assets/x/01.jpg", alt_text="a wave",
                                    provenance={"sref": "S1"})],
                caption="hi", hashtags=["a"], source_path=path,
            )
            save_post(post)
            loaded = load_post(path)
            self.assertEqual(loaded.id, "2026-07-02_x")
            self.assertEqual(loaded.status, Status.APPROVED)
            self.assertEqual(loaded.media_type, MediaType.IMAGE)
            self.assertEqual(loaded.images, ["automation/assets/x/01.jpg"])
            self.assertEqual(loaded.assets[0].alt_text, "a wave")
            self.assertEqual(loaded.assets[0].provenance, {"sref": "S1"})
            self.assertEqual(loaded.hashtags, ["a"])
            self.assertEqual(loaded.schema_version, 1)

    def test_legacy_images_file_loads(self):
        from igpub.queue import load_post

        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "old.yml")
            with open(path, "w") as f:
                f.write("id: old\nstatus: approved\nmedia_type: image\n"
                        "publish_at: '2026-07-02T19:00:00+09:00'\n"
                        "images: [automation/assets/old/01.jpg]\nalt_text: legacy alt\n")
            loaded = load_post(path)
            self.assertEqual(loaded.images, ["automation/assets/old/01.jpg"])
            self.assertEqual(loaded.assets[0].alt_text, "legacy alt")
            self.assertEqual(loaded.status, Status.SCHEDULED)  # migrated approved+publish_at → scheduled

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


class TestMoveGuard(unittest.TestCase):
    """move_to_published must refuse to overwrite an existing published record (id collision = data loss).
    Uses only os ops (no YAML) so it runs everywhere."""

    def test_refuses_overwrite(self):
        from igpub.queue import move_to_published

        with tempfile.TemporaryDirectory() as d:
            qdir = os.path.join(d, "automation", "queue")
            pubdir = os.path.join(d, "automation", "published")
            os.makedirs(qdir)
            os.makedirs(pubdir)
            path = os.path.join(qdir, "x.yml")
            open(path, "w").close()
            open(os.path.join(pubdir, "x.yml"), "w").close()   # a record with the same filename exists
            post = Post(id="x", status=Status.PUBLISHED, media_type=MediaType.IMAGE,
                        publish_at="", source_path=path)
            with self.assertRaises(FileExistsError):
                move_to_published(post, repo_root=d)
            self.assertTrue(os.path.isfile(path))   # original NOT moved/destroyed


class TestDuplicateIds(unittest.TestCase):
    def test_flags_collisions(self):
        from igpub.validate import duplicate_ids

        def p(pid):
            return Post(id=pid, status=Status.DRAFT, media_type=MediaType.IMAGE, publish_at="")

        self.assertEqual(duplicate_ids([p("a"), p("b"), p("a")]), ["a"])
        self.assertEqual(duplicate_ids([p("a"), p("b")]), [])


if __name__ == "__main__":
    unittest.main()
