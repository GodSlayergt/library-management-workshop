# Quick Start Guide

Get the Library Management API up and running in 5 minutes!

## Prerequisites

- Python 3.9 or higher installed
- Terminal/Command Prompt access

## Steps

### 1. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python -m uvicorn app.main:app --reload
```

Or simply:
```bash
python -m app.main
```

### 4. Access the API

Open your browser:

- **Swagger UI (Interactive Docs)**: http://localhost:8000/docs
- **API Root**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

## Test the API

### Using Swagger UI (Easiest)

1. Go to http://localhost:8000/docs
2. Click on **POST /api/books**
3. Click **Try it out**
4. Use this sample data:

```json
{
  "isbn": "978-0-13-468599-1",
  "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
  "author": "Robert C. Martin",
  "genre": "Software Engineering",
  "total_copies": 5
}
```

5. Click **Execute**
6. See the 201 Created response!

### Using cURL

```bash
curl -X POST http://localhost:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "isbn": "978-0-13-468599-1",
    "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
    "author": "Robert C. Martin",
    "genre": "Software Engineering",
    "total_copies": 5
  }'
```

### Using Python Requests

```python
import requests

url = "http://localhost:8000/api/books"
data = {
    "isbn": "978-0-13-468599-1",
    "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
    "author": "Robert C. Martin",
    "genre": "Software Engineering",
    "total_copies": 5
}

response = requests.post(url, json=data)
print(response.status_code)  # Should be 201
print(response.json())
```

## Run Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=app --cov-report=term-missing
```

## Common Issues

### Port 8000 already in use

Run on a different port:
```bash
python -m uvicorn app.main:app --reload --port 8080
```

### SQLite database locked

Delete the `library.db` file and restart:
```bash
rm library.db  # macOS/Linux
del library.db  # Windows
```

### Import errors

Make sure you're in the virtual environment:
```bash
# Check if (venv) appears in your terminal prompt
# If not, activate it again
```

## Next Steps

1. ✅ Read the full [README.md](README.md) for detailed documentation
2. ✅ Check [docs/apicontract.md](docs/apicontract.md) for API specifications
3. ✅ Explore the codebase structure in `app/`
4. ✅ Review tests in `tests/unit/services/`
5. ✅ Try creating books with different data
6. ✅ Test error cases (duplicate ISBN, invalid data)

## Key Features to Try

### ✅ Create a Book
**POST** `/api/books` - Add a new book

### ✅ Get Book by ID  
**GET** `/api/books/1` - Retrieve a specific book

### ✅ Get All Books
**GET** `/api/books` - List all books

### ✅ Test Validation
Try sending invalid data:
- Empty title
- Invalid ISBN format
- Negative total_copies

See the detailed validation errors!

### ✅ Test Duplicate Detection
Try creating the same book twice - you'll get a 409 Conflict!

## Stop the Server

Press `Ctrl+C` in the terminal

## Deactivate Virtual Environment

```bash
deactivate
```

---

**Happy Coding! 🚀**

For questions, see [README.md](README.md) or check the API documentation at http://localhost:8000/docs
