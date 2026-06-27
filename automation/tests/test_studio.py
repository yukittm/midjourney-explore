import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from PIL import Image  # noqa: F401
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False
try:
    import yaml  # noqa: F401
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False

from igpub.models import MediaType, Post, Result, Status, image_asset  # noqa: E402
from igpub.studio_logic import (  # noqa: E402
    assemble_board, classify, reconcile_order, safe_path, slugify,
)

MJ = ("Yuki_a_surfer_carving_a968cb9b-175e-40fb-924c-a405a390d301_2.png")


class TestSafePath(unittest.TestCase):
    def test_unknown_root(self):
        self.assertIsNone(safe_path("/repo", "secrets", "x"))

    def test_traversal_rejected(self):
        self.assertIsNone(safe_path("/repo", "candidates", "../../etc/passwd"))

    def test_valid(self):
        p = safe_path("/repo", "candidates", "a.png")
        self.assertTrue(p.endswith("/repo/outputs/candidates/a.png") or
                        p.endswith("\\repo\\outputs\\candidates\\a.png"))


class TestSlugify(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("A Surfer, Carving!"), "a-surfer-carving")

    def test_empty_fallbacks(self):
        self.assertEqual(slugify("!!!"), "post")


class TestClassify(unittest.TestCase):
    def test_flat(self):
        g = classify([MJ, "b.png", "notes.txt"], "flat")
        self.assertEqual(g, [("All images", [MJ, "b.png"])])  # case-sensitive sort: 'Y' < 'b'

    def test_subject(self):
        g = classify([MJ], "subject")
        self.assertEqual(g[0][0], "Yuki a surfer carving")

    def test_aspect_buckets(self):
        dims = {"p.png": (1080, 1350), "s.png": (1000, 1000), "l.png": (1910, 1000)}
        g = dict(classify(["p.png", "s.png", "l.png"], "aspect", dims=dims))
        self.assertEqual(g["portrait"], ["p.png"])
        self.assertEqual(g["square"], ["s.png"])
        self.assertEqual(g["landscape"], ["l.png"])

    def test_aspect_unknown_when_no_dims(self):
        g = dict(classify(["x.png"], "aspect", dims={}))
        self.assertEqual(g["unknown"], ["x.png"])


class TestAssembleBoard(unittest.TestCase):
    def _posts(self):
        live = Post(id="2026-06-27_villa", status=Status.PUBLISHED, media_type=MediaType.IMAGE,
                    assets=[image_asset("automation/assets/2026-06-27_villa/01.jpg")],
                    result=Result(published_at="2026-06-27T10:00:00+00:00"))
        appr = Post(id="2026-07-02_wave", status=Status.APPROVED, media_type=MediaType.IMAGE,
                    assets=[image_asset("automation/assets/2026-07-02_wave/01.jpg")])
        return [live, appr]

    def test_shape_and_urls(self):
        b = assemble_board([MJ], ["a-surfer.jpg"], self._posts(), axis="subject",
                           selects_order=["a-surfer.jpg"])
        self.assertEqual(b["axis"], "subject")
        self.assertEqual(b["counts"], {"pool": 1, "selects": 1, "live": 1})
        self.assertIn("/img?root=candidates&name=", b["pool"][0]["items"][0]["url"])
        # grid: draggable select tile on top, then approved (upcoming) post, then published (live)
        self.assertEqual([t["key"] for t in b["grid"]],
                         ["a-surfer.jpg", "2026-07-02_wave", "2026-06-27_villa"])
        sel = b["grid"][0]
        self.assertEqual((sel["kind"], sel["draggable"], sel["slug"]), ("select", True, "a-surfer"))
        self.assertIn("/img?root=selects&name=", sel["url"])
        self.assertFalse(b["grid"][2]["draggable"])  # live post locked
        self.assertIn("/img?root=assets&name=2026-06-27_villa/01.jpg", b["grid"][2]["url"])

    def test_bad_axis_falls_back(self):
        b = assemble_board([], [], [], axis="nonsense")
        self.assertEqual(b["axis"], "subject")


class TestPoolInSelects(unittest.TestCase):
    def test_marks_already_staged(self):
        # a candidate whose slug matches a select (incl. the -N dup suffix) is flagged in_selects
        b = assemble_board(["wave-one.png", "fresh.png"], ["wave-one.jpg", "other-2.jpg"], [])
        items = {it["name"]: it["in_selects"] for grp in b["pool"] for it in grp["items"]}
        self.assertTrue(items["wave-one.png"])
        self.assertFalse(items["fresh.png"])


class TestReconcileOrder(unittest.TestCase):
    def test_keeps_drops_newest_first(self):
        # keep b (still present), drop gone, put new a at the FRONT (newest → top-left)
        self.assertEqual(reconcile_order(["b.jpg", "gone.jpg"], ["a.jpg", "b.jpg"]), ["a.jpg", "b.jpg"])

    def test_empty_saved(self):
        self.assertEqual(reconcile_order([], ["b.jpg", "a.jpg"]), ["a.jpg", "b.jpg"])


@unittest.skipUnless(HAVE_PIL, "Pillow needed for studio server tests")
class TestStudioServer(unittest.TestCase):
    def setUp(self):
        import studio
        self.studio = studio
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = self.tmp.name
        for d in ("outputs/candidates", "outputs/selects", "automation/queue", "automation/assets"):
            os.makedirs(os.path.join(self.root, d))
        self._orig = studio.REPO_ROOT
        studio.REPO_ROOT = self.root
        self.addCleanup(lambda: setattr(studio, "REPO_ROOT", self._orig))

    def _cand(self, name, w=1080, h=1350):
        Image.new("RGB", (w, h), (20, 150, 90)).save(os.path.join(self.root, "outputs/candidates", name))

    def test_to_selects_converts_jpg_and_prepends(self):
        self._cand("scene.png")
        r = self.studio._to_selects("scene.png")
        self.assertTrue(r["select"].endswith(".jpg"))
        self.assertTrue(os.path.isfile(os.path.join(self.root, "outputs/selects", r["select"])))
        self.assertEqual(self.studio._load_order()[0], r["select"])
        r2 = self.studio._to_selects("scene.png")           # dup → -2, newest at front
        self.assertNotEqual(r2["select"], r["select"])
        self.assertEqual(self.studio._load_order()[0], r2["select"])

    def test_to_selects_missing(self):
        with self.assertRaises(ValueError):
            self.studio._to_selects("nope.png")

    def test_from_selects_removes_and_drops_order(self):
        self._cand("a.png")
        sel = self.studio._to_selects("a.png")["select"]
        self.studio._from_selects(sel)
        self.assertFalse(os.path.exists(os.path.join(self.root, "outputs/selects", sel)))
        self.assertNotIn(sel, self.studio._load_order())
        with self.assertRaises(ValueError):
            self.studio._from_selects("ghost.jpg")

    def test_reorder_keeps_only_present(self):
        self._cand("a.png")
        sel = self.studio._to_selects("a.png")["select"]
        self.studio._reorder([sel, "ghost.jpg"])
        self.assertEqual(self.studio._load_order(), [sel])

    def test_load_order_garbage_resets(self):
        with open(os.path.join(self.root, "outputs/selects", ".order.json"), "w") as f:
            f.write("{not json")
        self.assertEqual(self.studio._load_order(), [])

    @unittest.skipUnless(HAVE_YAML, "PyYAML needed for commit (scaffold writes yml)")
    def test_commit_carries_priority_and_removes_select(self):
        self._cand("wave.png")
        self._cand("surf.png")
        self.studio._to_selects("wave.png")
        self.studio._to_selects("surf.png")
        order = self.studio._load_order()        # [surf.jpg, wave.jpg] — newest first
        top = order[0]
        r = self.studio._commit(top, "")
        self.assertEqual(r["priority"], 2)        # len 2 - idx 0 → highest
        self.assertFalse(os.path.exists(os.path.join(self.root, "outputs/selects", top)))
        self.assertNotIn(top, self.studio._load_order())
        from igpub.queue import load_post
        post_obj = load_post(os.path.join(self.root, "automation/queue", r["id"] + ".yml"))
        self.assertEqual(post_obj.priority, 2)
        self.assertEqual(post_obj.status.value, "draft")


if __name__ == "__main__":
    unittest.main()
