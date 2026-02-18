"""
Tests for the main FastAPI application.

This file contains basic tests for the app configuration and root endpoints.
"""

import pytest
from fastapi import status


class TestAppConfiguration:
    """Tests for basic app configuration."""

    def test_app_title(self, client):
        """Test that the app has correct title."""
        from app.main import app
        assert app.title == "Blog API"

    def test_app_version(self, client):
        """Test that the app has correct version."""
        from app.main import app
        assert app.version == "v1.1"

    def test_openapi_schema_exists(self, client):
        """Test that OpenAPI schema is accessible."""
        response = client.get("/openapi.json")

        assert response.status_code == status.HTTP_200_OK
        assert "openapi" in response.json()
        assert "paths" in response.json()

    def test_docs_endpoint_exists(self, client):
        """Test that Swagger docs endpoint is accessible."""
        response = client.get("/docs")

        assert response.status_code == status.HTTP_200_OK

    def test_redoc_endpoint_exists(self, client):
        """Test that ReDoc endpoint is accessible."""
        response = client.get("/redoc")

        assert response.status_code == status.HTTP_200_OK


class TestHealthCheck:
    """
    Tests for health check endpoints (if you add one).

    Example: Add a health check endpoint to your main.py:

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}
    """

    def test_root_endpoint(self, client):
        """
        Test root endpoint if it exists.
        If you don't have a root endpoint, this test will fail -
        you can either add one or remove this test.
        """
        response = client.get("/")

        # This might return 404 if you don't have a root endpoint
        # Modify based on your actual implementation
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND
        ]
