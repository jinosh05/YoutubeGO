import unittest
from core.utils import format_speed, format_time

class TestUtils(unittest.TestCase):
    def test_format_speed(self):
        self.assertEqual(format_speed(1500), "1.50 KB/s")
        self.assertEqual(format_speed(1500000), "1.50 MB/s")

    def test_format_time(self):
        self.assertEqual(format_time(90), "1m 30s")
        self.assertEqual(format_time(3600), "1h 0m 0s")

if __name__ == "__main__":
    unittest.main()
