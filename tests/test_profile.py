import unittest
from core.profile import UserProfile
import os

class TestUserProfile(unittest.TestCase):
    def setUp(self):
        self.test_profile_path = "test_user_profile.json"
        self.profile = UserProfile(profile_path=self.test_profile_path)

    def test_set_get_profile(self):
        self.profile.set_profile("Tester", "", "/tmp")
        self.assertEqual(self.profile.data["name"], "Tester")
        self.assertEqual(self.profile.get_download_path(), "/tmp")

    def tearDown(self):
        if os.path.exists(self.test_profile_path):
            os.remove(self.test_profile_path)

if __name__ == "__main__":
    unittest.main()
