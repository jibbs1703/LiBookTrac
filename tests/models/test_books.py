"""Tests for the Books Model Module."""

import pytest

from backend.v1.app.models.books import BookFormat


@pytest.mark.unit
def test_bookformat_members():
    """
    Test that all expected members are present in the Bookformat enum.
    """
    assert BookFormat.PAPERBACK is not None
    assert BookFormat.EBOOK is not None
    assert BookFormat.AUDIOBOOK is not None


@pytest.mark.unit
def test_bookformat_values():
    """
    Test that the values of the Bookformat enum members are correct.
    """
    assert BookFormat.PAPERBACK.value == "paperback"
    assert BookFormat.EBOOK.value == "ebook"
    assert BookFormat.AUDIOBOOK.value == "audiobook"


@pytest.mark.unit
def test_bookformat_type():
    """
    Test that the type of the Bookformat members is Bookformat.
    """
    assert isinstance(BookFormat.PAPERBACK, BookFormat)
    assert isinstance(BookFormat.EBOOK, BookFormat)
    assert isinstance(BookFormat.AUDIOBOOK, BookFormat)


@pytest.mark.unit
def test_bookformat_string_representation():
    """
    Test the string representation of BookFormat enum members.
    """
    assert str(BookFormat.PAPERBACK) == "BookFormat.PAPERBACK"
    assert str(BookFormat.EBOOK) == "BookFormat.EBOOK"
    assert str(BookFormat.AUDIOBOOK) == "BookFormat.AUDIOBOOK"


@pytest.mark.unit
def test_bookformat_equality():
    """
    Test equality comparisons between BookFormat enum members.
    """
    assert BookFormat.PAPERBACK == BookFormat.PAPERBACK
    assert BookFormat.PAPERBACK != BookFormat.EBOOK
    assert BookFormat.EBOOK == BookFormat.EBOOK
    assert BookFormat.AUDIOBOOK == BookFormat.AUDIOBOOK


@pytest.mark.unit
def test_bookformat_from_value():
    """
    Test getting a BookFormat member from its value.
    """
    assert BookFormat("paperback") == BookFormat.PAPERBACK
    assert BookFormat("ebook") == BookFormat.EBOOK
    assert BookFormat("audiobook") == BookFormat.AUDIOBOOK


@pytest.mark.unit
def test_bookformat_invalid_value():
    """
    Test that creating a Bookformat from an invalid value raises a ValueError.
    """
    with pytest.raises(ValueError):
        BookFormat("invalid_type")


@pytest.mark.unit
def test_bookformat_iteration():
    """
    Test that Bookformat can be iterated over and contains all members.
    """
    members = list(BookFormat)
    assert len(members) == 3
    assert BookFormat.PAPERBACK in members
    assert BookFormat.EBOOK in members
    assert BookFormat.AUDIOBOOK in members
