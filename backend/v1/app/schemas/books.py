"""Database Collection Schema for Books."""

from beanie import Document


class Book(Document):
    title: str
    author: str
    published_year: int
    isbn: str| None
    available_copies: int = 1

    class Settings:
        name = "books"


# class Student(Document):
#     name: str
#     student_id: str
#     email: EmailStr
#     major: str | None
#     books_borrowed: list[str] = []

#     class Settings:
#         name = "students"


# class User(Document):
#     username: str
#     email: EmailStr
#     hashed_password: str
#     full_name: str | None
#     disabled: bool | None = False

#     class Settings:
#         name = "users"


# class Admin(Document):
#     username: str
#     email: EmailStr
#     hashed_password: str

#     class Settings:
#         name = "admins" 


# Add all your Beanie document models here for easy import
DOCUMENT_MODELS = [Book]
