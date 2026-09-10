import unittest
import math
from app.geometry.base import Line, Bezier, CatmullRomSpline


class TestLine(unittest.TestCase):
    def test_horizontal_line(self):
        line = Line((0, 5), (10, 5))
        self.assertTrue(line.is_horizontal())
        self.assertFalse(line.is_vertical())
        self.assertEqual(line.line_length(), 10.0)
        self.assertEqual(line.get_y_point(3), 5.0)

    def test_vertical_line(self):
        line = Line((5, 0), (5, 20))
        self.assertTrue(line.is_vertical())
        self.assertFalse(line.is_horizontal())
        self.assertEqual(line.line_length(), 20.0)
        self.assertEqual(line.get_x_point(10), 5.0)

    def test_line_intersection(self):
        line1 = Line((0, 0), (10, 10))
        line2 = Line((0, 10), (10, 0))
        ix, iy = line1.intersection(line2)
        self.assertAlmostEqual(ix, 5.0)
        self.assertAlmostEqual(iy, 5.0)

    def test_parallel_lines_no_intersection(self):
        line1 = Line((0, 0), (10, 0))
        line2 = Line((0, 5), (10, 5))
        with self.assertRaises(ValueError):
            line1.intersection(line2)

    def test_point_distance(self):
        line = Line((0, 0), (10, 0))
        p = line.get_point_distance(5)
        self.assertAlmostEqual(p[0], 5.0)
        self.assertAlmostEqual(p[1], 0.0)


class TestBezier(unittest.TestCase):
    def test_linear_bezier(self):
        curve = Bezier([(0, 0), (10, 10)])
        self.assertEqual(curve.degree, 1)
        p_mid = curve.get_point(0.5)
        self.assertAlmostEqual(p_mid[0], 5.0)
        self.assertAlmostEqual(p_mid[1], 5.0)

    def test_cubic_bezier_sampling(self):
        curve = Bezier([(0, 0), (0, 10), (10, 10), (10, 0)])
        self.assertEqual(curve.degree, 3)
        samples = curve.sample(resolution=20)
        self.assertEqual(len(samples), 20)
        self.assertAlmostEqual(samples[0][0], 0.0)
        self.assertAlmostEqual(samples[0][1], 0.0)
        self.assertAlmostEqual(samples[-1][0], 10.0)
        self.assertAlmostEqual(samples[-1][1], 0.0)

    def test_bezier_length(self):
        curve = Bezier([(0, 0), (10, 0)])
        self.assertAlmostEqual(curve.get_length(), 10.0, places=2)


class TestCatmullRomSpline(unittest.TestCase):
    def test_spline_sampling(self):
        points = [(0, 0), (5, 10), (10, 0), (15, -10)]
        spline = CatmullRomSpline(points)
        sampled = spline.sample(resolution=50)
        self.assertEqual(len(sampled), 50)
        self.assertAlmostEqual(sampled[0][0], 0.0, places=1)
        self.assertAlmostEqual(sampled[0][1], 0.0, places=1)


if __name__ == "__main__":
    unittest.main()
