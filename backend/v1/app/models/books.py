"""Pydantic Classes for the Books Models"""
from datetime import date, datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


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
    NA = "N/A"


class BookStatus(Enum):
    AVAILABLE = "available"
    CHECKED_OUT = "checked_out"
    RESERVED = "reserved"


class BookRequest(BaseModel):
    title: str | None = Field(None, description="Title of the book")
    author: str | None = Field(None, description="Author of the book")
    genre: str | None = Field(None, description="Genre of the book")
    isbn: str | None = Field(None, description="International Standard Book Number")
    book_type: BookType | None = Field(None, 
                                       description="Type of the book (e.g., paperback, ebook)")

    @field_validator("isbn", mode="before")
    @classmethod
    def validate_isbn_length(cls, v):
        if v and len(v) not in [10, 13]:
            raise ValueError("ISBN must be either 10 or 13 characters long")
        return v
    
    @field_validator("isbn", mode="before")
    @classmethod
    def validate_isbn_format(cls, v):
        if v and not v.isdigit():
            raise ValueError("ISBN must contain only digits")
        return v
    
    model_config = ConfigDict(use_enum_values = True)


class BookInformation(BookRequest):
    book_uuid: str = Field(default_factory=lambda: str(uuid4()), 
                           description="Unique identifier for the book")
    book_status: BookStatus = Field(description="Current status of the book")
    publisher: str | None = Field(None, description="Publisher of the book")
    publication_date: date | None = Field(None, description="Publication date of the book")
    shelf_location: str| None = Field(None, description="Location of the book in the library")
    total_pages: int | None = Field(None, description="Total number of pages in the book")
    file_format: EBookType = Field(None,
                                   description="Format of the softcopy book, e.g., 'PDF', 'EPUB'")
    available_copies: int = Field(ge=0, description="Number of copies available for borrowing")
    tags: list[str] = Field(default_factory=list, 
                            description="Tags for categorization or searching")
    description: str | None = Field(None, description="Brief summary of the book")

    @field_validator("publication_date", mode="after")
    @classmethod
    def convert_date_to_datetime(cls, v):
        return datetime.combine(v, datetime.min.time())

    model_config = ConfigDict(use_enum_values = True)


class BookResponse(BaseModel):
    results: list[BookInformation]
    total_count: int = Field(description="Total number of matching books returned by the search")

    @field_validator("results", mode="before")
    @classmethod
    def validate_results(cls, v):
        if not isinstance(v, list):
            raise ValueError("Results must be a list")
        return v
