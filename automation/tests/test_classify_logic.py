import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from igpub import classify_logic as L  # noqa: E402


class TestPlanWork(unittest.TestCase):
    def test_untagged_appears_tagged_does_not(self):
        store = {"images": {"h1": {"filenames": ["a.png"], "subject": "cyclist"}}}
        disk = {"h1": ["a.png"], "h2": ["b.png"]}
        todo = L.plan_subject_scene_work(disk, store)
        self.assertEqual([t["hash"] for t in todo], ["h2"])

    def test_color_only_record_still_needs_subject(self):
        store = {"images": {"h1": {"filenames": ["a.png"], "color": {"dominant": "blue"}}}}
        todo = L.plan_subject_scene_work({"h1": ["a.png"]}, store)
        self.assertEqual([t["hash"] for t in todo], ["h1"])  # color present, subject missing


class TestMerge(unittest.TestCase):
    def test_writes_new(self):
        store = L.empty_store()
        store, n = L.merge_subject_scene(store, {"h2": {"subject": "skier", "scene": "desert"}})
        self.assertEqual(n, 1)
        self.assertEqual(store["images"]["h2"]["subject"], "skier")
        self.assertEqual(store["images"]["h2"]["source"], "vision")

    def test_idempotent_does_not_retag(self):
        store = {"images": {"h1": {"subject": "cyclist", "source": "vision"}}}
        store, n = L.merge_subject_scene(store, {"h1": {"subject": "skater"}})
        self.assertEqual(n, 0)
        self.assertEqual(store["images"]["h1"]["subject"], "cyclist")

    def test_human_lock_never_clobbered(self):
        store = {"images": {"h1": {"subject": "kayaker", "source": "human"}}}
        store, n = L.merge_subject_scene(store, {"h1": {"subject": "cyclist"}})
        self.assertEqual(n, 0)
        self.assertEqual(store["images"]["h1"]["subject"], "kayaker")


class TestHelpers(unittest.TestCase):
    def test_index_by_filename(self):
        store = {"images": {"h1": {"filenames": ["a.png", "b.png"], "subject": "x"}}}
        idx = L.index_by_filename(store)
        self.assertEqual(idx["a.png"], idx["b.png"])
        self.assertEqual(idx["a.png"]["subject"], "x")

    def test_reattach_filenames(self):
        store = {"images": {"h1": {"filenames": ["old.png"]}}}
        L.reattach_filenames(store, {"h1": ["new1.png", "new2.png"]})
        self.assertEqual(store["images"]["h1"]["filenames"], ["new1.png", "new2.png"])

    def test_set_color_preserves_subject(self):
        store = {"images": {"h1": {"subject": "cyclist", "source": "vision"}}}
        L.set_color(store, "h1", ["a.png"], {"dominant": "blue", "accent": "green"})
        self.assertEqual(store["images"]["h1"]["subject"], "cyclist")
        self.assertEqual(store["images"]["h1"]["color"]["dominant"], "blue")

    def test_stale_hashes(self):
        store = {"images": {"h1": {}, "h2": {}}}
        self.assertEqual(L.stale_hashes(store, ["h1"]), ["h2"])


if __name__ == "__main__":
    unittest.main()
