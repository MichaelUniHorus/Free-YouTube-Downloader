import os
import re
import sys
import shutil
import glob
import subprocess
from dataclasses import dataclass, field
from typing import Optional, Callable, Union
from PyQt6.QtCore import QThread, pyqtSignal

import yt_dlp


def _find_ffmpeg() -> Optional[str]:
    # 1. Bundled FFmpeg next to the .exe (portable build)
    exe_dir = os.path.dirname(sys.executable)
    if os.path.exists(os.path.join(exe_dir, "ffmpeg.exe")):
        return exe_dir

    # 2. WinGet FFmpeg
    winget = os.path.expandvars(
        r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg*\bin"
    )
    matches = sorted(glob.glob(winget), reverse=True)
    if matches:
        return matches[0]

    # 3. System PATH
    path = shutil.which("ffmpeg")
    if path:
        return os.path.dirname(path)
    return None


FFMPEG_LOCATION = _find_ffmpeg()


class _SilentLogger:
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass
    def get_output(self): return ""
    def read_stderr(self): return ""


@dataclass
class QualityOption:
    label: str
    format_string: str
    height: int
    ext: str
    estimated_size: Optional[int] = None
    fps: Optional[int] = None
    hdr: bool = False


@dataclass
class VideoInfo:
    title: str
    thumbnail: str
    duration: int
    uploader: str
    qualities: list[QualityOption]
    url: str
    view_count: int = 0


def _format_filesize(size: Optional[Union[int, float]]) -> str:
    if size is None or size <= 0:
        return "—"
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def _format_duration(seconds: int) -> str:
    if seconds <= 0:
        return "—"
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


class InfoFetcher(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def run(self):
        try:
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,
                "logger": _SilentLogger(),
            }
            if FFMPEG_LOCATION:
                ydl_opts["ffmpeg_location"] = FFMPEG_LOCATION

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)

            duration = info.get("duration", 0) or 0
            formats = info.get("formats", [])

            video_heights: dict[int, dict] = {}
            best_audio_br = 0
            best_audio_size = 0

            for f in formats:
                vcodec = f.get("vcodec", "none")
                acodec = f.get("acodec", "none")
                has_video = vcodec not in ("none", None)
                has_audio = acodec not in ("none", None)

                if has_video:
                    h = f.get("height") or 0
                    if h > 0:
                        vbr = f.get("vbr") or f.get("tbr") or 0
                        fps = f.get("fps") or 0
                        filesize = f.get("filesize") or f.get("filesize_approx") or 0
                        dynamic_range = f.get("dynamic_range", "SDR")
                        is_hdr = dynamic_range in ("HDR", "Dolby Vision", "HDR10")
                        key = (h, fps, is_hdr)
                        existing = video_heights.get(h)
                        if existing is None:
                            video_heights[h] = {
                                "fps": fps, "vbr": vbr, "filesize": filesize,
                                "is_hdr": is_hdr, "ext": f.get("ext", "mp4"),
                            }
                        else:
                            if vbr > (existing.get("vbr") or 0):
                                video_heights[h] = {
                                    "fps": fps, "vbr": vbr, "filesize": filesize,
                                    "is_hdr": is_hdr, "ext": f.get("ext", "mp4"),
                                }

                if has_audio and not has_video:
                    abr = f.get("abr") or f.get("tbr") or 0
                    if abr > best_audio_br:
                        best_audio_br = abr
                        best_audio_size = f.get("filesize") or f.get("filesize_approx") or 0

            qualities: list[QualityOption] = []
            for h in sorted(video_heights.keys(), reverse=True):
                data = video_heights[h]
                fps = data["fps"]
                vbr = data["vbr"]
                is_hdr = data["is_hdr"]
                ext = data["ext"]

                v_size = data["filesize"]
                if not v_size and vbr and duration:
                    v_size = int(vbr * 1024 * duration / 8)
                a_size = best_audio_size
                if not a_size and best_audio_br and duration:
                    a_size = int(best_audio_br * 1024 * duration / 8)
                est_total = (v_size or 0) + (a_size or 0) or None

                fps_str = f"@{fps}" if fps and fps > 30 else ""
                hdr_str = " HDR" if is_hdr else ""
                size_str = _format_filesize(est_total)
                label = f"{h}p{fps_str}{hdr_str} — {ext.upper()} — ~{size_str}"

                fmt_str = (
                    f"bestvideo[height<={h}][ext=mp4]+bestaudio[ext=m4a]/"
                    f"bestvideo[height<={h}]+bestaudio/"
                    f"best[height<={h}]"
                )

                qualities.append(QualityOption(
                    label=label,
                    format_string=fmt_str,
                    height=h,
                    ext=ext,
                    estimated_size=est_total,
                    fps=fps,
                    hdr=is_hdr,
                ))

            if not qualities:
                qualities.append(QualityOption(
                    label="Лучшее доступное",
                    format_string="best",
                    height=0,
                    ext="mp4",
                ))

            video_info = VideoInfo(
                title=info.get("title", "Unknown"),
                thumbnail=info.get("thumbnail", ""),
                duration=duration,
                uploader=info.get("uploader", "Unknown"),
                qualities=qualities,
                url=self.url,
                view_count=info.get("view_count", 0) or 0,
            )
            self.finished.emit(video_info)
        except Exception as e:
            self.error.emit(str(e))


class Downloader(QThread):
    progress = pyqtSignal(float, str, str, str, str)  # percent, speed_str, eta_str, downloaded_str, phase
    postprocessing = pyqtSignal(str)  # status text
    finished = pyqtSignal(str, str)  # filepath, title
    error = pyqtSignal(str)

    def __init__(self, url: str, format_string: str, output_dir: str,
                 audio_only: bool = False, audio_quality: str = "192"):
        super().__init__()
        self.url = url
        self.format_string = format_string
        self.output_dir = output_dir
        self.audio_only = audio_only
        self.audio_quality = audio_quality
        self._total_bytes = 0
        self._downloaded_bytes = 0
        self._phase = "download"

    def _progress_hook(self, d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes", 0)

            frag_idx = d.get("fragment_index") or 0
            frag_count = d.get("fragment_count") or 0

            if total > 0:
                percent = (downloaded / total) * 100
            elif frag_count > 0:
                percent = (frag_idx / frag_count) * 100
            else:
                percent = 0

            speed = d.get("speed") or 0
            eta = d.get("eta") or 0

            speed_str = _format_filesize(int(speed)) + "/s" if speed else "—"
            if eta > 0:
                eta_str = f"{int(eta // 60)}:{int(eta % 60):02d}"
            else:
                eta_str = "—"
            downloaded_str = _format_filesize(downloaded)
            total_str = _format_filesize(total) if total else "~"

            info_str = f"{downloaded_str} / {total_str}"

            self.progress.emit(percent, speed_str, eta_str, info_str, self._phase)

        elif d["status"] == "finished":
            self._phase = "merging"
            self.progress.emit(100.0, "—", "—", "", "merging")

    def _postprocessing_hook(self, d):
        if d.get("status") == "started":
            self._phase = "converting"
            self.postprocessing.emit("Конвертация...")
        elif d.get("status") == "finished":
            self.postprocessing.emit("")

    def run(self):
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            output_template = os.path.join(self.output_dir, "%(title).200B.%(ext)s")

            base_opts = {
                "outtmpl": output_template,
                "progress_hooks": [self._progress_hook],
                "quiet": True,
                "no_warnings": True,
                "noprogress": True,
                "logger": _SilentLogger(),
            }
            if FFMPEG_LOCATION:
                base_opts["ffmpeg_location"] = FFMPEG_LOCATION

            if self.audio_only:
                ydl_opts = {
                    **base_opts,
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": self.audio_quality,
                        },
                        {
                            "key": "FFmpegMetadata",
                            "add_metadata": True,
                        },
                    ],
                }
            else:
                ydl_opts = {
                    **base_opts,
                    "format": self.format_string if self.format_string else "best",
                    "merge_output_format": "mp4",
                    "keepvideo": False,
                    "postprocessors": [
                        {
                            "key": "FFmpegVideoConvertor",
                            "preferedformat": "mp4",
                        },
                        {
                            "key": "FFmpegMetadata",
                            "add_metadata": True,
                        },
                    ],
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                filepath = ydl.prepare_filename(info)
                if self.audio_only:
                    base, _ = os.path.splitext(filepath)
                    filepath = base + ".mp3"
                self.finished.emit(filepath, info.get("title", ""))
        except Exception as e:
            self.error.emit(str(e))
