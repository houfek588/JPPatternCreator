import unittest
import json
from app.web.server import app


class TestWebServer(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_generate_hosen(self):
        payload = {
            "patternType": "hosen",
            "inputs": {
                "title": "Test Hosen",
                "VP": 175, "OP": 98, "OS": 116,
                "BDK": 122, "KD": 90, "O_st": 61,
                "O_nk": 46, "O_l": 40, "O_kot": 26
            },
            "sliders": {
                "slider1": 5, "slider2": 12, "slider3": 5,
                "slider4": 12, "slider5": 0, "slider6": 0, "slider7": 0
            },
            "part": "all"
        }
        response = self.client.post("/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("<svg", data["svg"])

    def test_generate_bodice(self):
        payload = {
            "patternType": "bodice",
            "inputs": {
                "title": "Test Bodice",
                "OH": 100, "OP": 80, "DZ": 40, "Szad": 42
            },
            "sliders": {
                "slider1": 12
            },
            "part": "all"
        }
        response = self.client.post("/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("<svg", data["svg"])

    def test_export_pdf(self):
        payload = {
            "patternType": "hosen",
            "inputs": {
                "title": "Export Test",
                "VP": 175, "OP": 98, "OS": 116,
                "BDK": 122, "KD": 90, "O_st": 61,
                "O_nk": 46, "O_l": 40, "O_kot": 26
            },
            "sliders": {
                "slider1": 5, "slider2": 12, "slider3": 5,
                "slider4": 12, "slider5": 0, "slider6": 0, "slider7": 0
            },
            "part": "all"
        }
        response = self.client.post("/export/pdf", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/pdf")
        self.assertGreater(len(response.data), 100)


if __name__ == "__main__":
    unittest.main()
