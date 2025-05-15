import pytest
from PySide6.QtWidgets import QApplication
import sys
import os
import shutil
import tempfile
from core.utils import get_data_dir

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app

@pytest.fixture
def temp_data_dir(monkeypatch):
    temp_dir = tempfile.mkdtemp()
    monkeypatch.setattr('core.utils.get_data_dir', lambda: temp_dir)
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_ffmpeg(monkeypatch):
    def mock_which(*args, **kwargs):
        return "/mock/ffmpeg"
    monkeypatch.setattr('shutil.which', mock_which)

@pytest.fixture
def clean_profile(temp_data_dir):
    from core.profile import UserProfile
    profile = UserProfile()
    profile.set_profile("Test User", "", os.path.join(temp_data_dir, "downloads"))
    return profile 