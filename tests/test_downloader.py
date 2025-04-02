import unittest
from core.downloader import DownloadTask

class TestDownloader(unittest.TestCase):
    def test_task_creation(self):
        task = DownloadTask("https://yt.com", "720p", "/tmp", "", audio_only=True)
        self.assertEqual(task.url, "https://yt.com")
        self.assertTrue(task.audio_only)

if __name__ == "__main__":
    unittest.main()
