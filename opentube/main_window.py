import os
from datetime import timedelta, datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QCheckBox, QProgressBar,
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog,
    QTabWidget, QScrollArea, QGroupBox, QMessageBox, QSpinBox,
    QFrame, QSizePolicy,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QFont, QDesktopServices
from PyQt6.QtCore import QUrl

from .downloader import InfoFetcher, Downloader, VideoInfo, QualityOption, _format_filesize, _format_duration
from .history import HistoryManager, HistoryEntry


STYLESHEET = """
QMainWindow { background-color: #0f0f1e; }
QLabel { color: #e0e0e0; }
QLineEdit {
    background-color: #1a1a2e; color: #e0e0e0;
    border: 2px solid #16213e; border-radius: 8px; padding: 10px 12px;
    font-size: 14px;
}
QLineEdit:focus { border: 2px solid #e94560; }
QPushButton {
    background-color: #e94560; color: white; border: none;
    border-radius: 8px; padding: 10px 24px; font-weight: bold;
    font-size: 14px;
}
QPushButton:hover { background-color: #ff5a7a; }
QPushButton:pressed { background-color: #c73650; }
QPushButton:disabled { background-color: #333; color: #666; }
QPushButton#secondary {
    background-color: #16213e; border: 1px solid #0f3460;
}
QPushButton#secondary:hover { background-color: #1a4a7a; border-color: #e94560; }
QComboBox {
    background-color: #1a1a2e; color: #e0e0e0;
    border: 2px solid #16213e; border-radius: 8px; padding: 8px 12px;
    font-size: 14px; min-height: 20px;
}
QComboBox:hover { border: 2px solid #0f3460; }
QComboBox::drop-down { border: none; width: 30px; }
QComboBox::down-arrow {
    image: none; border-left: 5px solid transparent;
    border-right: 5px solid transparent; border-top: 6px solid #e94560;
    width: 0; height: 0; margin-right: 10px;
}
QComboBox QAbstractItemView {
    background-color: #1a1a2e; color: #e0e0e0;
    selection-background-color: #e94560; border: 1px solid #0f3460;
    outline: none; padding: 4px;
}
QCheckBox { color: #e0e0e0; font-size: 14px; spacing: 8px; }
QCheckBox::indicator {
    width: 20px; height: 20px; border-radius: 4px;
    border: 2px solid #0f3460; background-color: #1a1a2e;
}
QCheckBox::indicator:checked {
    background-color: #e94560; border: 2px solid #e94560;
}
QProgressBar {
    background-color: #1a1a2e; border: 2px solid #16213e;
    border-radius: 8px; text-align: center; color: white;
    font-size: 13px; font-weight: bold; min-height: 28px;
}
QProgressBar::chunk {
    border-radius: 6px;
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #e94560, stop:1 #ff7a9a);
}
QTableWidget {
    background-color: #1a1a2e; color: #e0e0e0;
    border: 1px solid #16213e; border-radius: 8px;
    gridline-color: #16213e; outline: none;
    alternate-background-color: #16213e;
}
QTableWidget::item:selected { background-color: #e94560; }
QTableWidget::item { padding: 6px; }
QHeaderView::section {
    background-color: #0f3460; color: #e0e0e0;
    border: none; padding: 8px; font-weight: bold;
    font-size: 13px;
}
QGroupBox {
    color: #e94560; border: 2px solid #16213e;
    border-radius: 10px; margin-top: 14px; padding: 18px 12px 12px 12px;
    font-size: 14px; font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin; left: 16px; padding: 0 8px;
}
QTabWidget::pane {
    border: 2px solid #16213e; border-radius: 10px;
    background-color: #0f0f1e;
}
QTabBar::tab {
    background-color: #1a1a2e; color: #888;
    padding: 10px 28px; border: 2px solid #16213e;
    border-bottom: none; border-top-left-radius: 8px; border-top-right-radius: 8px;
    font-size: 14px; font-weight: bold; margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #0f0f1e; color: #e94560;
    border-bottom: 2px solid #0f0f1e;
}
QTabBar::tab:hover:!selected { color: #ccc; }
QScrollArea { border: none; }
QFrame#card {
    background-color: #1a1a2e; border-radius: 10px;
}
"""


class ThumbnailLoader(QThread):
    finished = pyqtSignal(QPixmap)

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def run(self):
        import urllib.request
        try:
            data = urllib.request.urlopen(self.url, timeout=10).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.finished.emit(pixmap)
        except Exception:
            self.finished.emit(QPixmap())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenTube — YouTube Downloader")
        self.setMinimumSize(850, 650)
        self.resize(960, 760)
        self.setStyleSheet(STYLESHEET)

        self.history = HistoryManager()
        self.current_video_info: VideoInfo | None = None
        self.downloader: Downloader | None = None
        self.info_fetcher: InfoFetcher | None = None
        self.thumbnail_loader: ThumbnailLoader | None = None
        self.output_dir = os.path.join(os.path.expanduser("~"), "Downloads", "OpenTube")

        self._build_ui()
        self._refresh_history_table()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        header = QHBoxLayout()
        title_label = QLabel("OpenTube")
        title_label.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #e94560;")
        header.addWidget(title_label)

        subtitle = QLabel("YouTube Video & Audio Downloader")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #666; padding-top: 12px;")
        header.addWidget(subtitle)
        header.addStretch()
        main_layout.addLayout(header)

        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        download_tab = QWidget()
        tabs.addTab(download_tab, "  Загрузка  ")
        self._build_download_tab(download_tab)

        history_tab = QWidget()
        tabs.addTab(history_tab, "  История  ")
        self._build_history_tab(history_tab)

        settings_tab = QWidget()
        tabs.addTab(settings_tab, "  Настройки  ")
        self._build_settings_tab(settings_tab)

    def _build_download_tab(self, parent):
        layout = QVBoxLayout(parent)
        layout.setSpacing(10)

        url_group = QGroupBox("Ссылка на видео")
        url_layout = QHBoxLayout(url_group)
        url_layout.setSpacing(10)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Вставьте ссылку YouTube (https://youtube.com/watch?v=... или https://youtu.be/...)")
        self.url_input.returnPressed.connect(self._fetch_info)
        url_layout.addWidget(self.url_input)

        self.fetch_btn = QPushButton("Информация")
        self.fetch_btn.clicked.connect(self._fetch_info)
        url_layout.addWidget(self.fetch_btn)
        layout.addWidget(url_group)

        info_group = QGroupBox("Информация о видео")
        info_layout = QHBoxLayout(info_group)
        info_layout.setSpacing(16)

        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(320, 180)
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setStyleSheet("background-color: #16213e; border-radius: 8px; color: #555; font-size: 13px;")
        self.thumbnail_label.setText("Превью появится\nпосле ввода ссылки")
        info_layout.addWidget(self.thumbnail_label)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(8)

        self.info_title = QLabel("Название: —")
        self.info_title.setWordWrap(True)
        self.info_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.info_title.setStyleSheet("color: #fff;")
        text_layout.addWidget(self.info_title)

        self.info_uploader = QLabel("Канал: —")
        self.info_uploader.setStyleSheet("color: #aaa; font-size: 13px;")
        text_layout.addWidget(self.info_uploader)

        self.info_duration = QLabel("Длительность: —")
        self.info_duration.setStyleSheet("color: #aaa; font-size: 13px;")
        text_layout.addWidget(self.info_duration)

        self.info_views = QLabel("Просмотры: —")
        self.info_views.setStyleSheet("color: #aaa; font-size: 13px;")
        text_layout.addWidget(self.info_views)

        text_layout.addStretch()
        info_layout.addLayout(text_layout, 1)
        layout.addWidget(info_group)

        format_group = QGroupBox("Настройки загрузки")
        format_layout = QVBoxLayout(format_group)
        format_layout.setSpacing(10)

        fmt_row = QHBoxLayout()
        fmt_label = QLabel("Качество:")
        fmt_label.setStyleSheet("font-size: 14px;")
        fmt_row.addWidget(fmt_label)
        self.format_combo = QComboBox()
        self.format_combo.setMinimumWidth(450)
        self.format_combo.setEnabled(False)
        fmt_row.addWidget(self.format_combo, 1)
        format_layout.addLayout(fmt_row)

        audio_row = QHBoxLayout()
        self.audio_only_check = QCheckBox("Только аудио (MP3)")
        self.audio_only_check.toggled.connect(self._on_audio_only_toggled)
        audio_row.addWidget(self.audio_only_check)

        audio_row.addWidget(QLabel("Битрейт:"))
        self.audio_quality_combo = QComboBox()
        self.audio_quality_combo.addItems(["128 kbps", "192 kbps", "256 kbps", "320 kbps"])
        self.audio_quality_combo.setCurrentText("192 kbps")
        self.audio_quality_combo.setFixedWidth(120)
        self.audio_quality_combo.setEnabled(False)
        self.audio_only_check.toggled.connect(self.audio_quality_combo.setEnabled)
        audio_row.addWidget(self.audio_quality_combo)
        audio_row.addStretch()
        format_layout.addLayout(audio_row)

        dir_row = QHBoxLayout()
        dir_label = QLabel("Папка:")
        dir_label.setStyleSheet("font-size: 14px;")
        dir_row.addWidget(dir_label)
        self.dir_label = QLabel(self.output_dir)
        self.dir_label.setWordWrap(True)
        self.dir_label.setStyleSheet("color: #888; font-size: 13px;")
        dir_row.addWidget(self.dir_label, 1)

        browse_btn = QPushButton("Выбрать")
        browse_btn.setObjectName("secondary")
        browse_btn.clicked.connect(self._browse_dir)
        dir_row.addWidget(browse_btn)
        format_layout.addLayout(dir_row)

        layout.addWidget(format_group)

        dl_row = QHBoxLayout()
        self.download_btn = QPushButton("Скачать")
        self.download_btn.setFixedHeight(46)
        self.download_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.download_btn.clicked.connect(self._start_download)
        self.download_btn.setEnabled(False)
        dl_row.addWidget(self.download_btn)
        layout.addLayout(dl_row)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(32)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        progress_info = QHBoxLayout()
        self.progress_speed = QLabel("")
        self.progress_speed.setStyleSheet("color: #e94560; font-size: 13px; font-weight: bold;")
        self.progress_speed.setVisible(False)
        progress_info.addWidget(self.progress_speed)

        self.progress_eta = QLabel("")
        self.progress_eta.setStyleSheet("color: #aaa; font-size: 13px;")
        self.progress_eta.setVisible(False)
        progress_info.addWidget(self.progress_eta)

        self.progress_size = QLabel("")
        self.progress_size.setStyleSheet("color: #aaa; font-size: 13px;")
        self.progress_size.setVisible(False)
        progress_info.addWidget(self.progress_size)

        progress_info.addStretch()
        layout.addLayout(progress_info)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #888; font-size: 13px;")
        layout.addWidget(self.status_label)

        layout.addStretch()

    def _build_history_tab(self, parent):
        layout = QVBoxLayout(parent)
        layout.setSpacing(10)

        btn_row = QHBoxLayout()
        clear_btn = QPushButton("Очистить историю")
        clear_btn.setObjectName("secondary")
        clear_btn.clicked.connect(self._clear_history)
        btn_row.addStretch()
        btn_row.addWidget(clear_btn)
        layout.addLayout(btn_row)

        self.history_table = QTableWidget(0, 5)
        self.history_table.setHorizontalHeaderLabels(["Название", "Формат", "Качество", "Дата", "Файл"])
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.doubleClicked.connect(self._open_history_file)
        layout.addWidget(self.history_table)

    def _build_settings_tab(self, parent):
        layout = QVBoxLayout(parent)
        layout.setSpacing(12)

        dir_group = QGroupBox("Папка загрузки по умолчанию")
        dir_layout = QHBoxLayout(dir_group)
        self.settings_dir_label = QLabel(self.output_dir)
        self.settings_dir_label.setWordWrap(True)
        self.settings_dir_label.setStyleSheet("color: #aaa;")
        dir_layout.addWidget(self.settings_dir_label, 1)
        change_btn = QPushButton("Изменить")
        change_btn.setObjectName("secondary")
        change_btn.clicked.connect(self._browse_dir)
        dir_layout.addWidget(change_btn)
        layout.addWidget(dir_group)

        about_group = QGroupBox("О программе")
        about_layout = QVBoxLayout(about_group)
        about_text = QLabel(
            "OpenTube — десктопное приложение для загрузки\n"
            "видео и аудио с YouTube.\n\n"
            "Технологии: yt-dlp + PyQt6 + FFmpeg\n"
            "Версия: 1.0.0"
        )
        about_text.setStyleSheet("color: #ccc; font-size: 14px;")
        about_layout.addWidget(about_text)
        layout.addWidget(about_group)

        layout.addStretch()

    def _fetch_info(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Предупреждение", "Введите ссылку на видео.")
            return

        self.fetch_btn.setEnabled(False)
        self.download_btn.setEnabled(False)
        self.format_combo.clear()
        self.format_combo.setEnabled(False)
        self.status_label.setText("Получение информации о видео...")
        self.info_title.setText("Название: ...")
        self.info_uploader.setText("Канал: ...")
        self.info_duration.setText("Длительность: ...")
        self.info_views.setText("Просмотры: ...")

        self.info_fetcher = InfoFetcher(url)
        self.info_fetcher.finished.connect(self._on_info_fetched)
        self.info_fetcher.error.connect(self._on_info_error)
        self.info_fetcher.start()

    def _on_info_fetched(self, video_info: VideoInfo):
        self.current_video_info = video_info
        self.fetch_btn.setEnabled(True)
        self.status_label.setText("")

        self.info_title.setText(f"Название: {video_info.title}")
        self.info_uploader.setText(f"Канал: {video_info.uploader}")
        self.info_duration.setText(f"Длительность: {_format_duration(video_info.duration)}")

        views = video_info.view_count
        if views > 0:
            self.info_views.setText(f"Просмотры: {views:,}".replace(",", " "))
        else:
            self.info_views.setText("Просмотры: —")

        if video_info.thumbnail:
            self.thumbnail_label.setText("")
            self.thumbnail_loader = ThumbnailLoader(video_info.thumbnail)
            self.thumbnail_loader.finished.connect(self._on_thumbnail_loaded)
            self.thumbnail_loader.start()

        self.format_combo.clear()
        for q in video_info.qualities:
            self.format_combo.addItem(q.label, q)
        self.format_combo.setEnabled(True)
        self.download_btn.setEnabled(True)

    def _on_info_error(self, err: str):
        self.fetch_btn.setEnabled(True)
        self.status_label.setText("")
        self.info_title.setText("Название: —")
        self.info_uploader.setText("Канал: —")
        self.info_duration.setText("Длительность: —")
        self.info_views.setText("Просмотры: —")
        QMessageBox.critical(self, "Ошибка", f"Не удалось получить информацию:\n{err}")

    def _on_thumbnail_loaded(self, pixmap: QPixmap):
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                320, 180, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.thumbnail_label.setPixmap(scaled)

    def _on_audio_only_toggled(self, checked: bool):
        self.format_combo.setEnabled(not checked)

    def _browse_dir(self):
        d = QFileDialog.getExistingDirectory(self, "Выберите папку загрузки", self.output_dir)
        if d:
            self.output_dir = d
            self.dir_label.setText(d)
            self.settings_dir_label.setText(d)

    def _start_download(self):
        if not self.current_video_info:
            return

        audio_only = self.audio_only_check.isChecked()
        format_string = ""
        if not audio_only:
            q: QualityOption | None = self.format_combo.currentData()
            if not q:
                QMessageBox.warning(self, "Предупреждение", "Выберите качество.")
                return
            format_string = q.format_string

        audio_quality = self.audio_quality_combo.currentText().replace(" kbps", "")

        self.download_btn.setEnabled(False)
        self.fetch_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_speed.setVisible(True)
        self.progress_eta.setVisible(True)
        self.progress_size.setVisible(True)
        self.status_label.setText("Начало загрузки...")

        self.downloader = Downloader(
            url=self.current_video_info.url,
            format_string=format_string,
            output_dir=self.output_dir,
            audio_only=audio_only,
            audio_quality=audio_quality,
        )
        self.downloader.progress.connect(self._on_download_progress)
        self.downloader.postprocessing.connect(self._on_postprocessing)
        self.downloader.finished.connect(self._on_download_finished)
        self.downloader.error.connect(self._on_download_error)
        self.downloader.start()

    def _on_download_progress(self, percent: float, speed: str, eta: str, size_info: str, phase: str):
        if phase == "merging":
            self.progress_bar.setValue(100)
            self.progress_speed.setText("Объединение...")
            self.progress_eta.setText("")
            self.progress_size.setText("")
            self.status_label.setText("Объединение видео и аудио потоков...")
            return

        self.progress_bar.setValue(int(percent))
        self.progress_speed.setText(f"{percent:.1f}%")
        self.progress_eta.setText(f"Скорость: {speed}")
        self.progress_size.setText(f"Размер: {size_info}  |  Осталось: {eta}" if size_info else f"Осталось: {eta}")
        self.status_label.setText("Загрузка...")

    def _on_postprocessing(self, text: str):
        if text:
            self.progress_bar.setValue(100)
            self.progress_speed.setText(text)
            self.progress_eta.setText("")
            self.progress_size.setText("")
            self.status_label.setText(text)
        else:
            self.progress_speed.setText("")

    def _on_download_finished(self, filepath: str, title: str):
        self.progress_bar.setValue(100)
        self.progress_speed.setText("Готово!")
        self.progress_eta.setText("")
        self.progress_size.setText("")
        self.status_label.setText(f"Сохранено: {filepath}")
        self.download_btn.setEnabled(True)
        self.fetch_btn.setEnabled(True)

        fmt_str = "MP3 (audio)" if self.audio_only_check.isChecked() else "MP4 (video)"
        if self.audio_only_check.isChecked():
            quality = self.audio_quality_combo.currentText()
        else:
            q: QualityOption | None = self.format_combo.currentData()
            quality = q.label if q else "—"

        entry = HistoryEntry(
            url=self.current_video_info.url if self.current_video_info else "",
            title=title,
            format=fmt_str,
            quality=quality,
            filepath=filepath,
        )
        self.history.add(entry)
        self._refresh_history_table()

        QMessageBox.information(self, "Загрузка завершена", f"Файл сохранён:\n{filepath}")

    def _on_download_error(self, err: str):
        self.progress_bar.setVisible(False)
        self.progress_speed.setVisible(False)
        self.progress_eta.setVisible(False)
        self.progress_size.setVisible(False)
        self.status_label.setText(f"Ошибка: {err}")
        self.download_btn.setEnabled(True)
        self.fetch_btn.setEnabled(True)
        QMessageBox.critical(self, "Ошибка загрузки", err)

    def _refresh_history_table(self):
        self.history_table.setRowCount(0)
        for entry in self.history.entries:
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            self.history_table.setItem(row, 0, QTableWidgetItem(entry.title))
            self.history_table.setItem(row, 1, QTableWidgetItem(entry.format))
            self.history_table.setItem(row, 2, QTableWidgetItem(entry.quality))
            dt = datetime.fromtimestamp(entry.timestamp).strftime("%Y-%m-%d %H:%M")
            self.history_table.setItem(row, 3, QTableWidgetItem(dt))
            self.history_table.setItem(row, 4, QTableWidgetItem(entry.filepath))

    def _clear_history(self):
        reply = QMessageBox.question(
            self, "Очистка истории",
            "Удалить все записи из истории?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.history.clear()
            self._refresh_history_table()

    def _open_history_file(self, index):
        row = index.row()
        if 0 <= row < len(self.history.entries):
            filepath = self.history.entries[row].filepath
            if os.path.exists(filepath):
                QDesktopServices.openUrl(QUrl.fromLocalFile(filepath))
            else:
                QMessageBox.warning(self, "Файл не найден", f"Файл не существует:\n{filepath}")
