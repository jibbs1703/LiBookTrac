"""LibookTrac Backend Books Endpoints."""

from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Response
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from backend.v1.app.models.books import BookCreate, BookResponse

router = APIRouter()

# Remove After DB is connected
books_db: dict = {}
isbn_set: set = set()


@router.post("/add",
             response_model=BookResponse,
             status_code=HTTP_201_CREATED)
async def create_book(book: BookCreate):
    """Create a Book in the Database."""
    if book.isbn and book.isbn in isbn_set:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=f"Book with ISBN '{book.isbn}' already exists."
        )

    new_book_id = uuid4()
    while new_book_id in books_db:
        new_book_id = uuid4()

    current_time = datetime.now()

    book_response = BookResponse(
        **book.model_dump(),
        book_id=new_book_id,
        book_entry_time=current_time,
        last_updated_date=current_time
    )

    books_db[new_book_id] = book_response
    if book.isbn:
        isbn_set.add(book.isbn)

    return book_response


@router.get("/get/all", response_model=list[BookResponse])
async def get_all_books():
    """
    Retrieves a list of all books stored in the database.
    """
    return list(books_db.values())


@router.get("/get/{criteria}", response_model=list[BookResponse])
async def get_book():
    """
    Retrieves a list of all books stored in the database.
    """
    return list(books_db.values())


@router.delete("/delete/{book_id}",
               status_code=HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    """Delete a book from the database by its book_id."""
    if book_id not in books_db:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Book not found by ID.")

    book_to_delete = books_db.pop(book_id)
    if book_to_delete.isbn and book_to_delete.isbn in books_db:
        del books_db[book_to_delete.isbn]
    
    return Response(status_code=HTTP_204_NO_CONTENT)
