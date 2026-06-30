import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from igpub.color import FAMILIES, classify_palette, color_distance, family_of  # noqa: E402


class TestFamilyOf(unittest.TestCase):
    def test_primaries(self):
        self.assertEqual(family_of((255, 0, 0)), "red-orange")
        self.assertEqual(family_of((0, 200, 0)), "green")
        self.assertEqual(family_of((0, 0, 255)), "blue")

    def test_teal_and_violet(self):
        self.assertEqual(family_of((0, 128, 128)), "teal")
        self.assertEqual(family_of((140, 0, 200)), "violet")

    def test_low_saturation_and_dark_are_neutral(self):
        self.assertEqual(family_of((128, 128, 128)), "neutral")   # grey
        self.assertEqual(family_of((10, 10, 12)), "neutral")      # near-black
        self.assertEqual(family_of((240, 238, 235)), "neutral")   # near-white


class TestClassifyPalette(unittest.TestCase):
    def test_dominant_accent_and_vector_sum(self):
        counts = [(70, (255, 30, 0)), (25, (0, 0, 230)), (5, (130, 130, 130))]
        r = classify_palette(counts)
        self.assertEqual(r["dominant"], "red-orange")
        self.assertEqual(r["accent"], "blue")
        self.assertAlmostEqual(sum(r["vector"].values()), 1.0, places=2)
        self.assertEqual(set(r["vector"]), set(FAMILIES))

    def test_single_family_accent_falls_back(self):
        r = classify_palette([(100, (0, 200, 0))])
        self.assertEqual(r["dominant"], "green")
        self.assertEqual(r["accent"], "green")  # nothing else -> falls back

    def test_empty(self):
        r = classify_palette([])
        self.assertEqual(r["dominant"], "neutral")

    def test_all_neutral(self):
        r = classify_palette([(50, (120, 120, 120)), (50, (20, 20, 20))])
        self.assertEqual(r["dominant"], "neutral")


class TestColorDistance(unittest.TestCase):
    def test_identical_is_zero(self):
        v = {f: (1.0 if f == "blue" else 0.0) for f in FAMILIES}
        self.assertEqual(color_distance(v, v), 0.0)

    def test_disjoint_is_two(self):
        a = {f: (1.0 if f == "blue" else 0.0) for f in FAMILIES}
        b = {f: (1.0 if f == "red-orange" else 0.0) for f in FAMILIES}
        self.assertAlmostEqual(color_distance(a, b), 2.0, places=6)


if __name__ == "__main__":
    unittest.main()
