import schedule
import time
import requests
from bs4 import BeautifulSoup
import os


def get_book_data(url):
    """
    Получает полную информацию о книге с веб-страницы.

    Функция парсит страницу книги и извлекает все основные данные:
    название, цену, рейтинг, наличие, описание и технические характеристики.

    Args:
        url (str): URL-адрес страницы с книгой

    Returns:
        dict: Словарь с данными о книге, содержащий следующие ключи:
            - 'title' (str): Название книги
            - 'price' (str): Цена книги
            - 'rating' (str): Рейтинг книги (One-Five)
            - 'availability' (str): Информация о наличии
            - 'description' (str): Описание книги
            - 'product_info' (dict): Словарь с техническими характеристиками из таблицы
    """
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Failed to fetch page. Status code: {response.status_code}"}

    soup = BeautifulSoup(response.text, "html.parser")
    book_data = {}

    title_element = soup.find("h1")
    book_data['title'] = title_element.text.strip() if title_element else "Not found"

    price_element = soup.find("p", class_="price_color")
    book_data['price'] = price_element.text.strip() if price_element else "Not found"

    rating_element = soup.find("p", class_="star-rating")
    if rating_element:
        book_data['rating'] = rating_element["class"][1]
    else:
        book_data['rating'] = "Not found"

    availability_element = soup.find("p", class_="instock")
    book_data['availability'] = availability_element.text.strip() if availability_element else "Not found"

    description_header = soup.find("div", id="product_description")
    if description_header:
        description_element = description_header.find_next_sibling("p")
        book_data['description'] = description_element.text.strip() if description_element else "Not found"
    else:
        book_data['description'] = "Not found"

    product_table = soup.find("table", class_="table-striped")
    book_data['product_info'] = {}

    if product_table:
        rows = product_table.find_all("tr")
        for row in rows:
            header = row.find("th")
            value = row.find("td")
            if header and value:
                book_data['product_info'][header.text.strip()] = value.text.strip()

    return book_data


def scrape_books(save_to_file=False, max_pages=None, delay=0.5):
    """
    Парсит все страницы каталога books.toscrape.com
    и возвращает список данных о книгах.

    Args:
        save_to_file (bool): Сохранять ли данные в файл
        max_pages (int): Максимальное количество страниц для парсинга
        delay (float): Задержка между запросами в секундах
    """
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    all_books = []
    page_number = 1

    print(" Начало парсинга всех страниц...")

    while True:
        if max_pages and page_number > max_pages:
            print(f" Достигнут лимит в {max_pages} страниц")
            break

        url = base_url.format(page_number)
        response = requests.get(url)

        if response.status_code != 200:
            print(f"✅ Парсинг завершён. Страниц обработано: {page_number - 1}")
            break

        print(f" Обработка страницы {page_number}...")

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.select("h3 a")

        if not books:
            print(" Больше книг не найдено.")
            break

        books_count = 0
        for book in books:
            relative_link = book.get("href")
            if relative_link.startswith("../"):
                relative_link = relative_link.replace("../", "")
            book_url = f"http://books.toscrape.com/catalogue/{relative_link}"

            book_data = get_book_data(book_url)
            all_books.append(book_data)
            books_count += 1
            time.sleep(delay)

        print(f" На странице {page_number} обработано {books_count} книг")
        page_number += 1

    if save_to_file:
        artifacts_dir = "artifacts"
        os.makedirs(artifacts_dir, exist_ok=True)

        file_path = os.path.join(artifacts_dir, "books_data.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            for book in all_books:
                f.write(str(book) + "\n\n")

        print(f" Данные сохранены в файл: {file_path}")
        print(f" Всего собрано данных о {len(all_books)} книгах с {page_number - 1} страниц")

    return all_books


def job():
    """
    Функция, запускает парсинг и сохранение данных каждый день в 19:00.
    """
    print("Запуск парсинга...")

    scrape_books(save_to_file=True, max_pages=3, delay=0.3)

    print("✅ Парсинг завершён и данные сохранены.")


schedule.every().day.at("20:05").do(job)

print("Планировщик запущен. Ожидаем запуск задачи...")
print("Для остановки нажмите Ctrl+C")

try:
    while True:
        schedule.run_pending()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n🛑 Планировщик остановлен пользователем")
