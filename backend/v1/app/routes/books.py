"""LibookTrac Backend Books Endpoints."""

from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from backend.v1.app.models.books import BookInformation, BookResponse
from backend.v1.app.server import config

router = APIRouter()


@router.get(path="/get-book/", response_model=BookResponse,
            name="books:get-book", status_code=HTTP_200_OK)
async def get_book_information(title: str = None,
                               author: str = None,
                               genre: str = None,
                               isbn: str = None,
                               book_type: str = None)-> BookResponse:
    """
    This endpoint searches for books in the database based on the 
    request criteria.

    Args:
    request: BookRequest object containing search criteria.

    Returns:
    BookSearchResponse object containing the search results
    """
    collection = config.BOOKS_COLLECTION
    # request = 
    query = {}
    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    if author:
        query["author"] = {"$regex": author, "$options": "i"}
    if genre:
        query["genre"] = {"$regex": f"^{genre}$", "$options": "i"}
    if isbn:
        query["isbn"] = isbn
    if book_type:
        query["book_type"] = book_type

    filtered_books = []
    async for book in collection.find(query):
        filtered_books.append(book)
    if not filtered_books:
        raise HTTPException(status_code=404, detail="No books found matching the criteria")

    return BookResponse(
        results=[BookInformation(**book) for book in filtered_books],
        total_count=len(filtered_books)
    )


@router.post(path="/add-book/", response_model=BookInformation,
             name="books:add-book", status_code=HTTP_201_CREATED)
async def add_book_to_database(book: BookInformation) -> BookInformation:
    """
    Add a new book to the database.

    This endpoint accepts a BookInformation object containing
    details about the book (e.g., title, author, genre, ISBN, etc.)
    and stores it in the MongoDB database. The newly added book's
    information is returned as confirmation.

    Args:
    book (BookInformation): The book details to be added to the database.

    Returns:
    BookInformation: The newly created book entry with its details.
    """
    collection = config.BOOKS_COLLECTION
    book_as_dict = book.model_dump()
    result = await collection.insert_one(book_as_dict)
    created_book = await result.find_one({"_id": result.inserted_id})
    return BookInformation(**created_book)