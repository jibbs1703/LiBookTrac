"""Database Connection Operations."""
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.exc import OperationalError
from sqlmodel import Session, SQLModel, create_engine

from backend.v1.app.config.settings import get_database_url

DATABASE_URL = get_database_url()
engine = create_engine(url=DATABASE_URL, echo=True)


def init_db():
    """Initialize the database by creating all tables."""
    try:
        print(f"Tables known to SQLModel.metadata: {SQLModel.metadata.tables.keys()}")
        SQLModel.metadata.create_all(engine)
    except OperationalError as e:
        raise Exception(f"Failed to connect to database: {e}") from e


def get_db():
    """Dependency to provide a database session."""
    with Session(engine) as session:
        yield session


database_dependency = Depends(get_db)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous context manager for FastAPI application lifespan events.

    This function initializes the database connection when the FastAPI application starts
    and performs any necessary cleanup when the application shuts down.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Control is yielded back to the FastAPI application after initialization.
    """
    init_db()
    yield
