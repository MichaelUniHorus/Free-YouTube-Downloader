<div align="center">

# OpenTube

**Free YouTube Downloader**

[English](README.en.md) | **Русский**

[![Release](https://img.shields.io/github/v/release/MichaelUniHorus/Free-YouTube-Downloader?color=e94560&style=for-the-badge)](https://github.com/MichaelUniHorus/Free-YouTube-Downloader/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.10%2B-16213e?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-0f3460?style=for-the-badge)](LICENSE)

</div>

---

## О проекте

OpenTube — это бесплатное десктопное приложение для загрузки видео и аудио с YouTube. Скачивайте контент в разных качествах, конвертируйте звук в MP3 и управляйте историей загрузок в одном окне.

---

## Возможности

| Возможность | Описание |
| --- | --- |
| Видео | Загрузка с выбором качества от 144p до 4K и выше |
| Аудио | Извлечение MP3 с выбором битрейта: 128/192/256/320 kbps |
| Превью | Просмотр обложки, названия, канала и длительности |
| Прогресс | Индикатор загрузки, скорость, оставшееся время и размер |
| История | Список загруженных файлов с быстрым открытием |
| Интерфейс | Современный тёмный дизайн на PyQt6 |

---

## Скриншоты

> Раздел будет дополнен скриншотами интерфейса.

---

## Быстрый старт

### Скачать готовую сборку

1. Перейдите в [Releases](https://github.com/MichaelUniHorus/Free-YouTube-Downloader/releases/latest)
2. Скачайте `OpenTube-v1.0.1.zip`
3. Распакуйте и запустите `OpenTube.exe`

### Запуск из исходников

```bash
git clone https://github.com/MichaelUniHorus/Free-YouTube-Downloader.git
cd Free-YouTube-Downloader
pip install -r requirements.txt
python main.py
```

---

## Использование

1. Вставьте ссылку на YouTube видео.
2. Нажмите **Информация** для получения метаданных.
3. Выберите **качество видео** или включите **Только аудио (MP3)**.
4. Укажите папку сохранения.
5. Нажмите **Скачать**.

---

## Требования

- Windows 10/11
- Python 3.10+ (только для запуска из исходников)
- FFmpeg — уже включён в портативную сборку

---

## Технологии

- **PyQt6** — графический интерфейс
- **yt-dlp** — загрузка видео с YouTube
- **FFmpeg** — конвертация аудио и слияние потоков

---

## Лицензия

Проект распространяется под лицензией MIT. Подробнее в файле [LICENSE](LICENSE).
