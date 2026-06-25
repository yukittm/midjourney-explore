import os
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from igpub.imaging import aspect_ok, read_jpeg_size  # noqa: E402
from igpub.models import MediaType, Post, Status  # noqa: E402
from igpub.validate import validate_meta, validate_post  # noqa: E402


def make_post(**kw) -> Post:
    base = dict(
        id="t", status=Status.APPROVED, media_type=MediaType.IMAGE,
        publish_at="2026-07-02T19:00:00+09:00", images=["a.jpg"],
    )
    base.update(kw)
    return Post(**base)


def minimal_jpeg(width: int, height: int) -> bytes:
    # SOI + SOF0(len=17, precision=8, height, width, 3 components...) + EOI
    return (b"\xff\xd8\xff\xc0\x00\x11\x08" + struct.pack(">HH", height, width)
            + b"\x03\x01\x22\x00\x02\x11\x01\x03\x11\x01\xff\xd9")


class TestAspect(unittest.TestCase):
    def test_portrait_4x5_ok(self): self.assertTrue(aspect_ok(1080, 1350))
    def test_square_ok(self): self.assertTrue(aspect_ok(1080, 1080))
    def test_landscape_191_ok(self): self.assertTrue(aspect_ok(1910, 1000))
    def test_too_tall_fails(self): self.assertFalse(aspect_ok(1000, 2000))
    def test_too_wide_fails(self): self.assertFalse(aspect_ok(3000, 1000))
    def test_zero_fails(self): self.assertFalse(aspect_ok(0, 100))


class TestJpegSize(unittest.TestCase):
    def test_reads_dims(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.jpg")
            with open(p, "wb") as f:
                f.write(minimal_jpeg(320, 240))
            self.assertEqual(read_jpeg_size(p), (320, 240))

    def test_non_jpeg_raises(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.jpg")
            with open(p, "wb") as f:
                f.write(b"not a jpeg")
            with self.assertRaises(ValueError):
                read_jpeg_size(p)


class TestMeta(unittest.TestCase):
    def test_clean_meta_passes(self):
        self.assertEqual(validate_meta(make_post(hashtags=["abstractart", "colorart"])), [])

    def test_caption_too_long(self):
        errs = validate_meta(make_post(caption="x" * 2300))
        self.assertTrue(any("chars >" in e for e in errs))

    def test_too_many_hashtags(self):
        errs = validate_meta(make_post(hashtags=[f"t{i}" for i in range(31)]))
        self.assertTrue(any("hashtags >" in e for e in errs))

    def test_hashtag_with_hash_rejected(self):
        errs = validate_meta(make_post(hashtags=["#abstractart"]))
        self.assertTrue(any("leading '#'" in e for e in errs))

    def test_image_count_for_single(self):
        errs = validate_meta(make_post(images=["a.jpg", "b.jpg"]))
        self.assertTrue(any("exactly 1 image" in e for e in errs))

    def test_carousel_count(self):
        errs = validate_meta(make_post(media_type=MediaType.CAROUSEL, images=["a.jpg"]))
        self.assertTrue(any("carousel needs" in e for e in errs))


class TestImages(unittest.TestCase):
    def test_good_image_passes(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "a.jpg"), "wb") as f:
                f.write(minimal_jpeg(1080, 1350))
            self.assertEqual(validate_post(make_post(), repo_root=d), [])

    def test_missing_image(self):
        with tempfile.TemporaryDirectory() as d:
            errs = validate_post(make_post(), repo_root=d)
            self.assertTrue(any("image not found" in e for e in errs))

    def test_bad_aspect(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "a.jpg"), "wb") as f:
                f.write(minimal_jpeg(1000, 3000))
            errs = validate_post(make_post(), repo_root=d)
            self.assertTrue(any("aspect ratio" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
