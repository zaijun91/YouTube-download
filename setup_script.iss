[Setup]
AppName=YouTube Downloader
AppVersion=1.0
DefaultDirName={autopf}\YouTube Downloader
DefaultGroupName=YouTube Downloader
UninstallDisplayIcon={app}\downloader_gui.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
OutputBaseFilename=YouTubeDownloader_Setup

[Files]
Source: "dist\downloader_gui.exe"; DestDir: "{app}"
Source: "yt.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\YouTube Downloader"; Filename: "{app}\downloader_gui.exe"
Name: "{commondesktop}\YouTube Downloader"; Filename: "{app}\downloader_gui.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional shortcuts:";

[Run]
Filename: "{app}\downloader_gui.exe"; Description: "Launch application"; Flags: nowait postinstall skipifsilent