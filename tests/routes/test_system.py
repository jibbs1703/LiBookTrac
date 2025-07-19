"""Tests for LibookTrac Backend System Routes."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.v1.app.routes import system_router

# Create a FastAPI app instance and include your router
app = FastAPI()
app.include_router(system_router)

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Libooktrac API"}
