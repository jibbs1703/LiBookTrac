"""LiBookTrac Application Server Module."""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.v1.app.routes import router as api_router
from backend.v1.app.server import config as app_config


def libooktrac() -> FastAPI:
    app = FastAPI(name=app_config.TITLE,
                  description=app_config.DESCRIPTION,
                  version=app_config.VERSION,
                  )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(api_router, prefix="")

    return app


app = libooktrac()