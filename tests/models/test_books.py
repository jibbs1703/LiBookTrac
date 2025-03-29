from datetime import date

import pytest
from pydantic import ValidationError

from app.models.books import BookInformation, BookResponse


def test_valid_book_information():
    BookInformation(
        title="Test Book",
        author="Test Author",
        genre="Test Genre",
        isbn="1234567890123",
        book_type="paperback",
        book_status="available",
        publisher="Test Publisher",
        publication_date=date(2023, 1, 1),
        shelf_location="Shelf A1",
        total_pages=200,
        file_format="pdf",
        available_copies=10,
        tags=["fiction", "test"],
        description="A test book description."
    )
    assert True


def test_invalid_isbn():
    with pytest.raises(ValidationError):
        BookInformation(
            title="Invalid ISBN Book",
            author="Test Author",
            genre="Test Genre",
            isbn="invalid_isbn",
            book_type="paperback",
            book_status="available",
            publication_date=date(2023, 1, 1),
            available_copies=5
        )


def test_default_uuid_generation():
    book = BookInformation(
        title="UUID Test Book",
        author="Test Author",
        book_type="ebook",
        book_status="available",
        publication_date=date(2023, 1, 1),
        available_copies=5
    )
    assert book.book_uuid is not None
    assert len(book.book_uuid) > 0
    assert isinstance(book.book_uuid, str)
    assert len(book.book_uuid) == 36
    assert book.book_uuid.count('-') == 4


def test_convert_date_to_datetime():
    book = BookInformation(
        title="Date Conversion Test",
        author="Test Author",
        book_type="paperback",
        book_status="available",
        publication_date=date(2023, 1, 1),
        available_copies=5
    )
    assert book.publication_date.year == 2023
    assert book.publication_date.month == 1
    assert book.publication_date.day == 1


def test_invalid_available_copies():
    with pytest.raises(ValidationError):
        BookInformation(
            title="Negative Copies Book",
            author="Test Author",
            book_type="paperback",
            book_status="available",
            publication_date=date(2023, 1, 1),
            available_copies=-5
        )


def test_book_response():
    book = BookInformation(
        title="Test Book",
        author="Test Author",
        genre="Test Genre",
        isbn="1234567890123",
        book_type="paperback",
        book_status="available",
        publisher="Test Publisher",
        publication_date=date(2023, 1, 1),
        shelf_location="Shelf A1",
        total_pages=200,
        file_format="pdf",
        available_copies=10,
        tags=["fiction", "test"],
        description="A test book description."
    )
    response = BookResponse(
        results=[book],
        total_count=1
    )
    assert response.total_count == 1
    assert response.results[0].title == "Test Book"
    assert isinstance(response.results, list)