"""Libooktrac Backend System Endpoints"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def home():
    """Home Endpoint."""
    return {"message": "Welcome to the Libooktrac API"}


@router.get("/health/ready")
async def healthcheck():
    """HealthCheck Endpoint."""
    return {"message": "Welcome to the Libooktrac HealthCheck Endpoint"}
