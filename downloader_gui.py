import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import threading
import os
import sys
import json
import sv_ttk
import shutil


CONFIG_FILE = "config.json"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_application_path():
    """
    Determines the application's base path.
    Works for both a script and a bundled PyInstaller exe.
    """
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return application_path


class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("视频下载器 (基于 yt-dlp)")
        self.root.geometry("600x400")
        
        # --- 加载配置 ---
        self.config = self.load_config()

        # --- 设置图标 ---
        try:
            icon_path = resource_path('yt.ico')
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error setting icon: {e}")

        # --- 框架 ---
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- URL 输入 ---
        url_label = ttk.Label(main_frame, text="视频链接:")
        url_label.pack(fill=tk.X, padx=5, pady=(0, 8))
        self.url_entry = ttk.Entry(main_frame, width=80)
        self.url_entry.pack(fill=tk.X, padx=5, pady=2)

        # --- 文件夹选择 ---
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, padx=5, pady=15)
        
        path_label = ttk.Label(path_frame, text="保存到:")
        path_label.pack(side=tk.LEFT, pady=2)
        self.path_entry = ttk.Entry(path_frame, width=60)
        self.path_entry.insert(0, self.config.get("download_path", ""))
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)
        browse_button = ttk.Button(path_frame, text="浏览...", command=self.browse_folder)
        browse_button.pack(side=tk.LEFT, padx=5, pady=2)

        # --- 选项 ---
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, padx=5, pady=10)

        self.download_mode = tk.StringVar(value=self.config.get("download_mode", "video"))
        video_radio = ttk.Radiobutton(options_frame, text="视频下载", variable=self.download_mode, value="video")
        video_radio.pack(side=tk.LEFT, padx=10)
        audio_radio = ttk.Radiobutton(options_frame, text="仅音频", variable=self.download_mode, value="audio")
        audio_radio.pack(side=tk.LEFT, padx=10)

        self.use_browser_cookies = tk.BooleanVar(value=self.config.get("use_browser_cookies", False))
        cookies_check = ttk.Checkbutton(options_frame, text="使用浏览器 Cookie", variable=self.use_browser_cookies)
        cookies_check.pack(side=tk.RIGHT, padx=10)

        # --- 下载按钮 ---
        self.download_button = ttk.Button(main_frame, text="下载", command=self.start_download_thread)
        self.download_button.pack(pady=25, ipady=6, ipadx=10)

        # --- 进度条和状态 ---
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(fill=tk.X, padx=5, pady=5)
        self.status_label = ttk.Label(main_frame, text="准备就绪")
        self.status_label.pack(fill=tk.X, padx=5, pady=5)

        # --- 检查依赖 ---
        self.check_dependencies()

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total_bytes:
                percentage = d['downloaded_bytes'] / total_bytes * 100
                self.progress['value'] = percentage
                status_text = f"正在下载: {d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']}"
                self.status_label.config(text=status_text)
                self.root.update_idletasks()
        elif d['status'] == 'finished':
            self.status_label.config(text="下载完成！正在处理...")
            self.root.update_idletasks()

    def download_video(self):
        url = self.url_entry.get()
        path = self.path_entry.get()

        if not url:
            messagebox.showerror("错误", "请输入视频链接！")
            return
        if not path:
            messagebox.showerror("错误", "请选择保存文件夹！")
            return

        self.download_button.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.status_label.config(text="正在准备下载...")

        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'progress_hooks': [self.progress_hook],
        }

        # 根据模式设置 format
        mode = self.download_mode.get()
        if mode == 'audio':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else: # video
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

        # 根据选项设置 cookie
        if self.use_browser_cookies.get():
            self.status_label.config(text="尝试从浏览器加载 Cookie...")
            # 这里我们假设用户最常用的是 Chrome，可以后续做的更复杂
            ydl_opts['cookies-from-browser'] = ('chrome',)
        else:
            cookie_file_path = os.path.join(get_application_path(), 'cookies.txt')
            if os.path.exists(cookie_file_path):
                self.status_label.config(text="检测到 cookies.txt，将使用 Cookie 进行下载...")
                ydl_opts['cookiefile'] = cookie_file_path
            else:
                self.status_label.config(text="未检测到 cookies.txt，将进行常规下载...")
        
        self.root.update_idletasks()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # 保存配置
            self.config["download_path"] = path
            self.config["download_mode"] = self.download_mode.get()
            self.config["use_browser_cookies"] = self.use_browser_cookies.get()
            self.save_config()

            messagebox.showinfo("成功", "视频下载完成！")
        except Exception as e:
            messagebox.showerror("下载失败", f"发生错误: {str(e)}")
        finally:
            self.download_button.config(state=tk.NORMAL)
            self.status_label.config(text="准备就绪")
            self.progress['value'] = 0

    def start_download_thread(self):
        download_thread = threading.Thread(target=self.download_video, daemon=True)
        download_thread.start()

    def load_config(self):
        config_path = os.path.join(get_application_path(), CONFIG_FILE)
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}

    def save_config(self):
        config_path = os.path.join(get_application_path(), CONFIG_FILE)
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def check_dependencies(self):
        if not shutil.which('ffmpeg'):
            self.download_button.config(state=tk.DISABLED)
            self.status_label.config(text="错误: 未找到 ffmpeg。请安装 ffmpeg 并将其添加到系统 PATH。")


if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    
    # 设置主题
    sv_ttk.set_theme("light")

    # --- 精细化样式配置 ---
    style = ttk.Style()
    
    # 颜色
    bg_color = "#F5F5F7"
    fg_color = "#1D1D1F"
    
    # 字体
    font_name = "PingFang SC"
    font_size = 10
    
    try:
        # 尝试设置苹方字体
        regular_font = (font_name, font_size)
        bold_font = (font_name, font_size, "bold")
    except tk.TclError:
        print(f"字体 '{font_name}' 未找到，将使用系统默认字体。")
        # 回退到备用字体
        font_name = "Microsoft YaHei UI"
        regular_font = (font_name, font_size)
        bold_font = (font_name, font_size, "bold")

    # 应用样式
    root.configure(bg=bg_color)
    style.configure(".", font=regular_font, background=bg_color, foreground=fg_color)
    style.configure("TLabel", background=bg_color, foreground=fg_color)
    style.configure("TRadiobutton", background=bg_color, foreground=fg_color)
    style.configure("TCheckbutton", background=bg_color, foreground=fg_color)
    style.configure("TFrame", background=bg_color)
    
    # 按钮样式
    style.configure(
        "TButton",
        font=bold_font,
        borderwidth=0,
        relief="flat",
        padding=10
    )
    style.map(
        "TButton",
        background=[("active", "#EAEAEB"), ("!active", "#FFFFFF")],
        foreground=[("!disabled", fg_color)]
    )

    root.mainloop()