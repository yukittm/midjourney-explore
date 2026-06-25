import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from igpub.models import MediaType, Post, Status, image_asset  # noqa: E402


class TestBackCompat(unittest.TestCase):
    def test_legacy_images_synthesize_assets(self):
        d = {"id": "x", "status": "approved", "media_type": "image",
             "publish_at": "2026-07-02T19:00:00+09:00",
             "images": ["automation/assets/x/01.jpg"], "alt_text": "wave",
             "provenance": {"sref": "S1"}}
        p = Post.from_dict(d)
        self.assertEqual(len(p.assets), 1)
        self.assertEqual(p.assets[0].kind, "image")
        self.assertEqual(p.assets[0].key, "automation/assets/x/01.jpg")
        self.assertEqual(p.assets[0].alt_text, "wave")
        self.assertEqual(p.assets[0].provenance, {"sref": "S1"})

    def test_legacy_approved_with_publish_at_migrates_to_scheduled(self):
        d = {"id": "x", "status": "approved", "media_type": "image",
             "publish_at": "2026-07-02T19:00:00+09:00", "images": ["a.jpg"]}
        self.assertEqual(Post.from_dict(d).status, Status.SCHEDULED)

    def test_legacy_approved_without_publish_at_stays_approved(self):
        d = {"id": "x", "status": "approved", "media_type": "image", "images": ["a.jpg"]}
        self.assertEqual(Post.from_dict(d).status, Status.APPROVED)

    def test_new_schema_approved_not_migrated(self):
        d = {"id": "x", "schema_version": 1, "status": "approved", "media_type": "image",
             "publish_at": "2026-07-02T19:00:00+09:00",
             "assets": [{"kind": "image", "key": "a.jpg"}]}
        self.assertEqual(Post.from_dict(d).status, Status.APPROVED)


class TestRoundTrip(unittest.TestCase):
    def test_roundtrip_preserves_assets_and_version(self):
        p = Post(id="x", status=Status.SCHEDULED, media_type=MediaType.IMAGE,
                 publish_at="2026-07-02T19:00:00+09:00",
                 assets=[image_asset("a.jpg", alt_text="alt", provenance={"sref": "S"})])
        p2 = Post.from_dict(p.to_dict())
        self.assertEqual(p2.assets[0].key, "a.jpg")
        self.assertEqual(p2.assets[0].alt_text, "alt")
        self.assertEqual(p2.assets[0].provenance, {"sref": "S"})
        self.assertEqual(p2.schema_version, 1)

    def test_images_property_orders_image_keys(self):
        from igpub.models import Asset
        p = Post(id="x", status=Status.DRAFT, media_type=MediaType.CAROUSEL, publish_at="",
                 assets=[image_asset("a.jpg"), Asset(kind="video", key="v/clip.mp4"),
                         image_asset("b.jpg")])
        self.assertEqual(p.images, ["a.jpg", "b.jpg"])
        self.assertEqual(p.videos, ["v/clip.mp4"])


if __name__ == "__main__":
    unittest.main()
