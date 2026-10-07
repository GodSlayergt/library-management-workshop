# Library Management System - Test Suite

Comprehensive test suite for the Library Management System using pytest.

---

## 📁 Test Structure

```
tests/
├── conftest.py                          # Shared fixtures and configuration
├── pytest.ini                           # Pytest configuration (in project root)
├── run_tests.py                         # Convenient test runner script
├── README.md                            # This file
└── unit/
    ├── __init__.py
    ├── routers/
    │   ├── __init__.py
    │   ├── test_book_router.py         # Router endpoint tests (40 tests)
    │   └── TEST_DOCUMENTATION.md       # Detailed router test docs
    └── services/
        ├── __init__.py
        └── test_book_service.py        # Service layer tests
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key testing dependencies:**
- `pytest` - Test framework
- `pytest-cov` - Coverage reporting
- `pytest-asyncio` - Async test support
- `httpx` - Required by FastAPI TestClient

### 2. Run All Tests

```bash
pytest tests/ -v
```

### 3. Run with Coverage

```bash
pytest tests/ --cov=app --cov-report=html
```

View HTML report: `htmlcov/index.html`

---

## 📋 Test Categories

### Unit Tests (`tests/unit/`)

Isolated tests with mocked dependencies.

#### Router Tests (`tests/unit/routers/`)
- **File:** `test_book_router.py`
- **Tests:** 40 test cases
- **Coverage:** All HTTP endpoints
- **Mocks:** BookService layer

**Endpoints tested:**
- ✅ `POST /api/books` - Create book (25 tests)
- ✅ `GET /api/books/{id}` - Get book by ID (5 tests)
- ✅ `GET /api/books` - Get all books (10 tests)

#### Service Tests (`tests/unit/services/`)
- **File:** `test_book_service.py`
- **Tests:** Business logic validation
- **Mocks:** BookRepository layer

---

## 🎯 Test Coverage

### Current Coverage

| Module | Coverage | Tests |
|--------|----------|-------|
| `app/routers/book_router.py` | 100% | 40 |
| `app/services/book_service.py` | 100% | ~15 |
| **Overall** | **>80%** | **55+** |

### Coverage Goals
- **Minimum:** 80% (enforced by pytest.ini)
- **Target:** 90%+
- **Critical paths:** 100%

---

## 🛠️ Running Tests

### Using Test Runner Script

```bash
# All tests
python tests/run_tests.py all

# Router tests only
python tests/run_tests.py router

# Service tests only
python tests/run_tests.py service

# All unit tests
python tests/run_tests.py unit

# With coverage report
python tests/run_tests.py coverage

# With HTML coverage report
python tests/run_tests.py coverage-html

# Router tests (extra verbose)
python tests/run_tests.py router-verbose
```

### Using pytest Directly

#### Run all tests
```bash
pytest
```

#### Run specific test file
```bash
pytest tests/unit/routers/test_book_router.py -v
```

#### Run specific test class
```bash
pytest tests/unit/routers/test_book_router.py::TestCreateBookEndpoint -v
```

#### Run specific test
```bash
pytest tests/unit/routers/test_book_router.py::TestCreateBookEndpoint::test_create_book_success -v
```

#### Run with markers
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

#### Run with coverage
```bash
# Terminal report
pytest --cov=app --cov-report=term-missing

# HTML report
pytest --cov=app --cov-report=html

# Both
pytest --cov=app --cov-report=term --cov-report=html
```

#### Stop on first failure
```bash
pytest -x
```

#### Show print statements
```bash
pytest -s
```

#### Extra verbose
```bash
pytest -vv
```

---

## 🧪 Test Types

### 1. Router Tests (HTTP/API Layer)

**What:** Test FastAPI endpoints
**How:** FastAPI TestClient with mocked services
**Example:**

```python
@patch('app.routers.book_router.book_service')
def test_create_book_success(mock_service):
    mock_service.create_book.return_value = book_response
    
    response = client.post("/api/books", json=request_data)
    
    assert response.status_code == 201
    assert response.json()["isbn"] == "978-0-13-468599-1"
```

### 2. Service Tests (Business Logic)

**What:** Test business rules and validation
**How:** Mocked repository layer
**Example:**

```python
def test_create_book_duplicate_isbn(mock_db_session):
    mock_repository.find_by_isbn.return_value = existing_book
    
    with pytest.raises(DuplicateResourceException):
        service.create_book(mock_db_session, request)
```

---

## 📊 Test Fixtures

### Shared Fixtures (conftest.py)

#### `mock_db_session`
Mocked SQLAlchemy Session for database operations.

```python
@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)
```

#### `sample_book_data`
Dictionary with sample book data.

```python
@pytest.fixture
def sample_book_data():
    return {
        "isbn": "978-0-13-468599-1",
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "genre": "Software Engineering",
        "total_copies": 5
    }
```

#### `sample_book_instance`
Book ORM model instance.

```python
@pytest.fixture
def sample_book_instance():
    return Book(
        id=101,
        isbn="978-0-13-468599-1",
        title="Clean Code",
        # ...
    )
```

#### `in_memory_db`
In-memory SQLite database for integration tests.

```python
@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    # ... setup and teardown
    yield session
```

---

## ✅ Best Practices

### Test Naming
```python
# Pattern: test_<action>_<scenario>_<expected>
test_create_book_success()
test_create_book_duplicate_isbn()
test_get_book_by_id_not_found()
```

### AAA Pattern
```python
def test_example():
    # Arrange - Setup test data
    mock_service.method.return_value = expected_data
    
    # Act - Execute code under test
    response = client.post("/endpoint", json=data)
    
    # Assert - Verify results
    assert response.status_code == 201
```

### Docstrings
```python
def test_create_book_success():
    """Test successful book creation.
    
    Scenario: POST request with valid book data.
    Expected: 201 Created with BookResponse.
    """
```

### Assertions
```python
# Multiple related assertions OK
assert response.status_code == 201
assert response.json()["id"] == 101
assert "created_at" in response.json()

# Verify service calls
assert mock_service.create_book.called
mock_service.create_book.assert_called_once()
```

---

## 🔍 Debugging Tests

### Print debugging
```bash
pytest -s  # Show print() output
```

### Drop into debugger on failure
```bash
pytest --pdb
```

### Show local variables on failure
```bash
pytest -l
```

### Verbose output
```bash
pytest -vv  # Extra verbose
```

### Show full traceback
```bash
pytest --tb=long
```

---

## 📈 Coverage Reports

### Generate HTML Report
```bash
pytest --cov=app --cov-report=html
```

**Output:** `htmlcov/index.html`

**Features:**
- Line-by-line coverage visualization
- Highlighted uncovered lines
- Branch coverage
- Module-level statistics

### Terminal Report
```bash
pytest --cov=app --cov-report=term-missing
```

**Shows:**
- Coverage percentage per module
- Missing line numbers

### Coverage Threshold

Configured in `pytest.ini`:
```ini
addopts = --cov-fail-under=80
```

Tests fail if coverage < 80%.

---

## 🎯 Test Markers

### Available Markers

Defined in `pytest.ini`:

```python
@pytest.mark.unit
def test_something():
    """Unit test with mocked dependencies."""

@pytest.mark.integration
def test_with_real_db():
    """Integration test with real database."""

@pytest.mark.slow
def test_long_running():
    """Test that takes significant time."""
```

### Usage

```bash
# Run only unit tests
pytest -m unit

# Run integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Combine markers
pytest -m "unit and not slow"
```

---

## 🚨 Common Issues

### Issue: ModuleNotFoundError

**Cause:** Python can't find app module

**Solution:**
```bash
# Ensure pytest.ini has:
pythonpath = .

# Or set PYTHONPATH:
export PYTHONPATH=.
pytest
```

### Issue: Fixture not found

**Cause:** Fixture defined in wrong scope

**Solution:** Check fixture location (conftest.py or test file)

### Issue: Mock not working

**Cause:** Wrong patch path

**Solution:**
```python
# Patch where it's used, not where it's defined
@patch('app.routers.book_router.book_service')  # ✅ Correct
@patch('app.services.book_service.BookService')  # ❌ Wrong
```

### Issue: Tests pass locally but fail in CI

**Causes:**
- Environment differences
- Missing dependencies
- Database state

**Solutions:**
- Use in-memory database for tests
- Pin dependency versions
- Reset state in fixtures

---

## 📚 Additional Resources

### Documentation

- **Router Tests:** `tests/unit/routers/TEST_DOCUMENTATION.md`
- **Pytest Docs:** https://docs.pytest.org/
- **FastAPI Testing:** https://fastapi.tiangolo.com/tutorial/testing/

### Test Examples

**Router endpoint test:**
```python
@patch('app.routers.book_router.book_service')
def test_create_book_success(mock_service):
    mock_service.create_book.return_value = BookResponse(...)
    response = client.post("/api/books", json=valid_data)
    assert response.status_code == 201
```

**Service business logic test:**
```python
def test_create_book_duplicate_isbn(mock_db_session):
    mock_repo.find_by_isbn.return_value = existing_book
    with pytest.raises(DuplicateResourceException):
        service.create_book(mock_db_session, request)
```

---

## 🎉 Summary

✅ **55+ comprehensive test cases**  
✅ **100% router endpoint coverage**  
✅ **Mocked dependencies for fast execution**  
✅ **Coverage reporting (HTML + terminal)**  
✅ **Convenient test runner script**  
✅ **AAA pattern and best practices**  
✅ **CI/CD ready**  

---

## 🔄 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests with coverage
      run: |
        pytest --cov=app --cov-report=xml --cov-report=term
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## 📝 Contributing

When adding new features:

1. **Write tests first** (TDD approach)
2. **Maintain >80% coverage**
3. **Follow naming conventions**
4. **Add docstrings to tests**
5. **Use AAA pattern**
6. **Update documentation**

---

**Happy Testing! 🧪✨**
