"""Pydantic Classes for the Books Models"""

from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class BookFormat(Enum):
    """Enum Class describing the Book Format."""
    HARDCOVER = "hardcover"
    EBOOK = "ebook"
    AUDIOBOOK = "audiobook"


class BookAudience(Enum):
    """Enum Class describing the Book Audience."""
    ADULT = "adult"
    YOUNG_ADULT = "young_adult"
    CHILDREN = "children"


class EBookType(Enum):
    """Enum Class describing the EBook Type."""
    PDF = "pdf"
    EPUB = "epub"
    MOBI = "mobi"
    AZW = "azw"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    RTF = "rtf"


class BookLanguage(Enum):
    """Enum Class describing the Language the Book is Written."""
    ENGLISH = "english"
    FRENCH = "french"
    SPANISH = "spanish"
    CHINESE = "chinese"


class BookCreateCondition(Enum):
    """Enum Class describing the Book Condition at Entry  into the Library."""
    NEW = "new"
    GOOD = "good"
    FAIR = "fair"


class BookUpdateCondition(Enum):
    """Enum Class describing the Book Condition when Updated."""
    DAMAGED = "damaged"
    LOST = "lost"


class BookCondition(Enum):
    """Enum Class describing all Possible Book Conditions."""
    NEW = "new"
    GOOD = "good"
    FAIR = "fair"
    DAMAGED = "damaged"
    LOST = "lost"


class BookLocation(Enum):
    """Enum Class describing the Book's Location."""
    MAIN = "main"
    BRANCH1 = "branch1"
    BRANCH2 = "branch2"


class BookCreate(BaseModel):
    """Pydantic Model to Create a Book in the Database."""
    title: str = Field(min_length=1, max_length=200)
    author_first_name: str = Field(min_length=2, max_length=100)
    author_middle_name: str | None = Field(None, min_length=2, max_length=100)
    author_last_name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = Field(None, max_length=1000)
    language: BookLanguage
    book_type: BookFormat
    ebook_type: EBookType | None = Field(None)
    hardcover_condition: BookCreateCondition | None = Field(None)
    publisher: str | None = Field(None, max_length=100)
    edition: int| None = Field(None, ge=1)
    page_count: int = Field(ge=1)
    tags: list[str] | None = Field(None, max_length=10)
    isbn: str | None = Field(None, pattern=r"^(?:\d{10}|\d{13})$")
    genre: str | None = Field(None, max_length=50)
    publication_year: date | None
    target_audience: BookAudience
    location: BookLocation
    replacement_cost: float | None = Field(None, ge=0.0)

    @model_validator(mode="after")
    def check_ebook_type_required(self):
        if self.book_type == BookFormat.EBOOK and self.ebook_type is None:
            raise ValueError("ebook_type must be specified when book_type is 'ebook'")
        return self
    
    @model_validator(mode="after")
    def check_paperback_condition(self):
        if self.book_type == BookFormat.HARDCOVER and self.hardcover_condition is None:
            raise ValueError("hardcover condition must be specified when book_type is 'ebook'")
        return self


class BookResponse(BookCreate):
    """Pydantic Model to Return Book Creation Response."""
    book_id: UUID = Field(
        description="Unique identifier for the book in the database.")
    book_entry_time: datetime = Field(
        description="Timestamp when the book record was first created.")
    last_updated_date: datetime = Field(
        description="Timestamp of the last modification to the book record.")


class BookUpdate(BaseModel):
    """Pydantic Model to Update a Book in the Database."""
    title: str | None = Field(None, min_length=1, max_length=200,
                              description="Update title.")
    description: str | None = Field(None, max_length=1000, 
                                    description="Update description.")
    publisher: str | None = Field(None, max_length=100,
                                  description="Update publisher.")
    edition: int | None = Field(None, ge=1,
                                description="Update edition number.")
    page_count: int | None = Field(None, ge=1,
                                   description="Update page count.")
    tags: list[str] | None = Field(None, max_length=10,
                                   description="Update list of tags.")
    isbn: str | None = Field(None, pattern=r"^(?:\d{10}|\d{13})$",
                             description="Update ISBN. Must be unique if provided.")
    genre: str | None = Field(None, max_length=50,
                              description="Update genre.")
    publication_year: date | None = Field(None,
                                          description="Update publication year.")
    target_audience: BookAudience | None = Field(None,
                                                 description="Update target audience.")
    location: BookLocation | None = Field(None,
                                          description="Update storage location.")
    replacement_cost: float | None = Field(None, ge=0.0, 
                                           description="Update replacement cost.")
    ebook_type: EBookType | None = Field(None, description="Update ebook type.")
    hardcover_condition: BookCreateCondition | None = Field(None,
                            description="Update hardcover/hardcover condition.")
