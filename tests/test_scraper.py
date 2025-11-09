
import sys
import os
import pytest
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.scraper import get_book_data, scrape_books


def test_get_book_data_returns_dict_with_required_keys():
    """
    Тест 1: Проверяет, что get_book_data возвращает словарь с нужными ключами.
    """
    mock_html = """
    <html>
        <h1>Test Book Title</h1>
        <p class="price_color">£20.00</p>
        <p class="star-rating Three"></p>
        <p class="instock">In stock (5 available)</p>
        <div id="product_description"></div>
        <p>This is a tests book description for testing purposes.</p>
        <table class="table-striped">
            <tr><th>UPC</th><td>test123456789</td></tr>
            <tr><th>Product Type</th><td>Books</td></tr>
            <tr><th>Price (excl. tax)</th><td>£20.00</td></tr>
            <tr><th>Price (incl. tax)</th><td>£20.00</td></tr>
            <tr><th>Tax</th><td>£0.00</td></tr>
            <tr><th>Availability</th><td>In stock (5 available)</td></tr>
            <tr><th>Number of reviews</th><td>0</td></tr>
        </table>
    </html>
    """

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = mock_html

    with patch('src.scraper.requests.get', return_value=mock_response):
        result = get_book_data("http://test.com/book")

        assert isinstance(result, dict), "Функция должна возвращать словарь"

        expected_keys = ['title', 'price', 'rating', 'availability',
                         'description', 'product_info']

        for key in expected_keys:
            assert key in result, f"Отсутствует обязательный ключ: {key}"

        assert result['title'] == "Test Book Title"
        assert result['price'] == "£20.00"
        assert result['rating'] == "Three"
        assert "In stock" in result['availability']


def test_book_data_fields_have_correct_values():
    """
    Тест 2: Проверяет корректность значений полей книги.
    """
    mock_html = """
    <html>
        <h1>A Light in the Attic</h1>
        <p class="price_color">£51.77</p>
        <p class="star-rating Three"></p>
        <p class="instock">In stock (22 available)</p>
        <div id="product_description"></div>
        <p>It's hard to imagine a world without A Light in the Attic...</p>
        <table class="table-striped">
            <tr><th>UPC</th><td>a897fe39b1053632</td></tr>
            <tr><th>Product Type</th><td>Books</td></tr>
        </table>
    </html>
    """

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = mock_html

    with patch('src.scraper.requests.get', return_value=mock_response):
        result = get_book_data("http://test.com/book")

        assert result['title'] == "A Light in the Attic"
        assert result['price'] == "£51.77"
        assert result['rating'] == "Three"
        assert "In stock" in result['availability']
        assert "world without" in result['description']


def test_scrape_books_returns_list_of_books():
    """
    Тест 3: Проверяет, что scrape_books возвращает список книг.
    """
    mock_catalog_html = """
    <html>
        <h3><a href="../../book-one_001/index.html">Book One</a></h3>
        <h3><a href="../../book-two_002/index.html">Book Two</a></h3>
    </html>
    """

    mock_book_html = """
    <html>
        <h1>Test Book</h1>
        <p class="price_color">£15.00</p>
        <p class="star-rating Four"></p>
        <p class="instock">In stock</p>
    </html>
    """

    mock_catalog_response = Mock()
    mock_catalog_response.status_code = 200
    mock_catalog_response.text = mock_catalog_html

    mock_book_response = Mock()
    mock_book_response.status_code = 200
    mock_book_response.text = mock_book_html

    with patch('src.scraper.requests.get') as mock_get:
        def side_effect(url):
            if 'page-' in url:
                return mock_catalog_response
            else:
                return mock_book_response

        mock_get.side_effect = side_effect

        result = scrape_books(save_to_file=False, max_pages=1, delay=0)

        assert isinstance(result, list), "Должен возвращаться список"
        assert len(result) == 2, f"Ожидалось 2 книги, получено {len(result)}"

        for book in result:
            assert isinstance(book, dict), "Каждая книга должна быть словарем"
            assert 'title' in book, "Книга должна содержать название."


if __name__ == "__main__":
    pytest.main([__file__, "-v"])