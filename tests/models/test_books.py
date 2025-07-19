"""Tests for the Books Model Module."""

import pytest

from backend.v1.app.models.books import BookType


@pytest.mark.unit
def test_booktype_members():
    """
    Test that all expected members are present in the BookType enum.
    """
    assert BookType.PAPERBACK is not None
    assert BookType.EBOOK is not None
    assert BookType.AUDIOBOOK is not None


@pytest.mark.unit
def test_booktype_values():
    """
    Test that the values of the BookType enum members are correct.
    """
    assert BookType.PAPERBACK.value == "paperback"
    assert BookType.EBOOK.value == "ebook"
    assert BookType.AUDIOBOOK.value == "audiobook"


@pytest.mark.unit
def test_booktype_type():
    """
    Test that the type of the BookType members is BookType.
    """
    assert isinstance(BookType.PAPERBACK, BookType)
    assert isinstance(BookType.EBOOK, BookType)
    assert isinstance(BookType.AUDIOBOOK, BookType)


@pytest.mark.unit
def test_booktype_string_representation():
    """
    Test the string representation of BookType enum members.
    """
    assert str(BookType.PAPERBACK) == "BookType.PAPERBACK"
    assert str(BookType.EBOOK) == "BookType.EBOOK"
    assert str(BookType.AUDIOBOOK) == "BookType.AUDIOBOOK"


@pytest.mark.unit
def test_booktype_equality():
    """
    Test equality comparisons between BookType enum members.
    """
    assert BookType.PAPERBACK == BookType.PAPERBACK
    assert BookType.PAPERBACK != BookType.EBOOK
    assert BookType.EBOOK == BookType.EBOOK
    assert BookType.AUDIOBOOK == BookType.AUDIOBOOK


@pytest.mark.unit
def test_booktype_from_value():
    """
    Test getting a BookType member from its value.
    """
    assert BookType("paperback") == BookType.PAPERBACK
    assert BookType("ebook") == BookType.EBOOK
    assert BookType("audiobook") == BookType.AUDIOBOOK


@pytest.mark.unit
def test_booktype_invalid_value():
    """
    Test that creating a BookType from an invalid value raises a ValueError.
    """
    with pytest.raises(ValueError):
        BookType("invalid_type")


@pytest.mark.unit
def test_booktype_iteration():
    """
    Test that BookType can be iterated over and contains all members.
    """
    members = list(BookType)
    assert len(members) == 3
    assert BookType.PAPERBACK in members
    assert BookType.EBOOK in members
    assert BookType.AUDIOBOOK in members
