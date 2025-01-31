# 🎶 YoutubeGO 4.3🎥

YoutubeGO 4.3 is a **free, fast, and secure** multimedia downloader built with **Python** and **PyQt5**, offering advanced features and a developer-friendly interface. It includes robust functionality such as **profile management**, **FFmpeg detection**, **scheduler for planned downloads**, **drag-and-drop support**, and an **enhanced queue system**.

---

## 🌟 Key Features

- **Multi-Platform Support**  
  Download videos and audio from platforms supporting HTTP streams, including YouTube, Vimeo, and more.

- **Playlist Downloads**  
  Save entire playlists with sequential processing in just a few clicks.

- **Multiple Formats**  
  Download in **MP4** (video) and **MP3** (audio) formats with automatic conversion and merging.

- **High-Resolution Support**  
  Supports downloads up to **8K, 4K, 2K, 1080p, 720p, 360p**. Select your preferred resolution in Settings.

- **Batch Processing**  
  Queue multiple downloads and manage them simultaneously. Pause, resume, or cancel downloads easily.

- **Audio Extraction**  
  Extract audio tracks in **MP3** format, ideal for music or podcasts. (Requires **FFmpeg**.)

- **Profile Management**  
  Save your name, profile picture, download paths, and social media links. Profiles can be updated directly in the app.

- **Drag & Drop Interface**  
  Add download URLs by dragging them into the app.

- **Dark & Light Mode**  
  Switch between Dark and Light themes for better usability.

- **Pause & Resume**  
  Manage downloads without restarting progress.

- **Error Handling**  
  Displays detailed error logs to debug issues.

- **Scheduler**  
  Schedule downloads to start at a specific time.

- **Download History**  
  View, search, and manage previous downloads directly in the app.

- **FFmpeg Detection**  
  Automatically detects FFmpeg installation and prompts for setup if missing.

- **Cross-Platform Compatibility**  
  Fully supported on **Linux**, **macOS**, and **Windows**.

---

## 💻 How It Works

The application leverages the following key components:

- **Python** for the core logic.
- **PyQt5** for the graphical user interface (GUI).
- **yt_dlp** for downloading videos and extracting metadata.
- **FFmpeg** for audio extraction and video merging.

Key modules and classes include:

- **`DragDropLineEdit`**: Handles drag-and-drop functionality for URLs.
- **`UserProfile`**: Manages user profile data including download paths, themes, and social media links.
- **`MainWindow`**: The main application window, featuring multiple pages such as Home, MP4/MP3 downloads, Queue, and Scheduler.
- **`DownloadTask`**: Represents individual download tasks with options like resolution, format, and subtitles.
- **`DownloadQueueWorker`**: Handles concurrent downloads and manages task progress.

---

## 🚀 New in Version 4.3

1. **Enhanced Profile Management**  
   Store your name, profile picture, and social media links (Instagram, Twitter, YouTube).

2. **Improved Queue System**  
   Concurrency management, pause/resume all, and bandwidth limiting.

3. **Scheduler**  
   Schedule downloads for a specific date and time.

4. **FFmpeg Integration**  
   Detects FFmpeg installation automatically. Displays status (found/missing) in the UI.

5. **Light & Dark Modes**  
   Instant switching with theme preferences saved automatically.

6. **Download History Management**  
   Search, enable/disable logging, and delete individual or all history entries.

---

## ⚙️ Installation

1. Clone or download this repository.
2. Ensure **Python 3.7+** is installed.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install **FFmpeg** for audio and video processing:

   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` or `sudo pacman -S ffmpeg`
   - **Windows**: Download from [official FFmpeg site](https://ffmpeg.org) or install via `winget`.

5. Run the application:

   ```bash
   python youtube_go_4_3.py
   ```

---

## 🔧 Usage

- Launch the app and configure your profile in the **Settings** or **Profile** page.
- Use the MP4 or MP3 pages to download videos or extract audio.
- Add multiple downloads to the queue and manage them from the Queue page.
- Schedule downloads in advance using the Scheduler.

---

## ⚠️ Notes

- **FFmpeg Required**: Some features, like audio extraction and video merging, depend on FFmpeg. Ensure it’s installed and available in your system PATH.
- **Third-Party Libraries**: The app uses `yt_dlp` for downloading and metadata extraction. Refer to their [GitHub page](https://github.com/yt-dlp/yt-dlp) for details.

---

## 🙏 Contributions

We welcome contributions to improve YoutubeGO 4.3. Please submit issues or pull requests via GitHub.

**Enjoy using YoutubeGO 4.3!**


 **This project is licensed under the Apache License 2.0.**
