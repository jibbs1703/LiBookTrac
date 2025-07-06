"""Configurations for the Libooktrac Application"""
import os

from dotenv import load_dotenv

load_dotenv()

TITLE="LiBookTrac App"
VERSION="1.0.0"
DESCRIPTION="library management system application backend"

DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")
BOOKS_COLLECTION=os.getenv("BOOKS_COLLECTION")
USERS_COLLECTION=os.getenv("USERS_COLLECTION")