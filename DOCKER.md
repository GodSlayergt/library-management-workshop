# Docker Deployment Guide

## 📦 Library Management System - Docker Setup

This guide explains how to build and run the Library Management FastAPI application using Docker and Docker Compose.

---

## 📋 **Prerequisites**

- **Docker** 20.10+ installed ([Download Docker](https://docs.docker.com/get-docker/))
- **Docker Compose** 1.29+ installed (included with Docker Desktop)
- **Git** (to clone the repository)

### Verify Installation

```bash
docker --version
docker-compose --version
```

---

## 🏗️ **Docker Architecture**

### Multi-Stage Dockerfile

The `Dockerfile` uses a **multi-stage build** for optimized image size and security:

#### **Stage 1: Builder**
- Base image: `python:3.12-slim`
- Installs system dependencies (gcc for compiling Python packages)
- Creates Python virtual environment in `/opt/venv`
- Installs all Python dependencies from `requirements.txt`

#### **Stage 2: Runtime**
- Base image: `python:3.12-slim` (fresh, minimal image)
- Copies only the virtual environment from Stage 1
- Creates non-root user `appuser` for security
- Copies application code
- Exposes port 8000
- Runs Uvicorn server

**Benefits:**
- 🔒 **Security**: Non-root user, minimal attack surface
- 📦 **Size**: No build tools in final image (~200MB vs ~1GB)
- ⚡ **Performance**: Only runtime dependencies included
- 🔄 **Caching**: Efficient layer caching for faster builds

---

## 🚀 **Quick Start**

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start the application
docker-compose up --build

# Run in detached mode (background)
docker-compose up -d --build
```

### Option 2: Using Docker Commands

```bash
# Build the Docker image
docker build -t library-api:latest .

# Run the container
docker run -d \
  --name library-api \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  library-api:latest
```

---

## 📂 **File Structure**

```
.
├── Dockerfile              # Multi-stage build configuration
├── docker-compose.yml      # Docker Compose orchestration
├── .dockerignore           # Files excluded from Docker context
├── requirements.txt        # Python dependencies
├── app/
│   ├── main.py            # FastAPI application entry point
│   ├── config/            # Configuration settings
│   ├── routers/           # API endpoints
│   ├── services/          # Business logic
│   ├── repositories/      # Data access layer
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   └── exceptions/        # Custom exceptions
├── data/                  # SQLite database (volume mounted)
└── logs/                  # Application logs (volume mounted)
```

---

## 🔧 **Configuration**

### Environment Variables

The application can be configured using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `production` | Deployment environment |
| `DEBUG` | `False` | Enable debug mode |
| `DATABASE_URL` | `sqlite:///./data/library.db` | Database connection string |
| `PROJECT_NAME` | `Library Management System - Book API` | API name |
| `VERSION` | `1.0.0` | API version |
| `CORS_ORIGINS` | `["http://localhost:3000"]` | Allowed CORS origins |

### Using .env File

Create a `.env` file in the project root:

```env
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=sqlite:///./data/library.db
PROJECT_NAME=Library Management System - Book API
VERSION=1.0.0
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]
```

Docker Compose will automatically load this file.

---

## 📖 **Docker Compose Commands**

### Build and Start Services

```bash
# Build and start in foreground
docker-compose up --build

# Build and start in background (detached mode)
docker-compose up -d --build

# Start without rebuilding
docker-compose up -d
```

### Stop Services

```bash
# Stop containers (keeps volumes)
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers, and delete volumes (⚠️ deletes data)
docker-compose down -v
```

### View Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs -f api

# View last 100 lines
docker-compose logs --tail=100 api
```

### Check Service Status

```bash
# List running containers
docker-compose ps

# Check health status
docker-compose ps api
```

### Execute Commands in Container

```bash
# Open a shell in the running container
docker-compose exec api bash

# Run a Python shell
docker-compose exec api python

# Run pytest
docker-compose exec api pytest
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart api
```

---

## 🗄️ **Database Persistence**

### SQLite Volume Mapping

The `docker-compose.yml` maps the database directory as a volume:

```yaml
volumes:
  - ./data:/app/data
```

**This ensures:**
- ✅ Database persists across container restarts
- ✅ Database survives container deletion
- ✅ Easy backup (copy `./data/library.db`)

### Accessing the Database

```bash
# SQLite CLI inside container
docker-compose exec api sqlite3 /app/data/library.db

# Query books table
SELECT * FROM books;

# Exit SQLite
.exit
```

### Backup Database

```bash
# Copy database from host
cp ./data/library.db ./backup/library.db.$(date +%Y%m%d)

# Or from container
docker cp library-api:/app/data/library.db ./backup/library.db
```

### Restore Database

```bash
# Copy backup to data directory
cp ./backup/library.db ./data/library.db

# Restart container to apply changes
docker-compose restart api
```

---

## 🩺 **Health Checks**

### Built-in Health Check

The Docker image includes a health check that pings `/health` every 30 seconds:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
```

### Check Health Status

```bash
# Check health via Docker
docker inspect --format='{{.State.Health.Status}}' library-api

# Check health via API
curl http://localhost:8000/health
```

**Expected response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production",
  "service": "Library Management System - Book API"
}
```

---

## 🌐 **Accessing the Application**

Once running, the application is accessible at:

- **API Root**: http://localhost:8000/
- **Interactive Docs (Swagger UI)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Books API**: http://localhost:8000/api/books

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Get all books
curl http://localhost:8000/api/books

# Create a book
curl -X POST http://localhost:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "isbn": "978-0-13-468599-1",
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "genre": "Software Engineering",
    "total_copies": 5
  }'

# Get book by ID
curl http://localhost:8000/api/books/1
```

---

## 🐛 **Troubleshooting**

### Container Won't Start

```bash
# Check logs
docker-compose logs api

# Check container status
docker-compose ps

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or change port in docker-compose.yml
ports:
  - "8001:8000"  # Map to different host port
```

### Database Locked

```bash
# Stop all containers
docker-compose down

# Remove database lock file
rm ./data/library.db-shm ./data/library.db-wal

# Restart
docker-compose up -d
```

### Permission Issues (Linux)

```bash
# Fix ownership of data directory
sudo chown -R $USER:$USER ./data

# Or run with proper user
docker-compose run --user $(id -u):$(id -g) api
```

### Clear Everything and Start Fresh

```bash
# Stop and remove containers, networks, and volumes
docker-compose down -v

# Remove all Docker images
docker rmi $(docker images -q library-api)

# Remove build cache
docker builder prune -a

# Rebuild and start
docker-compose up -d --build
```

---

## 🔒 **Security Best Practices**

### Implemented Security Features

✅ **Non-root User**: Application runs as `appuser` (UID 1000)
✅ **Minimal Base Image**: Uses `python:3.12-slim` (~200MB)
✅ **Multi-stage Build**: Build tools not included in runtime image
✅ **No Secrets in Image**: Use environment variables or Docker secrets
✅ **Health Checks**: Automatic container health monitoring
✅ **Read-only Filesystem**: Consider adding `--read-only` flag

### Production Recommendations

```yaml
# docker-compose.yml production additions
services:
  api:
    # Use secrets for sensitive data
    secrets:
      - db_password
    
    # Security options
    security_opt:
      - no-new-privileges:true
    
    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    
    # Read-only root filesystem
    read_only: true
    tmpfs:
      - /tmp
```

---

## 📊 **Monitoring and Logs**

### Log Configuration

Logs are written to:
- **Console**: Standard output (visible via `docker-compose logs`)
- **File**: `/app/app.log` (mapped to `./logs/app.log` on host)

### View Logs

```bash
# Docker logs
docker-compose logs -f api

# File logs on host
tail -f ./logs/app.log
```

### Log Rotation (Production)

Add log rotation to prevent disk space issues:

```yaml
services:
  api:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 🚀 **Production Deployment**

### Build for Production

```bash
# Build with production tag
docker build -t library-api:1.0.0 .
docker build -t library-api:latest .

# Tag for registry
docker tag library-api:1.0.0 registry.example.com/library-api:1.0.0

# Push to registry
docker push registry.example.com/library-api:1.0.0
```

### Deploy to Server

```bash
# Pull image on server
docker pull registry.example.com/library-api:1.0.0

# Run with production config
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Using with Reverse Proxy (Nginx)

```nginx
# nginx.conf
server {
    listen 80;
    server_name api.library.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🧪 **Running Tests in Docker**

```bash
# Run pytest in container
docker-compose exec api pytest

# Run with coverage
docker-compose exec api pytest --cov=app --cov-report=html

# Run specific test file
docker-compose exec api pytest tests/unit/routers/test_book_router.py -v
```

---

## 📚 **Additional Resources**

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Uvicorn Deployment](https://www.uvicorn.org/deployment/)

---

## 📝 **Summary**

### Files Created

1. **`Dockerfile`** - Multi-stage build with Python 3.12-slim
2. **`docker-compose.yml`** - Orchestration with volume mapping
3. **`.dockerignore`** - Excludes unnecessary files from build context

### Key Features

✅ Multi-stage build for minimal image size  
✅ Non-root user for security  
✅ SQLite database persistence via volumes  
✅ Health checks for monitoring  
✅ Port 8000 exposed and mapped  
✅ Environment variable configuration  
✅ Comprehensive logging  
✅ Production-ready setup  

### Quick Commands Cheat Sheet

```bash
# Start
docker-compose up -d --build

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Shell
docker-compose exec api bash

# Health
curl http://localhost:8000/health

# Test
curl http://localhost:8000/api/books
```

---

**Your Library Management System is now Docker-ready!** 🐳✨
