"""Database Initialization Operations."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import MongoClient

from backend.v1.app.config.settings import (
    COLLECTIONS,
    MONGO_DB,
    MONGO_HOST,
    MONGO_PASSWORD,
    MONGO_PORT,
    MONGO_USER,
)

logger = logging.getLogger(__name__)


def init_db():
    uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
    client = MongoClient(uri)
    db = client[MONGO_DB]

    for name in COLLECTIONS:
        if name is None:
            logger.warning("Encountered None in COLLECTIONS, skipping.")
            continue
        collection = db[name]
        if collection.count_documents({}) == 0:
            collection.insert_one({"_init": True})
            logger.info(f"Created collection: {name}")
        else:
            logger.info(f"Collection already exists: {name}")
    client.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing MongoDB collections...")
    init_db()
    logger.info("MongoDB initialization complete")
    yield
    logger.info("Shutting down FastAPI app")
