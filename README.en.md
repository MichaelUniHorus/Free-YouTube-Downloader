<div align="center">

# OpenTube

**Free YouTube Downloader**

**English** | [Russian](README.md)

[![Release](https://img.shields.io/github/v/release/MichaelUniHorus/Free-YouTube-Downloader?color=e94560&style=for-the-badge)](https://github.com/MichaelUniHorus/Free-YouTube-Downloader/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.10%2B-16213e?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-0f3460?style=for-the-badge)](LICENSE)

</div>

---

## About

OpenTube is a free desktop application for downloading YouTube videos and audio. Download content in different qualities, convert sound to MP3, and manage your download history in a single window.

---

## Features

| Feature | Description |
| --- | --- |
| Video | Download from 144p up to 4K and higher |
| Audio | Extract MP3 with bitrate choice: 128/192/256/320 kbps |
| Preview | View thumbnail, title, channel, and duration |
| Progress | Download bar, speed, remaining time, and file size |
| History | List of downloaded files with quick open |
| Interface | Modern dark UI built with PyQt6 |

---

## Screenshots

> Screenshots of the interface will be added here.

---

## Quick Start

### Download the ready-to-use build

1. Go to [Releases](https://github.com/MichaelUniHorus/Free-YouTube-Downloader/releases/latest)
2. Download `OpenTube-v1.0.1.zip`
3. Extract and run `OpenTube.exe`

### Run from source

```bash
git clone https://github.com/MichaelUniHorus/Free-YouTube-Downloader.git
cd Free-YouTube-Downloader
pip install -r requirements.txt
python main.py
```

---

## Usage

1. Paste a YouTube video link.
2. Click **Information** to fetch metadata.
3. Choose **video quality** or enable **Audio only (MP3)**.
4. Set the save folder.
5. Click **Download**.

---

## Requirements

- Windows 10/11
- Python 3.10+ (only for running from source)
- FFmpeg — already included in the portable build

---

## Technologies

- **PyQt6** — GUI framework
- **yt-dlp** — YouTube video downloader engine
- **FFmpeg** — audio conversion and stream merging

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
