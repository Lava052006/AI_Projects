"""Tests for middleware functionality."""

import pytest
import time
from fastapi.testclient import TestClient
from app.main import app, metrics_collector


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_metrics_endpoint(client):
    """Test that metrics endpoint returns performance data."""
    # Make a few requests to generate metrics
    client.get("/")
    client.get("/health")
    
    # Get metrics
    response = client.get("/metrics")
    assert response.status_code == 200
    
    data = response.json()
    assert "requests_total" in data
    assert "uptime_seconds" in data
    assert "requests_by_method" in data
    assert "requests_by_status" in data
    assert data["requests_total"] >= 2  # At least the requests we made


def test_rate_limiting_middleware(client):
    """Test that rate limiting middleware works."""
    # This test is basic since we can't easily test the full rate limiting
    # without making many requests or mocking time
    response = client.get("/")
    assert response.status_code == 200
    
    # The middleware should not block normal requests
    response = client.get("/health")
    assert response.status_code == 200


def test_logging_middleware_integration(client):
    """Test that logging middleware doesn't break normal operation."""
    # Test that requests work normally with logging middleware
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_json_parsing_middleware(client):
    """Test that JSON parsing middleware handles malformed JSON."""
    # Test with malformed JSON
    response = client.post(
        "/api/v1/analyze-job",
        data='{"invalid": json}',  # Invalid JSON
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert "Invalid JSON format" in response.json()["detail"]


def test_metrics_collection():
    """Test that metrics collector works correctly."""
    # Reset metrics for clean test
    initial_count = metrics_collector.metrics["requests_total"]
    
    # Record a test request
    metrics_collector.record_request("GET", 200, 0.1, "/test")
    
    # Check that metrics were updated
    assert metrics_collector.metrics["requests_total"] == initial_count + 1
    assert "GET" in metrics_collector.metrics["requests_by_method"]
    assert 200 in metrics_collector.metrics["requests_by_status"]
    
    # Test metrics summary
    summary = metrics_collector.get_metrics()
    assert "requests_total" in summary
    assert "response_times" in summary
    assert "error_rate" in summary


def test_error_handling_with_middleware(client):
    """Test that error handling works with middleware."""
    # Test 404 error
    response = client.get("/nonexistent")
    assert response.status_code == 404
    
    # Test validation error with correct endpoint
    response = client.post("/api/v1/analyze-job", json={})
    assert response.status_code == 422


def test_health_check_bypasses_rate_limiting(client):
    """Test that health check endpoints bypass rate limiting."""
    # Health check should always work
    for _ in range(5):  # Make multiple requests quickly
        response = client.get("/health")
        assert response.status_code == 200
        
    # Root endpoint should also work
    for _ in range(5):
        response = client.get("/")
        assert response.status_code == 200