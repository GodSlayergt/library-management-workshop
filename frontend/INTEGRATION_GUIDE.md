# Integration Guide: React Frontend + FastAPI Backend

## Quick Start

### 1. Start the FastAPI Backend

```bash
# Navigate to project root
cd path/to/library-management-workshop/add-book-feature

# Install Python dependencies (if not already done)
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at: **http://localhost:8000**

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

### 2. Set Up React Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install
```

### 3. Run the React App

```bash
npm start
# or
yarn start
```

Frontend will be available at: **http://localhost:3000**

## Architecture Overview

```
┌───────────────────────┐
│  React Frontend      │
│  (Port 3000)         │
│                      │
│  AddBookForm.tsx     │
│         │            │
│         v            │
│    fetch() POST      │
└────────│─────────────┘
         │
         │ HTTP Request
         │ POST /api/books
         │
         v
┌───────────────────────┐
│  FastAPI Backend     │
│  (Port 8000)         │
│                      │
│  ┌──────────────┐   │
│  │ book_router  │   │
│  └──────┬────────┘   │
│         │            │
│  ┌──────v────────┐   │
│  │ book_service │   │
│  └──────┬────────┘   │
│         │            │
│  ┌──────v──────────┐ │
│  │ book_repository│ │
│  └──────┬──────────┘ │
│         │            │
│  ┌──────v────────┐   │
│  │ SQLite DB    │   │
│  └──────────────┘   │
└───────────────────────┘
```

## API Communication Flow

### Successful Book Creation (201)

```mermaid
sequenceDiagram
    participant User
    participant AddBookForm
    participant FastAPI
    participant Database
    
    User->>AddBookForm: Fill form & submit
    AddBookForm->>AddBookForm: Validate input
    AddBookForm->>FastAPI: POST /api/books
    FastAPI->>FastAPI: Validate request
    FastAPI->>Database: Check ISBN uniqueness
    Database-->>FastAPI: ISBN not found
    FastAPI->>Database: INSERT book
    Database-->>FastAPI: Book created
    FastAPI-->>AddBookForm: 201 + BookResponse
    AddBookForm->>User: Show success message
    AddBookForm->>AddBookForm: Reset form
```

### Duplicate ISBN Error (409)

```mermaid
sequenceDiagram
    participant User
    participant AddBookForm
    participant FastAPI
    participant Database
    
    User->>AddBookForm: Fill form & submit
    AddBookForm->>FastAPI: POST /api/books
    FastAPI->>Database: Check ISBN
    Database-->>FastAPI: ISBN exists
    FastAPI-->>AddBookForm: 409 Conflict
    AddBookForm->>User: Show "ISBN already exists"
```

### Validation Error (400)

```mermaid
sequenceDiagram
    participant User
    participant AddBookForm
    participant FastAPI
    
    User->>AddBookForm: Submit invalid data
    AddBookForm->>FastAPI: POST /api/books
    FastAPI->>FastAPI: Pydantic validation
    FastAPI-->>AddBookForm: 400 + error details
    AddBookForm->>User: Show field errors
```

## CORS Configuration

### Backend (FastAPI)

Already configured in [`app/config/settings.py`](../app/config/settings.py):

```python
CORS_ORIGINS: list[str] = [
    "http://localhost:3000",  # React dev server
    "http://localhost:8080"   # Alternative port
]
```

Applied in [`app/main.py`](../app/main.py):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

✅ **No additional CORS configuration needed!**

## Environment Variables

### Backend (.env)

Create a `.env` file in the project root (optional):

```env
# Database
DATABASE_URL=sqlite:///./library.db

# Application
DEBUG=True
ENVIRONMENT=development

# CORS (optional override)
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]
```

### Frontend

API endpoint is configured in [`src/types/types.ts`](src/types/types.ts):

```typescript
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000',
  ENDPOINTS: {
    BOOKS: '/api/books',
  },
} as const;
```

To use different API URL in production:

```typescript
export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  ENDPOINTS: {
    BOOKS: '/api/books',
  },
} as const;
```

Then set environment variable:

```bash
# .env.production
REACT_APP_API_URL=https://api.yourdomain.com
```

## Testing the Integration

### 1. Backend Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

### 2. Test POST Endpoint (Command Line)

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

Expected response (201):
```json
{
  "id": 1,
  "isbn": "978-0-13-468599-1",
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "genre": "Software Engineering",
  "available_copies": 5,
  "total_copies": 5,
  "created_at": "2026-10-07T...",
  "updated_at": "2026-10-07T..."
}
```

### 3. Test Frontend Form

1. Navigate to http://localhost:3000
2. Fill in the form:
   - ISBN: `978-0-13-468599-1`
   - Title: `Clean Code`
   - Author: `Robert C. Martin`
   - Genre: `Software Engineering`
   - Total Copies: `5`
3. Click "Add Book"
4. Verify success message appears
5. Verify form resets

### 4. Test Error Handling

**Duplicate ISBN (409):**
- Submit the same ISBN twice
- Verify error: "A book with this ISBN already exists."

**Validation Error (400):**
- Leave title empty
- Set total_copies to 0
- Verify field-level error messages appear

**Network Error:**
- Stop the backend server
- Submit the form
- Verify network error message

## Troubleshooting

### Issue: CORS Error

**Symptom:**
```
Access to fetch at 'http://localhost:8000/api/books' from origin 'http://localhost:3000'
has been blocked by CORS policy
```

**Solution:**
1. Ensure backend is running
2. Check `app/config/settings.py` includes `http://localhost:3000`
3. Restart FastAPI server

### Issue: Network Error

**Symptom:**
```
Network error: Failed to fetch. Please check if the server is running.
```

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check backend port is 8000
3. Check no firewall blocking connection

### Issue: 400 Validation Error

**Symptom:**
```json
{
  "error": "Validation Error",
  "details": [{"field": "total_copies", "message": "..."}]
}
```

**Solution:**
- Check field values match validation rules
- ISBN: non-empty, alphanumeric + hyphens
- Title/Author: non-empty, max 255 chars
- Total copies: >= 1

### Issue: TypeScript Errors

**Solution:**
```bash
# Ensure types are properly imported
import { BookRequest, BookResponse, ErrorResponse } from '../types/types';

# Check tsconfig.json is correct
npm run type-check
```

## Production Deployment

### Backend

1. Update CORS origins:
```python
CORS_ORIGINS = ["https://yourdomain.com"]
```

2. Use production database:
```python
DATABASE_URL = "postgresql://user:pass@host:5432/dbname"
```

3. Disable debug mode:
```python
DEBUG = False
ENVIRONMENT = "production"
```

### Frontend

1. Update API URL:
```typescript
BASE_URL: process.env.REACT_APP_API_URL || 'https://api.yourdomain.com'
```

2. Build for production:
```bash
npm run build
```

3. Deploy build folder to static hosting (Netlify, Vercel, S3, etc.)

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [API Contract](../docs/apicontract.md)
- [Backend README](../README.md)
- [Frontend README](README.md)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the API contract documentation
3. Inspect browser console and network tab
4. Check backend logs in `app.log`