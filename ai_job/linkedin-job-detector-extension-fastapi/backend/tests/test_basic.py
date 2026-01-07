"""Basic tests to verify the testing framework is working."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns expected response."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Job Analysis API is running"
    assert data["version"] == "0.1.0"


def test_health_check_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "job-analysis-api"


def test_app_creation():
    """Test that the FastAPI app can be created."""
    from app.main import app
    assert app is not None
    assert app.title == "Job Analysis API"
    assert app.version == "0.1.0"