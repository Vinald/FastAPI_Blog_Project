"""
Pytest configuration and fixtures for FastAPI Blog Project tests.

This file contains shared fixtures that can be used across all test files.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app, version
from app.core.database import Base, get_db

# API prefix - dynamically uses the version from main.py
API_PREFIX = f"/api/{version}"


# Create an in-memory SQLite database for testing
# This ensures tests don't affect your real database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """
    Override the get_db dependency to use the test database.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """
    Create a fresh database session for each test.

    This fixture:
    1. Creates all database tables
    2. Provides a session for the test
    3. Cleans up (drops all tables) after the test
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after each test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client with database override.

    Usage in tests:
        def test_example(client):
            response = client.get("/some-endpoint")
            assert response.status_code == 200
    """
    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db

    # Create tables for the test
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    # Clean up
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_user_data():
    """
    Sample user data for testing.
    """
    return {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword123"
    }


@pytest.fixture
def sample_blog_data():
    """
    Sample blog data for testing.
    """
    return {
        "title": "Test Blog Title",
        "content": "This is test blog content.",
        "author_id": 1
    }


@pytest.fixture
def api_prefix():
    """
    Returns the API prefix (e.g., '/api/v1.0').
    This automatically updates when you change the version in main.py.
    """
    return API_PREFIX


@pytest.fixture
def created_user(client, sample_user_data, api_prefix):
    """
    Create a user and return the response data.
    Useful when you need a user to exist before running other tests.
    """
    response = client.post(f"{api_prefix}/users/", json=sample_user_data)
    return response.json()
