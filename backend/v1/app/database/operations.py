"""Database Initialization Operations."""

import asyncio
import logging
import os
from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from backend.v1.app.schemas import Book

logger = logging.getLogger(__name__)

MONGO_URI = os.getenv("MONGODB_URI",
                      "mongodb://localhost:27017/libooktrac")
MAX_RETRIES = 5
INTERVAL = 60


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for database initialization and shutdown.
    """
    client = None
    for attempt in range(MAX_RETRIES):
        try:
            client = AsyncIOMotorClient(MONGO_URI)
            await client.admin.command("ping")
            await init_beanie(
                database=client.get_database("libooktrac_db"),
                document_models=[Book]
            )
            print("Connected to MongoDB and initialized Beanie")
            break
        except (OSError, ConnectionError) as e:
            print(f"Failed to connect to MongoDB (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(INTERVAL)
            else:
                raise Exception("Could not connect to MongoDB after multiple attempts") from e
    
    print("Beanie initialization complete. Database and collections are ready.")
    yield
    print("Application shutdown: Closing MongoDB client...")
    if client:
        client.close()
    print("MongoDB client closed.")
