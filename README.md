# FastAPI Blog Project

## Database Setup

### Prerequisites
- MySQL server running on localhost:3306
- Database `blog_db` created
- User credentials configured in `.env`

### Environment Variables
Configure your `.env` file:
```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/blog_db
SECRET_KEY="your-secret-key"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Alembic Migrations

### Generate a New Migration
After making changes to your models, generate a migration:
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

## Running the Application

### Development Server
```bash
fastapi dev
```

### Production Server
```bash
fastapi run
```

The API will be available at `http://127.0.0.1:8000` with docs at `/docs`.
