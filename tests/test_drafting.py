import unittest
from app.geometry.measurements import Measurements, LowerMeasurements
from app.geometry.skeleton import BackPattern
from app.geometry.hosen import HosenPattern, HosenPatternParameter


class TestDrafting(unittest.TestCase):
    def setUp(self):
        self.upper_meas = Measurements({
            "OH": 100,
            "OP": 80,
            "DZ": 40,
            "Szad": 42
        })
        self.lower_meas = LowerMeasurements({
            "title": "Test Hosen",
            "VP": 175,
            "OP": 98,
            "OS": 116,
            "BDK": 122,
            "KD": 90,
            "O_st": 61,
            "O_nk": 46,
            "O_l": 40,
            "O_kot": 26
        })

    def test_back_pattern_drafting(self):
        bp = BackPattern(3, 8, self.upper_meas)
        lines = bp.get_skeleton_lines()
        self.assertIn("chest", lines)
        self.assertIn("waist", lines)
        points = bp.get_pattern_points(collar=True)
        self.assertIsInstance(points, list)
        self.assertGreater(len(points), 10)

    def test_collar_generation(self):
        bp = BackPattern(3, 8, self.upper_meas)
        collar = bp.generate_collar(collar_depth=12)
        collar_pts = collar.get_pattern_points()
        self.assertIsInstance(collar_pts, list)
        self.assertGreater(len(collar_pts), 5)

    def test_hosen_pattern_drafting(self):
        param = HosenPatternParameter(5, 12, 2, 15, 0, 0, 0)
        hp = HosenPattern(60, 8, self.lower_meas, param)
        lines = hp.get_skeleton_lines()
        self.assertIn("waist", lines)
        self.assertIn("knee", lines)
        self.assertIn("ankle", lines)
        seam_points = hp.get_pattern_points()
        self.assertIsInstance(seam_points, list)
        self.assertGreater(len(seam_points), 20)


if __name__ == "__main__":
    unittest.main()
