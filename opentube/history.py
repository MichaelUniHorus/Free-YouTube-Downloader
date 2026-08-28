import os
import json
import time
from dataclasses import dataclass, field, asdict
from typing import Optional
from pathlib import Path


@dataclass
class HistoryEntry:
    url: str
    title: str
    format: str
    quality: str
    filepath: str
    timestamp: float = field(default_factory=time.time)
    status: str = "completed"


class HistoryManager:
    def __init__(self, filepath: Optional[str] = None):
        if filepath is None:
            config_dir = Path.home() / ".opentube"
            config_dir.mkdir(parents=True, exist_ok=True)
            filepath = str(config_dir / "history.json")
        self.filepath = filepath
        self.entries: list[HistoryEntry] = []
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.entries = [HistoryEntry(**e) for e in data]
            except (json.JSONDecodeError, TypeError):
                self.entries = []

    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([asdict(e) for e in self.entries], f, ensure_ascii=False, indent=2)

    def add(self, entry: HistoryEntry):
        self.entries.append(entry)
        self._save()

    def clear(self):
        self.entries.clear()
        self._save()

    def remove(self, index: int):
        if 0 <= index < len(self.entries):
            self.entries.pop(index)
            self._save()
