import os

MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB = os.getenv("MONGO_DB", "libooktrac")
MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "secretpassword")
COLLECTIONS = [
                        os.getenv("ADMIN_COLLECTION"),
                        os.getenv("BOOKS_COLLECTION"),
                        os.getenv("STUDENTS_COLLECTION"),
                        os.getenv("USERS_COLLECTION")
]