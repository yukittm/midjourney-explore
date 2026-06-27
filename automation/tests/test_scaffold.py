import os
import struct
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    import yaml  # noqa: F401
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False

from igpub.scaffold import (  # noqa: E402
    ScaffoldError, make_id, scaffold_post, validate_date, validate_slug,
)


def minimal_jpeg(width: int, height: int) -> bytes:
    return (b"\xff\xd8\xff\xc0\x00\x11\x08" + struct.pack(">HH", height, width)
            + b"\x03\x01\x22\x00\x02\x11\x01\x03\x11\x01\xff\xd9")


def write_jpeg(path: str, w: int, h: int) -> None:
    with open(path, "wb") as f:
        f.write(minimal_jpeg(w, h))


class TestSlugDateValidators(unittest.TestCase):
    def test_good_slug(self):
        validate_slug("flowing-color-surfer")  # no raise

    def test_bad_slugs(self):
        for bad in ("", "Foo", "a b", "a/b", "../escape", "a--b", "café", "trailing-"):
            with self.subTest(bad=bad), self.assertRaises(ScaffoldError):
                validate_slug(bad)

    def test_good_date(self):
        validate_date("2026-07-02")  # no raise

    def test_bad_dates(self):
        for bad in ("2026-7-2", "2026-13-01", "2026-02-30", "nope", "07-02-2026", ""):
            with self.subTest(bad=bad), self.assertRaises(ScaffoldError):
                validate_date(bad)

    def test_make_id(self):
        self.assertEqual(make_id("2026-07-02", "surf"), "2026-07-02_surf")


@unittest.skipUnless(HAVE_YAML, "PyYAML not installed (runs in CI / after pip install)")
class TestScaffoldPost(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        os.makedirs(os.path.join(self.root, "automation", "queue"))
        os.makedirs(os.path.join(self.root, "outputs", "selects"))
        self.addCleanup(self.tmp.cleanup)

    def _src(self, name="pick.jpg", w=1080, h=1350, in_selects=True):
        d = os.path.join(self.root, "outputs", "selects") if in_selects else self.root
        p = os.path.join(d, name)
        write_jpeg(p, w, h)
        return p

    def test_in_range_jpeg_creates_draft(self):
        r = scaffold_post(image=self._src(), slug="surf", date_str="2026-07-02", repo_root=self.root)
        self.assertEqual(r.id, "2026-07-02_surf")
        self.assertEqual(r.image_status, "ok")
        self.assertEqual(r.validation_errors, [])
        self.assertTrue(os.path.isfile(os.path.join(self.root, "automation/assets/2026-07-02_surf/01.jpg")))
        self.assertTrue(os.path.isfile(os.path.join(self.root, "automation/queue/2026-07-02_surf.yml")))

    def test_draft_yml_shape_roundtrips(self):
        scaffold_post(image=self._src(), slug="surf", date_str="2026-07-02", repo_root=self.root)
        from igpub.queue import load_post
        post = load_post(os.path.join(self.root, "automation/queue/2026-07-02_surf.yml"))
        self.assertEqual(post.status.value, "draft")
        self.assertEqual(post.media_type.value, "image")
        self.assertEqual(post.publish_at, "")
        self.assertEqual(post.schedule_mode, "auto")
        self.assertEqual(post.priority, 0)
        self.assertEqual(post.caption, "")
        self.assertEqual(post.hashtags, [])
        self.assertEqual(len(post.assets), 1)
        self.assertEqual(post.assets[0].key, "automation/assets/2026-07-02_surf/01.jpg")
        self.assertEqual(post.assets[0].alt_text, "")

    def test_out_of_range_jpeg_writes_but_warns(self):
        r = scaffold_post(image=self._src(w=1000, h=3000), slug="tall", date_str="2026-07-02", repo_root=self.root)
        self.assertEqual(r.image_status, "out_of_range")
        self.assertTrue(any("aspect" in e for e in r.validation_errors))
        self.assertTrue(os.path.isfile(os.path.join(self.root, "automation/assets/2026-07-02_tall/01.jpg")))

    def test_non_jpeg_is_refused_and_nothing_written(self):
        bad = os.path.join(self.root, "outputs", "selects", "fake.jpg")
        with open(bad, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n not a jpeg")
        with self.assertRaises(ScaffoldError):
            scaffold_post(image=bad, slug="png", date_str="2026-07-02", repo_root=self.root)
        self.assertFalse(os.path.exists(os.path.join(self.root, "automation/assets/2026-07-02_png")))
        self.assertFalse(os.path.exists(os.path.join(self.root, "automation/queue/2026-07-02_png.yml")))

    def test_missing_image(self):
        with self.assertRaises(ScaffoldError):
            scaffold_post(image=os.path.join(self.root, "nope.jpg"), slug="x", date_str="2026-07-02",
                          repo_root=self.root)

    def test_reject_carousel_media_type(self):
        with self.assertRaises(ScaffoldError):
            scaffold_post(image=self._src(), slug="x", date_str="2026-07-02", repo_root=self.root,
                          media_type="carousel")

    def test_refuse_overwrite_existing_yml(self):
        p = os.path.join(self.root, "automation/queue/2026-07-02_surf.yml")
        with open(p, "w") as f:
            f.write("id: existing\n")
        with self.assertRaises(ScaffoldError):
            scaffold_post(image=self._src(), slug="surf", date_str="2026-07-02", repo_root=self.root)

    def test_refuse_overwrite_existing_asset_dir(self):
        os.makedirs(os.path.join(self.root, "automation/assets/2026-07-02_surf"))
        with self.assertRaises(ScaffoldError):
            scaffold_post(image=self._src(), slug="surf", date_str="2026-07-02", repo_root=self.root)

    def test_cleanup_on_midwrite_failure(self):
        # save_post raising mid-write must remove the partial asset dir so a retry isn't blocked.
        with mock.patch("igpub.queue.save_post", side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                scaffold_post(image=self._src(), slug="surf", date_str="2026-07-02", repo_root=self.root)
        self.assertFalse(os.path.exists(os.path.join(self.root, "automation/assets/2026-07-02_surf")))

    def test_remove_select_deletes_source(self):
        src = self._src()
        r = scaffold_post(image=src, slug="surf", date_str="2026-07-02", repo_root=self.root,
                          remove_select=True)
        self.assertTrue(r.source_in_selects)
        self.assertTrue(r.select_removed)
        self.assertFalse(os.path.exists(src))

    def test_default_keeps_select_source(self):
        src = self._src()
        r = scaffold_post(image=src, slug="surf", date_str="2026-07-02", repo_root=self.root)
        self.assertTrue(r.source_in_selects)
        self.assertFalse(r.select_removed)
        self.assertTrue(os.path.exists(src))

    def test_source_outside_selects_not_flagged(self):
        src = self._src(in_selects=False)
        r = scaffold_post(image=src, slug="surf", date_str="2026-07-02", repo_root=self.root,
                          remove_select=True)
        self.assertFalse(r.source_in_selects)
        self.assertFalse(r.select_removed)
        self.assertTrue(os.path.exists(src))


if __name__ == "__main__":
    unittest.main()
