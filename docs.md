# Library Management System - Complete Documentation

A full-stack library management system featuring a FastAPI backend with clean architecture and a React TypeScript frontend.

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Docker Deployment](#docker-deployment)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Configuration](#configuration)
- [Development Workflow](#development-workflow)
- [Troubleshooting](#troubleshooting)

---

## Project Overview

### Purpose

The Library Management System is a workshop project demonstrating modern web development practices with a RESTful API backend and reactive frontend. It implements book catalog management with features for adding, retrieving, and managing library inventory.

### Key Features

- ✅ **RESTful API** - FastAPI backend with automatic OpenAPI documentation
- ✅ **Clean Architecture** - Strict layer separation (Router → Service → Repository → Model)
- ✅ **Type Safety** - Full type hints in Python, TypeScript in frontend
- ✅ **Validation** - Pydantic v2 schemas with custom validators
- ✅ **Error Handling** - Centralized exception handling with proper HTTP status codes
- ✅ **Database ORM** - SQLAlchemy with SQLite (swappable to PostgreSQL)
- ✅ **React Frontend** - TypeScript-based UI with form validation
- ✅ **Docker Support** - Multi-stage builds with docker-compose
- ✅ **Comprehensive Testing** - Pytest with 80%+ coverage requirement
- ✅ **Seed Data** - Python script to populate sample books

### Technology Stack

**Backend:**
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- Pydantic 2.5.0
- Uvicorn (ASGI server)
- Pytest (testing)

**Frontend:**
- React 18.2.0
- TypeScript 5.3.3
- Vite 5.0.8 (build tool)

**Infrastructure:**
- Docker & Docker Compose
- SQLite (development) / PostgreSQL (production)

---

## Repository Structure

```
library-management-workshop/
├── app/                          # Backend application code
│   ├── config/                   # Application settings
│   │   └── settings.py           # Environment-based configuration
│   ├── database/                 # Database setup
│   │   └── session.py            # SQLAlchemy session management
│   ├── models/                   # ORM models
│   │   └── book.py               # Book entity definition
│   ├── schemas/                  # Pydantic schemas
│   │   ├── request/
│   │   │   └── book_request.py   # Request validation
│   │   └── response/
│   │       └── book_response.py  # Response serialization
│   ├── repositories/             # Data access layer
│   │   └── book_repository.py    # Book CRUD operations
│   ├── services/                 # Business logic layer
│   │   └── book_service.py       # Book service
│   ├── routers/                  # API endpoints
│   │   └── book_router.py        # Book routes
│   ├── exceptions/               # Custom exceptions
│   │   ├── duplicate_resource_exception.py
│   │   └── exception_handlers.py # Global error handlers
│   └── main.py                   # Application entry point
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   └── types/                # TypeScript type definitions
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── tests/                        # Test suite
│   ├── unit/
│   │   ├── routers/
│   │   └── services/
│   └── conftest.py               # Pytest configuration
├── docs/                         # Documentation
│   ├── apicontract.md            # API specification
│   └── projectstructure.txt      # Directory tree
├── design/                       # Design documents
├── .env.example                  # Environment template
├── requirements.txt              # Python dependencies
├── pytest.ini                    # Pytest configuration
├── Dockerfile                    # Multi-stage Docker build
├── docker-compose.yml            # Container orchestration
├── seed_library.py               # Database seeding script
├── README.md                     # Main readme
├── QUICKSTART.md                 # Quick start guide
└── DOCKER.md                     # Docker documentation
```

---

## Prerequisites

### Required Software

- **Python 3.9+** (3.12 recommended)
- **pip** (Python package manager)
- **Node.js 18+** and **npm** (for frontend)
- **Git** (for version control)

### Optional

- **Docker** and **Docker Compose** (for containerized deployment)
- **PostgreSQL** (for production database)

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/GodSlayergt/library-management-workshop.git
cd library-management-workshop
```

### 2. Backend Setup (5 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn app.main:app --reload
```

**Backend running at:** http://localhost:8000

### 3. Frontend Setup (Optional)

```bash
cd frontend
npm install
npm run dev
```

**Frontend running at:** http://localhost:3000

### 4. Verify Installation

- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Root Endpoint:** http://localhost:8000/

---

## Backend Setup

### Environment Configuration

1. **Copy the example environment file:**

```bash
cp .env.example .env
```

2. **Edit `.env` with your settings:**

```env
# Application Settings
PROJECT_NAME=Library Management System - Book API
VERSION=1.0.0
API_V1_PREFIX=/api
DESCRIPTION=REST API for managing books in the library system

# Database Configuration
DATABASE_URL=sqlite:///./library.db
# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/library_db

# Application Settings
DEBUG=True
ENVIRONMENT=development

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

### Running the Backend

**Method 1: Using Uvicorn directly**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Method 2: Using Python module**

```bash
python -m app.main
```

**Method 3: Using the main script**

```bash
python app/main.py
```

### Seeding Sample Data

Populate the database with sample books:

```bash
python seed_library.py
```

This adds 30+ books across various genres (Software Engineering, Classic Literature, Science Fiction, Philosophy, History, Biography, Business).

---

## Frontend Setup

### Installation

```bash
cd frontend
npm install
```

### Development Server

```bash
npm run dev
```

Access at: http://localhost:3000

### Build for Production

```bash
npm run build
```

Output in `frontend/dist/`

### Preview Production Build

```bash
npm run preview
```

---

## Docker Deployment

### Using Docker Compose (Recommended)

**Start all services:**

```bash
docker-compose up -d
```

**View logs:**

```bash
docker-compose logs -f api
```

**Stop services:**

```bash
docker-compose down
```

**Rebuild after code changes:**

```bash
docker-compose up -d --build
```

### Using Docker Directly

**Build image:**

```bash
docker build -t library-api:latest .
```

**Run container:**

```bash
docker run -d \
  --name library-api \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  library-api:latest
```

### Docker Configuration

The `docker-compose.yml` includes:

- **Port mapping:** 8000:8000
- **Volume persistence:** Database and logs
- **Health checks:** Automatic health monitoring
- **Restart policy:** `unless-stopped`
- **Environment variables:** Production configuration

---

## Architecture

### Clean Architecture Layers

The application follows strict layer separation:

```
┌─────────────────────────────────────────┐
│         Router Layer (API)              │  ← HTTP requests/responses
│  - book_router.py                       │
│  - Request validation                   │
│  - Response serialization               │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Service Layer (Business)        │  ← Business logic
│  - book_service.py                      │
│  - Business rules                       │
│  - Orchestration                        │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Repository Layer (Data Access)     │  ← Database operations
│  - book_repository.py                   │
│  - CRUD operations                      │
│  - Query building                       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Model Layer (ORM)               │  ← Database schema
│  - book.py (SQLAlchemy)                 │
│  - Table definitions                    │
└─────────────────────────────────────────┘
```

### Request Flow

1. **Client** sends HTTP request to router
2. **Router** validates request with Pydantic schema
3. **Service** applies business logic
4. **Repository** performs database operations
5. **Model** represents database entity
6. **Response** flows back through layers with serialization

### Key Design Patterns

- **Repository Pattern:** Abstract data access
- **Dependency Injection:** FastAPI's dependency system
- **DTO Pattern:** Separate request/response schemas
- **Exception Handling:** Centralized error management
- **Singleton Pattern:** Cached settings instance

---

## API Reference

### Base URL

```
http://localhost:8000
```

### Endpoints

#### Create Book

**POST** `/api/books`

Create a new book record.

**Request Body:**

```json
{
  "isbn": "978-0-13-468599-1",
  "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
  "author": "Robert C. Martin",
  "genre": "Software Engineering",
  "total_copies": 5
}
```

**Response (201 Created):**

```json
{
  "id": 101,
  "isbn": "978-0-13-468599-1",
  "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
  "author": "Robert C. Martin",
  "genre": "Software Engineering",
  "available_copies": 5,
  "total_copies": 5,
  "created_at": "2026-10-06T10:30:00Z",
  "updated_at": "2026-10-06T10:30:00Z"
}
```

**Error Responses:**

- `400 Bad Request` - Validation error
- `409 Conflict` - Duplicate ISBN
- `500 Internal Server Error` - Server error

#### Get Book by ID

**GET** `/api/books/{book_id}`

Retrieve a specific book.

**Response (200 OK):**

```json
{
  "id": 101,
  "isbn": "978-0-13-468599-1",
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "genre": "Software Engineering",
  "available_copies": 5,
  "total_copies": 5,
  "created_at": "2026-10-06T10:30:00Z",
  "updated_at": "2026-10-06T10:30:00Z"
}
```

#### Get All Books

**GET** `/api/books?skip=0&limit=100`

Retrieve all books with pagination.

**Query Parameters:**

- `skip` (optional, default: 0) - Number of records to skip
- `limit` (optional, default: 100) - Maximum records to return

**Response (200 OK):**

```json
[
  {
    "id": 101,
    "isbn": "978-0-13-468599-1",
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "genre": "Software Engineering",
    "available_copies": 5,
    "total_copies": 5,
    "created_at": "2026-10-06T10:30:00Z",
    "updated_at": "2026-10-06T10:30:00Z"
  }
]
```

#### Health Check

**GET** `/health`

Check application health.

**Response (200 OK):**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "service": "Library Management System - Book API"
}
```

### Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/api/openapi.json

### cURL Examples

**Create a book:**

```bash
curl -X POST http://localhost:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "isbn": "978-0-13-468599-1",
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "genre": "Software Engineering",
    "total_copies": 5
  }'
```

**Get all books:**

```bash
curl http://localhost:8000/api/books
```

**Get book by ID:**

```bash
curl http://localhost:8000/api/books/1
```

---

## Testing

### Running Tests

**Run all tests:**

```bash
pytest
```

**Run with coverage:**

```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

**Run specific test file:**

```bash
pytest tests/unit/services/test_book_service.py -v
```

**Run by marker:**

```bash
pytest -m unit
```

### Test Structure

```
tests/
├── unit/
│   ├── routers/
│   │   └── test_book_router.py    # Router layer tests
│   └── services/
│       └── test_book_service.py   # Service layer tests
├── conftest.py                    # Shared fixtures
└── run_tests.py                   # Test runner script
```

### Coverage Requirements

The project enforces 80% minimum code coverage (configured in `pytest.ini`).

**View HTML coverage report:**

```bash
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

### Test Markers

- `@pytest.mark.unit` - Unit tests with mocked dependencies
- `@pytest.mark.integration` - Integration tests with real database
- `@pytest.mark.slow` - Tests that take significant time

---

## Configuration

### Environment Variables

All configuration is managed through environment variables (see `.env.example`):

| Variable | Description | Default |
|----------|-------------|----------|
| `PROJECT_NAME` | Application name | Library Management System - Book API |
| `VERSION` | API version | 1.0.0 |
| `API_V1_PREFIX` | API URL prefix | /api |
| `DATABASE_URL` | Database connection string | sqlite:///./library.db |
| `DEBUG` | Enable debug mode | False |
| `ENVIRONMENT` | Deployment environment | development |
| `CORS_ORIGINS` | Allowed CORS origins | ["http://localhost:3000"] |

### Database Configuration

**SQLite (Development):**

```env
DATABASE_URL=sqlite:///./library.db
```

**PostgreSQL (Production):**

```env
DATABASE_URL=postgresql://user:password@localhost:5432/library_db
```

Install PostgreSQL driver:

```bash
pip install psycopg2-binary
```

### CORS Configuration

To allow frontend access, configure CORS origins:

```env
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

### Logging

Logs are written to:

- **Console:** Structured logs with timestamps
- **File:** `app.log` in project root

Log levels:

- `DEBUG=True` - Detailed logs including SQL queries
- `DEBUG=False` - Standard operational logs (INFO level)

---

## Development Workflow

### Adding New Features

1. **Create Model** in `app/models/`
2. **Define Schemas** in `app/schemas/request/` and `app/schemas/response/`
3. **Implement Repository** in `app/repositories/`
4. **Add Business Logic** in `app/services/`
5. **Create Router** in `app/routers/`
6. **Write Tests** in `tests/unit/`
7. **Register Router** in `app/main.py`

### Code Quality

**Format code:**

```bash
black app/ tests/
```

**Lint code:**

```bash
flake8 app/ tests/
```

**Type checking:**

```bash
mypy app/
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature
```

### Database Migrations

For schema changes, the application automatically creates tables on startup via:

```python
Base.metadata.create_all(bind=engine)
```

For production, consider using Alembic for migrations:

```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---

## Troubleshooting

### Common Issues

#### Port 8000 Already in Use

**Solution:** Run on a different port

```bash
uvicorn app.main:app --reload --port 8080
```

#### SQLite Database Locked

**Solution:** Delete the database file and restart

```bash
rm library.db  # macOS/Linux
del library.db  # Windows
```

#### Import Errors

**Solution:** Ensure virtual environment is activated

```bash
# Check for (venv) in terminal prompt
# If not present, activate:
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

#### CORS Errors in Frontend

**Problem:** "No 'Access-Control-Allow-Origin' header"

**Solution:** Update CORS origins in `.env`:

```env
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

#### Docker Container Won't Start

**Solution:** Check logs

```bash
docker-compose logs api
```

Rebuild container:

```bash
docker-compose down
docker-compose up -d --build
```

#### Tests Failing

**Solution:** Ensure dependencies are installed

```bash
pip install -r requirements.txt
pytest --cache-clear
```

### Health Check Endpoints

**Backend health:**

```bash
curl http://localhost:8000/health
```

**Expected response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

### Debug Mode

Enable detailed logging:

```env
DEBUG=True
```

This enables:

- SQL query logging
- Detailed error messages
- Auto-reload on code changes
- Verbose stack traces

### Performance Optimization

**Database indexes:** Already configured on:

- `isbn` (unique index)
- `title`
- `author`

**Connection pooling:** For PostgreSQL, configure in `DATABASE_URL`:

```env
DATABASE_URL=postgresql://user:pass@localhost/db?pool_size=10&max_overflow=20
```

---

## Business Rules

1. **ISBN Uniqueness:** Each book must have a unique ISBN
2. **Automatic Available Copies:** When creating a book, `available_copies` equals `total_copies`
3. **Minimum Copies:** At least one copy required (`total_copies >= 1`)
4. **Automatic Timestamps:** `created_at` and `updated_at` managed automatically
5. **Field Constraints:**
   - ISBN: max 50 characters, alphanumeric with hyphens
   - Title: max 255 characters, required
   - Author: max 255 characters, required
   - Genre: max 100 characters, optional

---

## Additional Resources

### Documentation Files

- **README.md** - Main project documentation
- **QUICKSTART.md** - 5-minute quick start guide
- **DOCKER.md** - Docker deployment guide
- **docs/apicontract.md** - Detailed API specification
- **frontend/README.md** - Frontend component documentation

### API Documentation

- **Swagger UI:** http://localhost:8000/docs (interactive)
- **ReDoc:** http://localhost:8000/redoc (readable)

### Repository

- **GitHub:** https://github.com/GodSlayergt/library-management-workshop

---

## License

This project is part of the Library Management Workshop.

## Support

For issues or questions:

1. Check this documentation
2. Review the API contract in `docs/apicontract.md`
3. Consult the interactive API docs at http://localhost:8000/docs
4. Check existing issues on GitHub

---

**Happy Coding! 🚀**
