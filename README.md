# YouTube Downloader GUI

A simple, modern, and easy-to-use desktop application for downloading YouTube videos and audio, built with Python and Tkinter.

  <!-- You can upload a screenshot of the app to an image host like imgur.com and paste the link here -->

## ✨ Features

- **Modern UI**: Clean and intuitive user interface powered by the `sv-ttk` theme.
- **Multiple Download Modes**:
  - **Video Mode**: Downloads the best available video stream with audio.
  - **Audio Mode**: Downloads only the best quality audio, saved as an `.mp3` file.
- **Configuration Memory**: Remembers your last used download path and mode for convenience.
- **Cookie Support**: Allows using a `cookies.txt` file for downloading age-restricted or private videos.
- **Standalone Executable**: Packaged into a single `.exe` file, no Python installation required for end-users.
- **Dependency Check**: Automatically checks for the required `ffmpeg` dependency on startup.

## 🚀 How to Use (for End-Users)

1.  **Download**: Go to the [Releases](https://github.com/zaijun91/YouTube-download/releases) page and download the latest `YouTube-Downloader-Setup.exe`.
2.  **Install**: Run the setup file and follow the installation instructions.
3.  **Run**: Launch the "YouTube Downloader" application from your Start Menu or Desktop shortcut.
4.  **Paste & Download**: Paste a YouTube video URL into the input box, select your desired download path and mode, and click "Download".

**Important**: This application requires **FFmpeg** to be installed and accessible in your system's PATH to merge video and audio streams. You can download it from [ffmpeg.org](https://ffmpeg.org/download.html).

## 🛠️ How to Develop (for Developers)

### Prerequisites

- Python 3.8+
- Git
- FFmpeg (added to system PATH)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/zaijun91/YouTube-download.git
    cd YouTube-download
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # Install packages
    pip install -r requirements.txt 
    # Note: A requirements.txt file should be created for this.
    ```

3.  **Run the application:**
    ```bash
    python downloader_gui.py
    ```

4.  **Build the executable (using PyInstaller):**
    ```bash
    pyinstaller --noconfirm --onefile --windowed --icon "yt.ico" --add-data "yt.ico;." --add-data "cookies.txt;." downloader_gui.py
    ```

## 💻 Technology Stack

- **Core**: Python
- **Backend Logic**: `yt-dlp`
- **GUI**: `Tkinter`, `sv-ttk`
- **Packaging**: `PyInstaller`
- **Installer**: `Inno Setup`
