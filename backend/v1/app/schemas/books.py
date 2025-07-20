"""Books Table Schema."""

from datetime import date, datetime
from enum import Enum
from uuid import UUID

from sqlmodel import Column, Field, SQLModel
from sqlmodel import Enum as SQLModelEnum

from backend.v1.app.models.books import (
    BookAudience,
    BookCondition,
    BookFormat,
    BookLanguage,
    BookLocation,
    EBookType,
)


class CirculationStatus(Enum):
    AVAILABLE = "available"
    CHECKED_OUT = "checked_out"
    RESERVED = "reserved"
    ON_HOLD = "on_hold"
    DAMAGED = "damaged"
    LOST = "lost"
    ARCHIVED = "archived"


class Books(SQLModel, table=True):
    """Books Table Class."""
    book_id: UUID = Field(unique=True, nullable=False, primary_key=True)
    title: str = Field(nullable=False, unique=False)
    author_first_name: str = Field(max_length=100,
                                   nullable=False)
    author_middle_name: str | None = Field(default=None, max_length=100,
                                           nullable=True)
    author_last_name: str | None = Field(default=None, max_length=100,
                                         nullable=True)
    description: str | None = Field(default=None, max_length=1000,
                                    nullable=True)
    language: BookLanguage = Field(
        sa_column=Column(SQLModelEnum(BookLanguage), nullable=False)
    )
    book_type: BookFormat = Field(
        sa_column=Column(SQLModelEnum(BookFormat), nullable=False)
    )
    ebook_type: EBookType | None = Field(
        sa_column=Column(SQLModelEnum(EBookType), nullable=True)
    )
    hardcover_condition: BookCondition | None = Field(
        sa_column=Column(SQLModelEnum(BookCondition), nullable=True)
    )
    publisher: str | None = Field(default=None, nullable=True)
    edition: int 
    page_count: int | None = Field(default=None, nullable=True)
    tags: list[str] | None = Field(default=None, nullable=True)
    isbn: str | None = Field(default=None, nullable=False)
    genre: str | None = Field(default=None)
    publication_year: date | None = Field(default=None)
    target_audience: BookAudience = Field(
        sa_column=Column(SQLModelEnum(BookAudience), nullable=False)
    )
    location: BookLocation = Field(
        sa_column=Column(SQLModelEnum(BookLocation), nullable=False)
    )
    replacement_cost: float | None = Field(default=None)
    last_access_time: datetime | None = Field(default=None)
    book_entry_time: datetime
    last_updated_date: datetime
