import logging

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def connect_to_mongodb(host: str, port: int, database: str) -> Database | None:
    """
    Establish a connection to a MongoDB database.

    Returns:
    Connected database object or None if connection fails
    """
    try:
        client = MongoClient(host=host, port=port)
        client.admin.command("ping")
        logger.info("Connected to MongoDB")
        return client[database]
    except ConnectionFailure as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        return None


def access_db_collection(db: Database, collection_name: str) -> Collection | None:
    """
    Get a collection from the database.

    Args:
    db: Database object
    collection_name: Name of the collection to retrieve

    Returns:
    Collection object or None if the collection does not exist
    """
    try:
        return db[collection_name]
    except ConnectionFailure as e:
        logger.error(f"Error accessing collection {collection_name}: {e}")
        return None


if __name__ == "__main__":
    db = connect_to_mongodb("localhost", 27017, "libooktrac")
    print(isinstance(db, Database))
    print(db.name)
    collection = access_db_collection(db=db, collection_name="books")
    print(isinstance(collection, Collection))
    print(collection._name)
