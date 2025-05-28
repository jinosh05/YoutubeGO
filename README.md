# 🎶 YoutubeGO 5.0 🎥

<div align="center">
  <img src="assets/banner.png" alt="YoutubeGO Logo" width="650"/>
  
  ### Modern YouTube Downloader with Advanced Features
  
  [![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![PySide6](https://img.shields.io/badge/UI-PySide6-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PySide6/)
  [![yt-dlp](https://img.shields.io/badge/Downloader-yt--dlp-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
  [![requests](https://img.shields.io/badge/HTTP-requests-2496ED?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/requests/)
  [![FFmpeg](https://img.shields.io/badge/External-FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
</div>

## 📋 Table of Contents
- [Features](#-key-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [ScreenShots](showcase/showcase.md)
- [Contributing](#-contributions)
- [License](#-legal)
- [Project Structure](#-project-structure)

## 🛠️ Tech Stack

### 📊 Project Stats
[![Code size](https://img.shields.io/github/languages/code-size/Efeckc17/YoutubeGO?style=for-the-badge&color=blueviolet)](https://github.com/Efeckc17/YoutubeGO)
[![Last commit](https://img.shields.io/github/last-commit/Efeckc17/YoutubeGO?style=for-the-badge&color=blue)](https://github.com/Efeckc17/YoutubeGO/commits)
[![Stars](https://img.shields.io/github/stars/Efeckc17/YoutubeGO?style=for-the-badge&color=yellow)](https://github.com/Efeckc17/YoutubeGO/stargazers)
[![Forks](https://img.shields.io/github/forks/Efeckc17/YoutubeGO?style=for-the-badge&color=orange)](https://github.com/Efeckc17/YoutubeGO/network/members)
[![GitHub release (latest by tag)](https://img.shields.io/github/v/tag/Efeckc17/YoutubeGO?style=for-the-badge&color=green&label=latest)](https://github.com/Efeckc17/YoutubeGO/releases)

### 📜 Legal 
[![License](https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge&logo=gnu&logoColor=white)](LICENSE)

### 📜 Qt/PySide6 License

Please see [QtLicense.md](QtLicense.md) for full LGPL-3.0 compliance information regarding PySide6 (Qt).

### 🌐 Links
[![Website](https://img.shields.io/badge/Visit-Website-1DA1F2?style=for-the-badge&logo=web&logoColor=white)](https://youtubego.org)
[![Discord](https://img.shields.io/badge/Join-Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/SyMTVFYcbb)

## 🌐 Languages

 | 🇷🇺 [Русский](README.ru.md)

## 🌟 Key Features

### 🎯 Core Features
- **Multi-Platform Support**  
  Download videos and audio from platforms supporting HTTP streams, including YouTube, Vimeo, and more.

- **Playlist Downloads**  
  Save entire playlists with sequential processing in just a few clicks.

- **Multiple Formats**  
  Download in **MP4** (video) and multiple audio formats (**MP3**, **M4A**, **WAV**, **AAC**, **FLAC**, **OPUS**, **VORBIS**).

- **High-Resolution Support**  
  Supports downloads up to **8K, 4K, 2K, 1080p, 720p, 360p**. Select your preferred resolution in Settings.

- **Modular Codebase**  
  Code has been fully refactored into `core/`, `ui/`, and `tests/` directories for easier maintenance and contribution.

### 🛠️ Advanced Features
- **Batch Processing**  
  Queue multiple downloads and manage them simultaneously. Pause, resume, or cancel downloads easily.

- **Audio Extraction**  
  Extract audio tracks in multiple formats including **MP3**, **M4A**, **WAV**, **AAC**, **FLAC**, **OPUS**, and **VORBIS**.

- **Profile Management**  
  Save your name, profile picture, download paths, and social media links. Profiles can be updated directly in the app.

- **Profile Import/Export**  
  Easily export your profile, settings, history, and profile picture as a single ZIP file, and import them back into the app on any device. Great for backup, migration, or restoring your preferences.

- **Drag & Drop Interface**  
  Add download URLs by dragging them into the app.

- **System Tray Integration**  
  Application runs in the system tray when minimized with quick access menu to restore or quit the app.

- **Enhanced Download System**  
  Improved stability and efficiency with better support for large file downloads and multiple simultaneous downloads.

- **Queue System Optimization**  
  Concurrency management with pause & resume all functionality and bandwidth limiting support via proxy settings.

### 🎨 User Experience
- **Dark & Light Mode**  
  Switch between Dark and Light themes for better usability.

- **Error Handling**  
  Displays detailed error logs to debug issues.

- **Scheduler**  
  Schedule downloads to start at a specific date and time.

- **Download History**  
  View, search, and manage previous downloads directly in the app.

- **Improved Notification System**  
  Download Complete notifications, Download Failed alerts, and Download Canceled warnings.

- **Enhanced UI**  
  Better UI animations and responsiveness with color-coded log messages and search & filter options in history and queue.

### 🔧 Technical Features
- **FFmpeg Detection**  
  Automatically detects FFmpeg installation and prompts for setup if missing.

- **Cross-Platform Compatibility**  
  Fully supported on **Linux** and **Windows**.

## ⚙️ Installation

### Prerequisites
- Python 3.7 or higher
- FFmpeg (for audio/video processing)
- Git (for cloning the repository)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/Efeckc17/YoutubeGO.git
cd YoutubeGO

# Ensure Python 3.7+ is installed
python --version

# Install dependencies
pip install -r requirements.txt

# Install FFmpeg for audio and video processing

# Linux
sudo apt install ffmpeg

# Windows (via winget)
winget install FFmpeg
```

## 🔧 Usage

### Basic Usage
```bash
# Launch the app
python main.py
```

### Key Features Usage
- Configure your profile in the **Settings** or **Profile** page
- Use the MP4 or MP3 pages to download videos or extract audio
- Add multiple downloads to the queue and manage them from the Queue page
- Schedule downloads in advance using the Scheduler

### Tips & Tricks
- Use drag & drop for quick URL addition
- Enable system tray for background operation
- Use the scheduler for off-peak downloads
- Export your profile for easy migration

## ⚠️ Notes

### Requirements
```bash
# FFmpeg Required
# Some features, like audio extraction and video merging, depend on FFmpeg.
# Ensure it's installed and available in your system PATH.

# Third-Party Libraries
# The app uses yt_dlp for downloading and metadata extraction.
# Refer to their GitHub page for details.
https://github.com/yt-dlp/yt-dlp
```

## 🙏 Contributions

### How to Contribute
```bash
# We welcome contributions to improve YoutubeGO 5.0.
# Please submit issues or pull requests via GitHub.

# Enjoy using YoutubeGO 5.0!
🚀
```

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## ⚠️ Legal Notice

YoutubeGO is an independent open-source project. It operates independently from YouTube and Google, performing downloads and other operations without using their APIs. This project is not bound by YouTube's terms of service or rules.

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/Efeckc17">Efeckc17</a></sub>
</div>
