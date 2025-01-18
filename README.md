# 🎶 YoutubeGO 4.2 🎥

YoutubeGO 4.2 is a **free, fast, and secure** multimedia downloader built with **Python** and **PyQt5**, offering advanced features and a developer-friendly interface. It expands on the capabilities of the 3.0 version with new functionality such as **server status checks**, **profile management with social media links**, **FFmpeg detection**, **scheduler for planned downloads**, and an **enhanced queue system**.

---

## 🌟 Why Choose YoutubeGO 4.2?

- **Multi-Platform Support**  
  Download videos and audio from any platform supporting HTTP streams, including YouTube, Vimeo, and more.

- **Playlist Downloads**  
  Save entire playlists with sequential processing in just a few clicks—now with improved concurrency handling.

- **Multiple Formats**  
  Download in **MP4** (video) and **MP3** (audio) formats with automatic conversion and merging (video + audio).

- **High-Resolution Support**  
  Supports downloads up to **8K, 4K, 2K, 1080p, 720p, 360p**—select your preferred resolution in Settings.

- **Batch Processing**  
  **Queue multiple downloads** and run them simultaneously (or in a prioritized sequence). You can pause/resume/cancel individual items or entire queues.

- **Audio Extraction**  
  Extract audio tracks directly in **MP3** format, ideal for music or podcasts. (Requires **FFmpeg**.)

- **Profile Management**  
  **Store your name, profile picture, and social media links** (Instagram, Twitter, YouTube). A dedicated Profile page in the new UI handles these details.

- **Drag & Drop**  
  Add download URLs by simply dragging and dropping them onto the interface.

- **Dark & Light Mode**  
  Switch between modern **Dark** or **Light** themes for better usability and appearance.

- **Pause & Resume**  
  Manage downloads seamlessly without restarting progress; improved concurrency logic prevents conflicts.

- **Performance Control**  
  Choose **High**, **Balanced**, or **Normal** performance (bandwidth-limiting or proxy can be set in advanced Settings).

- **Error Handling**  
  Displays detailed error messages (with logs) to debug issues quickly. Helpful status indicators in the status bar.

- **Download History**  
  Track and log past downloads with searching and toggling (“Enable History Logging”). Quickly reference previous items.

- **Sequential Downloading & Automatic Merging**  
  Combines separate video and audio streams into a single file automatically. Queue items can be processed in order.

- **Scheduler**  
  **Schedule downloads** at specific times or dates, with automated start once the scheduled moment arrives.

- **Server Checks**  
  Periodically checks if `ytplaylistdown.com` (or another configured server) is active, showing its status in the UI.

- **Cross-Platform Compatibility**  
  Built on PyQt5, fully supported on **Linux** ,**Macos** and **Windows**.

---

## 💻 Use Cases

- **Offline Access**  
  Save playlists and videos for offline viewing—no more internet hassles.

- **Content Archiving**  
  Easily create backups of educational videos, music, and tutorials for future reference.

- **Podcast Downloads**  
  Extract and organize audio content in high-quality MP3 format to enjoy on the go.

- **Presentations & Teaching**  
  Securely store instructional videos for classrooms, lectures, or conferences.

---

## 🚀 What's New in 4.2?

1. **Profile Page Enhancements**  
   Store not just your name and picture, but also **Instagram**, **Twitter**, and **YouTube** links.

2. **Advanced Queue & Scheduler**  
   - **Queue** improvements: concurrency, pause/resume/cancel all, bandwidth-limiting.  
   - **Scheduler**: schedule downloads for a future date/time, automatically starting them at the specified moment.

3. **FFmpeg Detection**  
   - UI label shows **“FFmpeg Found”** (green) or **“FFmpeg Missing”** (red).  
   - If FFmpeg is missing, audio extraction or merging may be limited, and you are prompted to install it.

4. **Server Status**  
   - Automatic checks (every 60s) to see if `ytplaylistdown.com` is reachable.  
   - Displays **“Server Active”** or **“Server Inactive”** in the status bar.

5. **Light/Dark Theming**  
   - Switch instantly between Light and Dark modes from Settings.  
   - The app remembers your preference.

6. **Improved History & Searching**  
   - Enable/disable history logging.  
   - Search by keywords or partial text in the history table.

7. **Performance Tuning**  
   - Choose “High,” “Balanced,” or “Normal” (or custom) to limit download rates if desired, or set a proxy.

---

## ⚙️ FFmpeg Notice

This project uses **FFmpeg**, a library for processing multimedia data. To enable all features (especially audio extraction/merging), **FFmpeg** must be available in your system's PATH. FFmpeg is licensed under **LGPL** or **GPL** depending on compilation. For more details, visit the [official FFmpeg website](https://ffmpeg.org).

---

## 🔧 Installation and Usage

1. **Clone** or **download** this repository.
2. Ensure **Python 3.7+** and **PyQt5** are installed.
3. Install **FFmpeg** if you need audio extraction or merging.
4. Run `python youtube_go_4_2.py` (or the respective main file).
5. Start downloading with MP4/MP3 modes, queue scheduling, or advanced settings.

**Enjoy using YoutubeGO 4.2!** We welcome contributions and feedback.

---


