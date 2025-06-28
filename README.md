# YouTube 下载器 GUI

一个简洁、现代化且易于使用的桌面应用程序，用于下载 YouTube 视频和音频，使用 Python 和 Tkinter 构建。

<!-- 您可以将应用的截图上传到图床 (如 imgur.com) 并在此处粘贴链接 -->

## ✨ 功能特性

- **现代化界面**: 基于 `sv-ttk` 主题的干净、直观的用户界面。
- **多种下载模式**:
  - **视频模式**: 下载最高可用画质的视频流（包含音频）。
  - **音频模式**: 仅下载最高品质的音频，并保存为 `.mp3` 文件。
- **配置记忆**: 自动保存您上次使用的下载路径和选择的模式，方便下次使用。
- **Cookie 支持**: 允许使用 `cookies.txt` 文件来下载有年龄限制或需要登录的视频。
- **独立可执行文件**: 已打包为单个 `.exe` 文件，最终用户无需安装 Python 环境。
- **依赖项检查**: 启动时会自动检查所需的 `ffmpeg` 依赖是否存在。

## 🚀 如何使用 (最终用户)

1.  **下载**: 前往本项目的 [**Releases (发行版)**](https://github.com/zaijun91/YouTube-download/releases) 页面。
2.  **找到最新的 Release**，然后下载 `YouTube-Downloader-Setup.exe` 安装程序。
3.  **安装**: 运行安装文件，并按照屏幕上的指示完成安装。
4.  **运行**: 从您的开始菜单或桌面快捷方式启动 "YouTube Downloader"。
5.  **粘贴链接并下载**: 将 YouTube 视频的 URL 粘贴到输入框中，选择您希望的保存路径和下载模式，然后点击“下载”。

**重要提示**: 本程序需要 **FFmpeg** 才能合并视频和音频。请确保您已经安装了 FFmpeg，并将其添加到了系统的 PATH 环境变量中。您可以从 [ffmpeg.org](https://ffmpeg.org/download.html) 下载。

## 🛠️ 如何开发 (开发者)

### 环境要求

- Python 3.8+
- Git
- FFmpeg (已添加到系统 PATH)

### 安装步骤

1.  **克隆仓库:**
    ```bash
    git clone https://github.com/zaijun91/YouTube-download.git
    cd YouTube-download
    ```

2.  **创建虚拟环境并安装依赖:**
    ```bash
    # Windows 系统
    python -m venv venv
    .\venv\Scripts\activate
    
    # 安装依赖包
    pip install -r requirements.txt 
    ```

3.  **运行程序:**
    ```bash
    python downloader_gui.py
    ```

4.  **构建可执行文件 (使用 PyInstaller):**
    ```bash
    pyinstaller --noconfirm --onefile --windowed --icon "yt.ico" --add-data "yt.ico;." --add-data "cookies.txt;." downloader_gui.py
    ```

## 💻 技术栈

- **核心**: Python
- **后端逻辑**: `yt-dlp`
- **图形界面**: `Tkinter`, `sv-ttk`
- **打包工具**: `PyInstaller`
- **安装程序**: `Inno Setup`
