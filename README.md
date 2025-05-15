# 🎶 YoutubeGO 4.4 🎥

## 🛠️ Tech Stack

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/UI-PySide6-brightgreen)](https://pypi.org/project/PySide6/)
[![yt-dlp](https://img.shields.io/badge/Downloader-yt--dlp-yellow)](https://github.com/yt-dlp/yt-dlp)
[![requests](https://img.shields.io/badge/HTTP-requests-orange)](https://pypi.org/project/requests/)
[![FFmpeg](https://img.shields.io/badge/External-FFmpeg-red)](https://ffmpeg.org/)


### 📊 Project Stats
[![Code size](https://img.shields.io/github/languages/code-size/Efeckc17/YoutubeGO)](https://github.com/Efeckc17/YoutubeGO)
[![Last commit](https://img.shields.io/github/last-commit/Efeckc17/YoutubeGO)](https://github.com/Efeckc17/YoutubeGO/commits)
[![Stars](https://img.shields.io/github/stars/Efeckc17/YoutubeGO?style=social)](https://github.com/Efeckc17/YoutubeGO/stargazers)
[![Forks](https://img.shields.io/github/forks/Efeckc17/YoutubeGO?style=social)](https://github.com/Efeckc17/YoutubeGO/network/members)
[![GitHub release (latest by tag)](https://img.shields.io/github/v/tag/Efeckc17/YoutubeGO?label=latest)](https://github.com/Efeckc17/YoutubeGO/releases)


### 📜 Legal 
[![License](https://img.shields.io/badge/License-Apache_2.0-green)](LICENSE)

### 🌐 Links
[![Website](https://img.shields.io/badge/Visit-Website-blue)](https://youtubego.org)
[![Discord](https://img.shields.io/badge/Join-Discord-7289DA)](https://discord.gg/XdK97UH3fE)

## 🌐 Languages

 | 🇷🇺 [Русский](README.ru.md)

## 🌟 Key Features

### 🎯 Core Features
- **Multi-Platform Support**  
  Download videos and audio from platforms supporting HTTP streams, including YouTube, Vimeo, and more.

- **Playlist Downloads**  
  Save entire playlists with sequential processing in just a few clicks.

- **Multiple Formats**  
  Download in **MP4** (video) and **MP3** (audio) formats with automatic conversion and merging.

- **High-Resolution Support**  
  Supports downloads up to **8K, 4K, 2K, 1080p, 720p, 360p**. Select your preferred resolution in Settings.

### 🛠️ Advanced Features
- **Batch Processing**  
  Queue multiple downloads and manage them simultaneously. Pause, resume, or cancel downloads easily.

- **Audio Extraction**  
  Extract audio tracks in **MP3** format, ideal for music or podcasts. (Requires **FFmpeg**.)

- **Profile Management**  
  Save your name, profile picture, download paths, and social media links. Profiles can be updated directly in the app.

- **Profile Import/Export**  
  Easily export your profile, settings, history, and profile picture as a single ZIP file, and import them back into the app on any device. Great for backup, migration, or restoring your preferences.

- **Drag & Drop Interface**  
  Add download URLs by dragging them into the app.

### 🎨 User Experience
- **Dark & Light Mode**  
  Switch between Dark and Light themes for better usability.

- **Error Handling**  
  Displays detailed error logs to debug issues.

- **Scheduler**  
  Schedule downloads to start at a specific time.

- **Download History**  
  View, search, and manage previous downloads directly in the app.

### 🔧 Technical Features
- **FFmpeg Detection**  
  Automatically detects FFmpeg installation and prompts for setup if missing.

- **Cross-Platform Compatibility**  
  Fully supported on **Linux** and **Windows**.

## 🚀 New in Version 4.4

### 🔥 Modular Codebase
- **Code has been fully refactored** into `core/`, `ui/`, and `tests/` directories.
- Easier to maintain, extend and contribute.

### 🔥 System Tray Integration
- Application now runs in the **system tray** when minimized.
- Quick access menu to restore or quit the app.

### 🔥 Improved Notification System
- **Download Complete** notifications.
- **Download Failed** alerts.
- **Download Canceled** warnings.

### 🔥 Enhanced Download System
- Fixed issues with **large file downloads**.
- Improved **stability and efficiency**.
- Better support for **multiple simultaneous downloads**.

### 🔥 Profile Management Upgrades
- Store your **name, profile picture, and social media links**.
- Improved UI for editing and updating user details.

### 🔥 Queue System Optimization
- **Concurrency management**: Limit simultaneous downloads.
- **Pause & Resume All**: Manage queued downloads easily.
- **Bandwidth Limiting Support** (via proxy settings).

### 🔥 Scheduler for Planned Downloads
- Schedule downloads for a specific **date and time**.
- Improved UI for managing scheduled downloads.

### 🔥 Other Improvements
- **Better UI animations and responsiveness.**
- **Logs now include color-coded messages**.
- **Search & filter options** in history and queue.

## 📸 Screenshots

<div align="center">
  <img src="assets/homepage.png" alt="Homepage" width="300"/>
  <img src="assets/history.png" alt="History" width="300"/>
  <img src="assets/settings.png" alt="Settings" width="300"/>
</div>

## ⚙️ Installation

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

```bash
# Launch the app
python main.py
```

- Configure your profile in the **Settings** or **Profile** page.
- Use the MP4 or MP3 pages to download videos or extract audio.
- Add multiple downloads to the queue and manage them from the Queue page.
- Schedule downloads in advance using the Scheduler.

## ⚠️ Notes

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

```bash
# We welcome contributions to improve YoutubeGO 4.4.
# Please submit issues or pull requests via GitHub.

# Enjoy using YoutubeGO 4.4!
🚀
```

```bash
# License
# This project is licensed under the Apache License 2.0.
```

## ⚠️ Legal Notice

YoutubeGO is an independent open-source project. It operates independently from YouTube and Google, performing downloads and other operations without using their APIs. This project is not bound by YouTube's terms of service or rules.


