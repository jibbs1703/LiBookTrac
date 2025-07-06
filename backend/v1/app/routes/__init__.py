"""Routes Package for LiBookTrac Application."""
from fastapi import APIRouter

from backend.v1.app.routes.books import router as books_router

router = APIRouter()

router.include_router(books_router, prefix="/books", tags=["books"])
