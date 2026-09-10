import unittest
from app.geometry.measurements import Measurements, LowerMeasurements, ValidationError


class TestMeasurements(unittest.TestCase):
    def test_valid_measurements(self):
        data = {"OH": 100, "OP": 80, "DZ": 40, "Szad": 42}
        m = Measurements(data)
        self.assertEqual(m.meas["OH"], 100.0)

    def test_missing_measurement_raises(self):
        data = {"OH": 100, "OP": 80}
        with self.assertRaises(ValidationError):
            Measurements(data)

    def test_non_positive_measurement_raises(self):
        data = {"OH": -10, "OP": 80, "DZ": 40, "Szad": 42}
        with self.assertRaises(ValidationError):
            Measurements(data)

    def test_unit_conversion(self):
        data = {"OH": 100, "OP": 80, "DZ": 40, "Szad": 42}
        m = Measurements(data)
        cm_scaled = m.get_all_measurements(scale=1, unit="cm")
        mm_scaled = m.get_all_measurements(scale=1, unit="mm")
        self.assertEqual(cm_scaled["OH"], 100.0)
        self.assertEqual(mm_scaled["OH"], 1000.0)


class TestLowerMeasurements(unittest.TestCase):
    def test_valid_lower_measurements(self):
        data = {
            "title": "Test Hosen",
            "VP": 175, "OP": 98, "OS": 116,
            "BDK": 122, "KD": 90, "O_st": 61,
            "O_nk": 46, "O_l": 40, "O_kot": 26
        }
        lm = LowerMeasurements(data)
        self.assertEqual(lm.meas["VP"], 175.0)

    def test_missing_lower_measurement_raises(self):
        data = {
            "title": "Incomplete",
            "VP": 175, "OP": 98
        }
        with self.assertRaises(ValidationError):
            LowerMeasurements(data)


if __name__ == "__main__":
    unittest.main()
