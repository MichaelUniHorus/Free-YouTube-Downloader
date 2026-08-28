<div align="center">

# OpenTube

*Free, ad-free, open-source YouTube Downloader*

[Русский](#русский) | [English](#english)

[![Release](https://img.shields.io/github/v/release/MichaelUniHorus/Free-YouTube-Downloader?color=e94560&style=for-the-badge)](https://github.com/MichaelUniHorus/Free-YouTube-Downloader/releases/latest)
[![License](https://img.shields.io/badge/License-MIT-0f3460?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-16213e?style=for-the-badge)](https://python.org)
[![Build](https://img.shields.io/badge/build-no%20CI%20yet-555?style=for-the-badge)](#)
[![Codecov](https://img.shields.io/badge/codecov-not%20configured-555?style=for-the-badge)](#)
[![Downloads](https://img.shields.io/github/downloads/MichaelUniHorus/Free-YouTube-Downloader/total?color=e94560&style=for-the-badge)](https://github.com/MichaelUniHorus/Free-YouTube-Downloader/releases)

</div>

---

## Русский

<a name="русский"></a>
<!-- ====== Русский ====== -->

### Содержание

- [О проекте](#ru-about)
- [Описание](#ru-description)
- [Возможности](#ru-features)
- [Установка](#ru-installation)
- [Использование](#ru-usage)
- [Конфигурация](#ru-config)
- [Структура проекта](#ru-structure)
- [Разработка](#ru-development)
- [Участие в проекте](#ru-contributing)
- [Лицензия](#ru-license)

<a name="ru-about"></a>
<!-- ====== О проекте ====== -->

### О проекте

OpenTube создан как простой, бесплатный и безопасный инструмент для загрузки контента с YouTube. Никаких аккаунтов, рекламы или платных функций.

<a name="ru-description"></a>
<!-- ====== Описание ====== -->

### Описание

OpenTube -- это бесплатное десктопное приложение для загрузки видео и аудио с YouTube. Скачивайте контент в разных качествах, конвертируйте звук в MP3 и управляйте историей загрузок в одном окне.

Приложение полностью бесплатное, без рекламы и с открытым исходным кодом.

> В портативную сборку уже включён FFmpeg. При запуске из исходников FFmpeg необходимо установить отдельно.

<a name="ru-features"></a>
<!-- ====== Возможности ====== -->

### Возможности

- Загрузка видео с выбором качества от 144p до 4K и выше.
- Извлечение MP3 с выбором битрейта: 128 / 192 / 256 / 320 kbps.
- Предварительный просмотр обложки, названия, канала и длительности.
- Индикатор загрузки со скоростью, оставшимся временем и размером.
- История загруженных файлов с возможностью быстрого открытия.
- Современный тёмный интерфейс на PyQt6.

<a name="ru-installation"></a>
<!-- ====== Установка ====== -->

### Установка

#### Готовая сборка

1. Откройте [Releases](https://github.com/MichaelUniHorus/Free-YouTube-Downloader/releases/latest).
2. Скачайте `OpenTube-v1.0.1.zip`.
3. Распакуйте и запустите `OpenTube.exe`.

#### Из исходников

```bash
git clone https://github.com/MichaelUniHorus/Free-YouTube-Downloader.git
cd Free-YouTube-Downloader
pip install -r requirements.txt
```

Установите FFmpeg:

```bash
winget install Gyan.FFmpeg
```

<a name="ru-usage"></a>
<!-- ====== Использование ====== -->

### Использование

Запуск из исходников:

```bash
python main.py
```

1. Вставьте ссылку на YouTube видео.
2. Нажмите **Информация** для получения метаданных.
3. Выберите **качество видео** или включите **Только аудио (MP3)**.
4. Укажите папку сохранения.
5. Нажмите **Скачать**.

<a name="ru-config"></a>
<!-- ====== Конфигурация ====== -->

### Конфигурация

| Параметр | Значение по умолчанию | Описание |
| --- | --- | --- |
| `download_dir` | `~/Downloads/OpenTube` | Папка для сохранения файлов |
| `audio_bitrate` | `192 kbps` | Битрейт MP3 при аудио-режиме |
| `video_quality` | `best` | Выбранное качество видео |
| `history_file` | `~/.opentube/history.json` | Файл истории загрузок |

<a name="ru-structure"></a>
<!-- ====== Структура ====== -->

### Структура проекта

```
Free-YouTube-Downloader/
+-- main.py
+-- requirements.txt
+-- README.md
+-- LICENSE
+-- .gitignore
+-- opentube/
    +-- __init__.py
    +-- main_window.py
    +-- downloader.py
    +-- history.py
```

<a name="ru-development"></a>
<!-- ====== Разработка ====== -->

### Разработка

Для проверки стиля и типов используйте:

```bash
pytest tests/
ruff check opentube
mypy opentube
```

> В данный момент тесты и линтеры не настроены. Раздел добавлен как <PLACEHOLDER>.

<a name="ru-contributing"></a>
<!-- ====== Участие ====== -->

### Участие в проекте

1. Форкните репозиторий.
2. Создайте ветку для изменений.
3. Внесите правки и обновите README при необходимости.
4. Откройте Pull Request.

<a name="ru-license"></a>
<!-- ====== Лицензия ====== -->

### Лицензия

Проект распространяется под лицензией MIT. Подробнее в файле [LICENSE](LICENSE).

---

## English

<a name="english"></a>
<!-- ====== English ====== -->

### Table of Contents

- [About](#en-about)
- [Description](#en-description)
- [Features](#en-features)
- [Installation](#en-installation)
- [Usage](#en-usage)
- [Configuration](#en-config)
- [Project Structure](#en-structure)
- [Development](#en-development)
- [Contributing](#en-contributing)
- [License](#en-license)

<a name="en-about"></a>
<!-- ====== About ====== -->

### About

OpenTube was built as a simple, free, and safe tool for downloading YouTube content. No accounts, no ads, no paid features.

<a name="en-description"></a>
<!-- ====== Description ====== -->

### Description

OpenTube is a free desktop application for downloading YouTube videos and audio. Download content in different qualities, convert sound to MP3, and manage your download history in a single window.

The application is completely free, ad-free, and open-source.

> FFmpeg is bundled in the portable build. For source installation, install FFmpeg separately.

<a name="en-features"></a>
<!-- ====== Features ====== -->

### Features

- Download video from 144p up to 4K and higher.
- Extract MP3 with bitrate choice: 128 / 192 / 256 / 320 kbps.
- Preview thumbnail, title, channel, and duration.
- Progress bar with speed, remaining time, and file size.
- Download history with quick file opening.
- Modern dark UI built with PyQt6.

<a name="en-installation"></a>
<!-- ====== Installation ====== -->

### Installation

#### Ready-to-use build

1. Go to [Releases](https://github.com/MichaelUniHorus/Free-YouTube-Downloader/releases/latest).
2. Download `OpenTube-v1.0.1.zip`.
3. Extract and run `OpenTube.exe`.

#### From source

```bash
git clone https://github.com/MichaelUniHorus/Free-YouTube-Downloader.git
cd Free-YouTube-Downloader
pip install -r requirements.txt
```

Install FFmpeg:

```bash
winget install Gyan.FFmpeg
```

<a name="en-usage"></a>
<!-- ====== Usage ====== -->

### Usage

Run from source:

```bash
python main.py
```

1. Paste a YouTube video link.
2. Click **Information** to fetch metadata.
3. Choose **video quality** or enable **Audio only (MP3)**.
4. Set the save folder.
5. Click **Download**.

<a name="en-config"></a>
<!-- ====== Configuration ====== -->

### Configuration

| Parameter | Default | Description |
| --- | --- | --- |
| `download_dir` | `~/Downloads/OpenTube` | Output directory for downloads |
| `audio_bitrate` | `192 kbps` | MP3 bitrate for audio-only mode |
| `video_quality` | `best` | Selected video quality |
| `history_file` | `~/.opentube/history.json` | Download history file path |

<a name="en-structure"></a>
<!-- ====== Structure ====== -->

### Project Structure

```
Free-YouTube-Downloader/
+-- main.py
+-- requirements.txt
+-- README.md
+-- LICENSE
+-- .gitignore
+-- opentube/
    +-- __init__.py
    +-- main_window.py
    +-- downloader.py
    +-- history.py
```

<a name="en-development"></a>
<!-- ====== Development ====== -->

### Development

To run style and type checks:

```bash
pytest tests/
ruff check opentube
mypy opentube
```

> Tests and linters are not configured yet. This section is a <PLACEHOLDER>.

<a name="en-contributing"></a>
<!-- ====== Contributing ====== -->

### Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make changes and update the README if needed.
4. Open a Pull Request.

<a name="en-license"></a>
<!-- ====== License ====== -->

### License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

<p align="center">
  Created by <a href="https://github.com/MichaelUniHorus">Michael Prolubnikov</a>
  <br>
  <a href="https://github.com/MichaelUniHorus/Free-YouTube-Downloader">Free-YouTube-Downloader</a>
</p>
