"""Pydantic Classes for the Books Models"""

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class BookType(Enum):
    PAPERBACK = "paperback"
    EBOOK = "ebook"
    AUDIOBOOK = "audiobook"


class EBookType(Enum):
    PDF = "pdf"
    EPUB = "epub"
    MOBI = "mobi"
    AZW = "azw"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    RTF = "rtf"


class BookStatus(Enum):
    AVAILABLE = "available"
    CHECKED_OUT = "checked_out"
    RESERVED = "reserved"


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(None, max_length=1000)
    book_type: BookType = BookType.PAPERBACK
    ebook_type: EBookType | None
    status: BookStatus = BookStatus.AVAILABLE
    published_date: date | None
    isbn: str | None
    genre: str | None = Field(None, max_length=50)
    language: str | None = Field(None, max_length=30)

    @model_validator(mode="after")
    def check_ebook_type_required(self):
        if self.book_type == BookType.EBOOK and self.ebook_type is None:
            raise ValueError("ebook_type must be specified when book_type is 'ebook'")
        return self


class BookCreate(BookBase):
    title: str
    author: str


class BookUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    author: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = Field(None, max_length=1000)
    book_type: BookType | None
    ebook_type: EBookType | None
    status: BookStatus | None
    published_date: date | None
    isbn: str | None
    genre: str | None = Field(None, max_length=50)
    language: str | None = Field(None, max_length=30)
