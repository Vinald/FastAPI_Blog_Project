# FastAPI Blog Project

A RESTful Blog API built with FastAPI, SQLAlchemy, and JWT Authentication.

## Features

- 🔐 **JWT Authentication** - Secure token-based authentication
- 👤 **User Management** - Create, read, update, delete users
- 📝 **Blog Management** - Full CRUD operations for blog posts
- 🔒 **Authorization** - Users can only modify their own data
- 📚 **API Documentation** - Auto-generated Swagger UI and ReDoc
- 🧪 **Testing** - Comprehensive test suite with pytest

## Project Structure

```
FastAPI_Blog_Project/
├── app/
│   ├── api/v1/routes/      # API route handlers
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── blog.py         # Blog endpoints
│   │   └── user.py         # User endpoints
│   ├── core/               # Core configurations
│   │   ├── config.py       # Settings management
│   │   ├── database.py     # Database connection
│   │   └── security.py     # JWT & password utilities
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   └── services/           # Business logic
├── migrations/             # Alembic migrations
├── tests/                  # Test suite
└── .env                    # Environment variables
```

## Setup

### Prerequisites

- Python 3.10+
- MySQL server running on localhost:3306
- Database `blog_db` created

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd FastAPI_Blog_Project
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables - create a `.env` file:
```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/blog_db
SECRET_KEY="your-secret-key-here"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Tip:** Generate a secure secret key with: `openssl rand -base64 32`

5. Run database migrations:
```bash
alembic upgrade head
```

## Running the Application

### Development Server
```bash
fastapi dev
```

### Production Server
```bash
fastapi run
```

The API will be available at:
- **API:** `http://127.0.0.1:8000`
- **Swagger Docs:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1.1/auth/login` | Login and get JWT token | ❌ |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1.1/users/` | Create a new user | ❌ |
| GET | `/api/v1.1/users/` | Get all users | ❌ |
| GET | `/api/v1.1/users/me` | Get current user | ✅ |
| GET | `/api/v1.1/users/{id}` | Get user by ID | ❌ |
| PUT | `/api/v1.1/users/{id}` | Update user | ✅ (own profile only) |
| DELETE | `/api/v1.1/users/{id}` | Delete user | ✅ (own account only) |

### Blogs

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1.1/blogs/` | Create a new blog | ✅ |
| GET | `/api/v1.1/blogs/` | Get all blogs | ❌ |
| GET | `/api/v1.1/blogs/{id}` | Get blog by ID | ❌ |
| PUT | `/api/v1.1/blogs/{id}` | Update blog | ✅ |
| DELETE | `/api/v1.1/blogs/{id}` | Delete blog | ✅ |

## Authentication

### Login

```bash
curl -X POST "http://127.0.0.1:8000/api/v1.1/auth/login" \
  -d "username=your_email@example.com&password=your_password"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Using the Token

Include the token in the `Authorization` header:

```bash
curl -X GET "http://127.0.0.1:8000/api/v1.1/users/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

### Swagger UI Authentication

1. Go to `http://127.0.0.1:8000/docs`
2. Click the **Authorize** button (🔓)
3. Enter your email as username and password
4. Click **Authorize**
5. All protected endpoints will now include your token automatically

## Alembic Migrations

### Generate a New Migration
After making changes to your models:
```bash
alembic revision --autogenerate -m "description of changes"
```

### Apply Migrations
Run all pending migrations:
```bash
alembic upgrade head
```

### Rollback Migration
Rollback the last migration:
```bash
alembic downgrade -1
```

### View Migration History
```bash
alembic history
```

### View Current Revision
```bash
alembic current
```

## Testing

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Run Specific Test File
```bash
pytest tests/test_users.py
pytest tests/test_blogs.py
```

### Run Specific Test Class
```bash
pytest tests/test_users.py::TestAuthentication
pytest tests/test_blogs.py::TestCreateBlog
```

### Run with Verbose Output
```bash
pytest -v
```

## Example Usage

### Create a User
```bash
curl -X POST "http://127.0.0.1:8000/api/v1.1/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "password": "securepass123"}'
```

### Login
```bash
curl -X POST "http://127.0.0.1:8000/api/v1.1/auth/login" \
  -d "username=john@example.com&password=securepass123"
```

### Create a Blog (Authenticated)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1.1/blogs/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{"title": "My First Blog", "content": "Hello World!", "author_id": 1}'
```

### Get All Blogs
```bash
curl -X GET "http://127.0.0.1:8000/api/v1.1/blogs/"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Vinald** - [vinald.me](http://vinald.me)
