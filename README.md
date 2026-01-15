# Book Scraper Project

Проект для автоматического сбора данных о книгах с сайта books.toscrape.com. Включает в себя парсинг данных,
автоматическое расписание выполнения и сохранение результатов.

##  Структура проекта

book_scraper_project/

    ├── src
    │    └── scraper.py 
    ├── artifacts/ 
    │   └── books_data_*.txt 
    ├── tests/ 
    │   └── test_scraper.py 
    │── notebooks/ 
    │   └── HW_03_python_ds_2025.ipynb # Основной ноутбук с анализом
    ├── requirements.txt 
    ├── README.md 


##  Функциональность

### Основные возможности:

- **Парсинг данных о книгах**: название, цена, рейтинг, наличие, описание, технические характеристики
- **Автоматическое расписание**: ежедневный запуск в указанное время
- **Сохранение результатов**: автоматическое сохранение в текстовые файлы
- **Обработка ошибок**: устойчивость к сетевым ошибкам и изменениям структуры сайта

##  Установка и запуск

### 1. Клонирование и настройка

```bash
# Создайте папку проекта
mkdir book_scraper_project
cd book_scraper_project

# Создайте необходимые папки
mkdir artifacts tests notebooks
```

## 2. Установка зависимостей.

### Установка из файла requirements.txt:

```bash
pip install -r requirements.txt
```

### Альтернативная установка (если нет файла requirements.txt):

```bash
pip install requests beautifulsoup4 schedule
```

## 3. Запуск парсера

### Вариант 1: Однократный запуск (рекомендуется для тестирования)

```python
from src.scraper import scrape_books

# Быстрый тест - 2 страницы
books = scrape_books(save_to_file=True, max_pages=2)

# Полный парсинг всех страниц
books = scrape_books(save_to_file=True)
```

### Вариант 2: Прямой запуск из командной строки

```bash
# Запуск парсера напрямую
python scraper.py
```

##  Формат выходных данных

Данные сохраняются в папке `artifacts/` в формате txt.

##  Тестирование

Для запуска тестов:

```bash
python -m pytest tests/
```

Или конкретного тестового файла:

```bash
python tests/test_scraper.py
```

##  Используемые библиотеки

### Основные библиотеки:

```python
import requests
from bs4 import BeautifulSoup
import time
import schedule
import os
from datetime import datetime  
```

### Назначение каждой библиотеки:

- **`requests`** - отправка HTTP-запросов к сайту books.toscrape.com
- **`beautifulsoup4`** - парсинг HTML и извлечение данных со страниц
- **`schedule`** - автоматический запуск парсинга по расписанию
- **`time`** - задержки между запросами (`time.sleep()`)
- **`os`** - создание папки `artifacts` если её не существует
- **`datetime`** - добавление временных меток к данным
