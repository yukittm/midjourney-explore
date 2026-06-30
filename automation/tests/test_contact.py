import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from igpub.contact import build_candidates, group, render_html, subject_of  # noqa: E402

MJ = ("Yuki_a_surfer_carving_large_in_the_frame_down_a_steep_flowing_"
      "a968cb9b-175e-40fb-924c-a405a390d301_2.png")


class TestSubjectGrouping(unittest.TestCase):
    def test_strips_uuid_tail(self):
        # subject is normalized: UUID tail stripped, leading "Yuki " dropped, lowercased
        self.assertEqual(subject_of(MJ),
                         "a surfer carving large in the frame down a steep flowing")

    def test_strips_mj_params_and_junk_prefix(self):
        # `--chaos 10 --ar 45 …` flags and an httpss.mj.run<id> URL prefix are dropped so trivial
        # prefix differences collapse into one readable group key.
        self.assertEqual(
            subject_of("Yuki_geometric_scene_--chaos_10_--ar_45_--profile_g2sx9a7_"
                       "--styliz_0a248e6d-6f8c-4cef-ade2-a40837ab0985_3.png"),
            "geometric scene")
        self.assertEqual(
            subject_of("geometric_scene_--chaos_10_--ar_45_"
                       "6e58d03b-1bb9-4c09-8f11-ccef281ca016_2.png"),
            "geometric scene")

    def test_same_subject_groups_together(self):
        a = MJ
        b = ("Yuki_a_surfer_carving_large_in_the_frame_down_a_steep_flowing_"
             "11111111-2222-3333-4444-555555555555_0.png")
        cands = build_candidates([a, b])
        groups = group(cands)
        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0][1]), 2)

    def test_fallback_for_non_mj_name(self):
        self.assertEqual(subject_of("random_thing.png"), "random thing")

    def test_only_image_files(self):
        cands = build_candidates([MJ, "notes.txt", "contact-sheet.html", "x.PNG"])
        self.assertEqual({c.filename for c in cands}, {MJ, "x.PNG"})

    def test_biggest_group_first(self):
        big = [f"big_set_aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee_{i}.png" for i in range(3)]
        small = ["lone_set_aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee_0.png"]
        groups = group(build_candidates(small + big))
        self.assertEqual(groups[0][0], "big set")  # 3 before 1


class TestRender(unittest.TestCase):
    def test_renders_tiles_with_prefix_and_escapes(self):
        cands = build_candidates([MJ])
        out = render_html(group(cands), total=1, img_prefix="candidates/")
        self.assertIn(f"candidates/{MJ}", out)
        self.assertIn("a surfer carving", out)

    def test_empty(self):
        out = render_html([], total=0)
        self.assertIn("No candidate images found", out)

    def test_escapes_subject(self):
        # a crafted name with HTML chars in the subject must be escaped
        name = "a<b>&c_aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee_0.png"
        out = render_html(group(build_candidates([name])), total=1)
        self.assertIn("a&lt;b&gt;&amp;c", out)
        self.assertNotIn("<b>&c", out)


if __name__ == "__main__":
    unittest.main()
