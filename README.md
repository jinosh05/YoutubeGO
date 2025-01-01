# 🎶 YoutubeGO 3.0 🎥

YoutubeGO 3.0 is a 🌟 free, fast, and secure tool designed for downloading videos and playlists effortlessly from any platform. Built with **Python** and **PyQt5**, it offers advanced features and a user-friendly interface tailored for developers and power users. 🚀

---

## 🌟 Why Choose YoutubeGO 3.0?

- **Multi-Platform Support** - Download videos and audio from any platform supporting HTTP streams, including YouTube and Vimeo.
- **Playlist Downloads** - Save entire playlists with sequential processing in just a few clicks.
- **Multiple Formats** - Download in **MP4** (video 🎬) and **MP3** (audio 🎶) formats with automatic conversion.
- **High-Resolution Support** - Supports downloads up to **8K, 4K, 2K, 1080p, 720p, and 360p**.
- **Batch Processing** - Queue multiple downloads and process them simultaneously.
- **Audio Extraction** - Extract audio tracks directly in **MP3** format for music or podcasts.
- **Drag & Drop Support** - Add download URLs by simply dragging and dropping them into the interface.
- **Dark Mode** - Modern dark theme for better usability and appearance.
- **Pause & Resume Support** - Manage downloads seamlessly without restarting progress.
- **Performance Control** - Customize performance with modes like **High**, **Balanced**, and **Normal**.
- **Error Handling** - Displays detailed error messages to debug issues quickly.
- **Download History Management** - Track and log past downloads for easy reference.
- **Audio and Video Merging** - Combines separate video and audio streams into a single file automatically.
- **Sequential Downloading System** - Ensures prioritized and ordered processing for queues.
- **Cross-Platform Compatibility** - Fully supported on **Linux** and **Windows**.

---

## 💻 Use Cases

- **Offline Access** - Save playlists and videos for offline viewing.
- **Content Archiving** - Create backups of educational videos, music, and tutorials.
- **Podcast Downloads** - Extract and organize audio content in high-quality MP3 format.
- **Presentations & Teaching** - Save instructional videos for classroom and presentation use.

---

## 🔧 Installation

### Linux

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/youtubego3.git
   cd youtubego3
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**

   ```bash
   python3 youtubego3.py
   ```

4. **Build Executable for Linux:**

   ```bash
   pyinstaller --onefile --hidden-import=yt_dlp youtubego3.py
   ./dist/youtubego3
   ```

### Windows

1. Download and install **Python 3.10+**.
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application:**
   ```bash
   python youtubego3.py
   ```
4. **Build Executable for Windows:**
   ```bash
   pyinstaller --onefile --hidden-import=yt_dlp youtubego3.py
   dist\youtubego3.exe
   ```

---

## ⚙️ FFmpeg Notice

This project uses **FFmpeg**, a library for handling multimedia data. FFmpeg binaries must be available in your system's PATH for the tool to function properly. FFmpeg is licensed under **LGPL** or **GPL**, depending on how it is compiled.

For more details, visit the [official FFmpeg website](https://ffmpeg.org).

---



---

