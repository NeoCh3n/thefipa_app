import unittest
import json
import requests

class TestFlaskApp(unittest.TestCase):
    base_url = "https://thefipa1.azurewebsites.net"

    def test_home(self):
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello, Flask!")

    def test_predict(self):
        test_data = {
            "input": ["0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2"]
        }
        response = requests.post(f"{self.base_url}/predict", json=test_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("prediction", data)

    def test_test_db(self):
        response = requests.get(f"{self.base_url}/test_db")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Database connection successful")

    def test_test_model(self):
        test_data = {
            "input": ["0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2"]
        }
        response = requests.post(f"{self.base_url}/test_model", json=test_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Model prediction successful")

if __name__ == "__main__":
    unittest.main()