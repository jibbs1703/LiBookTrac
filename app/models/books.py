import uuid
from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, field_validator


# Enum for book type
class BookType(Enum):
    HARD_COPY = "hard_copy"
    SOFT_COPY = "soft_copy"


# Base Book model with common fields
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Title of the book")
    author: str = Field(..., min_length=1, max_length=100, description="Author(s) of the book")
    publication_date: date = Field(..., description="Publication date of the book")
    isbn: str | None = Field(
        None, min_length=10, max_length=13, description="ISBN number (10 or 13 digits)"
    )
    book_type: BookType = Field(..., description="Type of book: hard_copy or soft_copy")

    @field_validator("publication_date")
    @classmethod
    def validate_publication_date(cls, v):
        today = date.today()
        if v > today:
            raise ValueError("Publication date cannot be in the future")
        return v

    @field_validator("isbn", pre=True, always=True)
    @classmethod
    def validate_isbn(cls, v):
        if v is None:
            return v
        # Remove any hyphens or spaces
        isbn_clean = "".join(filter(str.isdigit, v))
        if len(isbn_clean) not in (10, 13):
            raise ValueError("ISBN must be 10 or 13 digits")
        return isbn_clean

    class Config:
        orm_mode = True


# Book Create model that extends BookBase
class BookCreate(BookBase):
    book_id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique book identifier")
    # Fields specific to hard copy
    total_copies: int | None = Field(
        None, ge=0, description="Total number of physical copies (required for hard_copy)"
    )
    available_copies: int | None = Field(
        None, ge=0, description="Number of available physical copies (required for hard_copy)"
    )
    # Fields specific to soft copy
    file_url: str | None = Field(
        None, max_length=500, description="URL to the digital file (required for soft_copy)"
    )
    file_format: str | None = Field(
        None,
        max_length=10,
        description="Format of the digital file (e.g., PDF, EPUB) (required for soft_copy)",
    )

    @field_validator("total_copies", "available_copies", pre=True)
    @classmethod
    def ensure_hard_copy_fields(cls, v, values):
        if "book_type" in values and values["book_type"] == BookType.HARD_COPY:
            if v is None:
                raise ValueError(f"{v} is required for hard_copy books")
            if "total_copies" in values and "available_copies" in values:
                if values.get("available_copies", 0) > values.get("total_copies", 0):
                    raise ValueError("Available copies cannot exceed total copies")
        return v

    @field_validator("file_url", "file_format", pre=True)
    @classmethod
    def ensure_soft_copy_fields(cls, v, values):
        if "book_type" in values and values["book_type"] == BookType.SOFT_COPY:
            if v is None:
                raise ValueError(f"{v} is required for soft_copy books")
        return v


# Book Response model for returning data
class BookResponse(BookBase):
    book_id: uuid.UUID
    total_copies: int | None = None
    available_copies: int | None = None
    file_url: str | None = None
    file_format: str | None = None


class Config:
    orm_mode = True
