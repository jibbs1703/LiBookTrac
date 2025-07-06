from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo.collection import Collection

from backend.v1.app.config import config
from backend.v1.app.database.database import access_db_collection, connect_to_mongodb
from backend.v1.app.routes import router as all_routers

collections ={}


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = connect_to_mongodb(config.DB_HOST, int(config.DB_PORT), config.DB_NAME)
    collections[config.BOOKS_COLLECTION] = access_db_collection(
                                           db=db,
                                           collection_name=config.BOOKS_COLLECTION)
    yield
    collections.clear()


app = FastAPI(
    title=config.TITLE,
    version=config.VERSION,
    description=config.DESCRIPTION,
    lifespan=lifespan
)
templates = Jinja2Templates(directory="app/templates")

app.include_router(all_routers)


@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    """This route leads to the landing page for the application"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/healthcheck")
async def health_check():
    """Check if the database is ready."""
    if not isinstance(collections[config.BOOKS_COLLECTION], Collection):
        raise HTTPException(status_code=503, detail="Collections not loaded.")
    return {"status": "healthy", "message": "Collections are loaded."}
