# FastAPI Blog Project - Testing Guide

This guide explains how to write and run tests for the FastAPI Blog Project.

## 📁 Project Test Structure

```
tests/
├── __init__.py          # Makes tests a Python package
├── conftest.py          # Shared fixtures and configuration
├── test_main.py         # Tests for app configuration
├── test_users.py        # Tests for user endpoints
└── test_blogs.py        # Tests for blog endpoints
```

## 🚀 Quick Start

### Install Testing Dependencies

```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run Tests with Verbose Output

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_users.py
pytest tests/test_blogs.py
```

### Run Specific Test Class

```bash
pytest tests/test_users.py::TestCreateUser
```

### Run Specific Test

```bash
pytest tests/test_users.py::TestCreateUser::test_create_user_success
```

## 📊 Code Coverage

### Run Tests with Coverage Report

```bash
pytest --cov=app tests/
```

### Generate HTML Coverage Report

```bash
pytest --cov=app --cov-report=html tests/
```
Then open `htmlcov/index.html` in your browser.

### Generate Coverage Report with Missing Lines

```bash
pytest --cov=app --cov-report=term-missing tests/
```

## 🧪 Writing Tests

### Basic Test Structure

```python
from fastapi import status

class TestFeatureName:
    """Tests for a specific feature."""
    
    def test_something_success(self, client):
        """Test successful operation."""
        response = client.get("/api/v1.0/endpoint/")
        assert response.status_code == status.HTTP_200_OK
    
    def test_something_failure(self, client):
        """Test failure case."""
        response = client.get("/api/v1.0/nonexistent/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
```

### Using Fixtures

Fixtures provide reusable test data and setup. Available fixtures in `conftest.py`:

```python
# Use the test client
def test_example(client):
    response = client.get("/api/v1.0/users/")
    assert response.status_code == 200

# Use sample data
def test_create_user(client, sample_user_data):
    response = client.post("/api/v1.0/users/", json=sample_user_data)
    assert response.status_code == 201

# Use pre-created user
def test_with_user(client, created_user):
    user_id = created_user["id"]
    response = client.get(f"/api/v1.0/users/{user_id}")
    assert response.status_code == 200
```

### Creating Custom Fixtures

Add to `conftest.py`:

```python
@pytest.fixture
def custom_data():
    """Custom test data."""
    return {
        "field1": "value1",
        "field2": "value2"
    }

@pytest.fixture
def authenticated_client(client, sample_user_data):
    """Client with authentication (if you add auth)."""
    # Create user and get token
    client.post("/api/v1.0/users/", json=sample_user_data)
    # Login and get token
    # Add token to headers
    return client
```

## 🔧 Test Configuration

### pytest.ini Options

```ini
[pytest]
testpaths = tests              # Where to find tests
addopts = -v --tb=short        # Default options
markers =                       # Custom markers
    slow: marks tests as slow
    integration: integration tests
```

### Using Markers

```python
import pytest

@pytest.mark.slow
def test_slow_operation(client):
    """This test takes a long time."""
    pass

@pytest.mark.integration
def test_integration(client):
    """This is an integration test."""
    pass
```

Run tests excluding slow tests:
```bash
pytest -m "not slow"
```

## 🗄️ Database Testing

Tests use an **in-memory SQLite database** instead of your real database:

- Tests won't affect your production data
- Each test gets a fresh database
- Tests run faster

### How It Works

```python
# conftest.py sets up a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db
```

## 📝 Common Test Patterns

### Testing CRUD Operations

```python
class TestResource:
    def test_create(self, client):
        response = client.post("/api/v1.0/resource/", json={"data": "value"})
        assert response.status_code == 201
    
    def test_read(self, client):
        # Create first, then read
        create_resp = client.post("/api/v1.0/resource/", json={"data": "value"})
        resource_id = create_resp.json()["id"]
        
        response = client.get(f"/api/v1.0/resource/{resource_id}")
        assert response.status_code == 200
    
    def test_update(self, client):
        # Create, then update
        create_resp = client.post("/api/v1.0/resource/", json={"data": "value"})
        resource_id = create_resp.json()["id"]
        
        response = client.put(
            f"/api/v1.0/resource/{resource_id}", 
            json={"data": "updated"}
        )
        assert response.status_code == 200
    
    def test_delete(self, client):
        # Create, then delete
        create_resp = client.post("/api/v1.0/resource/", json={"data": "value"})
        resource_id = create_resp.json()["id"]
        
        response = client.delete(f"/api/v1.0/resource/{resource_id}")
        assert response.status_code in [200, 204]
```

### Testing Validation Errors

```python
def test_missing_required_field(self, client):
    response = client.post("/api/v1.0/resource/", json={})
    assert response.status_code == 422  # Validation error

def test_invalid_data_type(self, client):
    response = client.post("/api/v1.0/resource/", json={"id": "not-an-int"})
    assert response.status_code == 422
```

### Testing Error Responses

```python
def test_not_found(self, client):
    response = client.get("/api/v1.0/resource/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
```

## 🎯 Best Practices

1. **One assertion per concept** - Each test should verify one thing
2. **Descriptive names** - `test_create_user_with_duplicate_email_fails`
3. **Arrange-Act-Assert** - Setup, execute, verify
4. **Use fixtures** - Reuse common setup code
5. **Test edge cases** - Empty inputs, invalid data, boundaries
6. **Keep tests independent** - Each test should work in isolation

## 🔄 Continuous Integration

Add to your CI pipeline (e.g., GitHub Actions):

```yaml
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=app --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## 🆘 Troubleshooting

### Tests can't find modules
```bash
# Make sure you're in the project root
cd /path/to/FastAPI_Blog_Project
pytest
```

### Database errors in tests
- Check that SQLite is available
- Ensure `conftest.py` properly overrides `get_db`

### Async test issues
```bash
# Install pytest-asyncio
pip install pytest-asyncio
```

## 📚 Resources

- [FastAPI Testing Documentation](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
