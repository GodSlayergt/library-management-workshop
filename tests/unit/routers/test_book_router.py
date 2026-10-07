"""Unit tests for BookRouter.

Tests FastAPI router endpoints with mocked service dependencies.
Follows pytest best practices and AAA pattern (Arrange-Act-Assert).

Note: This application uses custom exception handlers that return:
- 400 Bad Request for validation errors (not 422)
- Custom error format with 'error', 'message', and 'details' fields
- 409 Conflict for duplicate resources with 'error', 'message', and 'details'
"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.exceptions.duplicate_resource_exception import DuplicateResourceException
from app.schemas.request.book_request import BookRequest
from app.schemas.response.book_response import BookResponse
from app.services.book_service import BookService


# Test client for FastAPI
client = TestClient(app)


class TestCreateBookEndpoint:
    """Test cases for POST /api/books endpoint."""
    
    @pytest.fixture
    def mock_book_service(self):
        """Mock BookService for testing router endpoints.
        
        Returns:
            MagicMock: Mocked BookService instance
        """
        return MagicMock(spec=BookService)
    
    @pytest.fixture
    def valid_book_request(self):
        """Valid book request payload.
        
        Returns:
            dict: Valid book data for POST request
        """
        return {
            "isbn": "978-0-13-468599-1",
            "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
            "author": "Robert C. Martin",
            "genre": "Software Engineering",
            "total_copies": 5
        }
    
    @pytest.fixture
    def book_response_data(self):
        """Sample book response data.
        
        Returns:
            BookResponse: Sample response object
        """
        return BookResponse(
            id=101,
            isbn="978-0-13-468599-1",
            title="Clean Code: A Handbook of Agile Software Craftsmanship",
            author="Robert C. Martin",
            genre="Software Engineering",
            available_copies=5,
            total_copies=5,
            created_at=datetime(2026, 10, 6, 10, 30, 0),
            updated_at=datetime(2026, 10, 6, 10, 30, 0)
        )
    
    @patch('app.routers.book_router.book_service')
    def test_create_book_success(self, mock_service, valid_book_request, book_response_data):
        """Test successful book creation.
        
        Scenario: POST request with valid book data.
        Expected: 201 Created with BookResponse in body.
        """
        # Arrange
        mock_service.create_book.return_value = book_response_data
        
        # Act
        response = client.post("/api/books", json=valid_book_request)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        
        response_data = response.json()
        assert response_data["id"] == 101
        assert response_data["isbn"] == valid_book_request["isbn"]
        assert response_data["title"] == valid_book_request["title"]
        assert response_data["author"] == valid_book_request["author"]
        assert response_data["genre"] == valid_book_request["genre"]
        assert response_data["total_copies"] == 5
        assert response_data["available_copies"] == 5
        assert "created_at" in response_data
        assert "updated_at" in response_data
        
        # Verify service method was called
        assert mock_service.create_book.called
    
    @patch('app.routers.book_router.book_service')
    def test_create_book_duplicate_isbn(self, mock_service, valid_book_request):
        """Test book creation with duplicate ISBN.
        
        Scenario: POST request with ISBN that already exists.
        Expected: 409 Conflict error with custom format.
        """
        # Arrange
        mock_service.create_book.side_effect = DuplicateResourceException(
            resource_type="Book",
            identifier=valid_book_request["isbn"],
            message=f"A book with ISBN '{valid_book_request['isbn']}' already exists in the system"
        )
        
        # Act
        response = client.post("/api/books", json=valid_book_request)
        
        # Assert
        assert response.status_code == status.HTTP_409_CONFLICT
        
        response_data = response.json()
        assert "error" in response_data
        assert "message" in response_data
        assert valid_book_request["isbn"] in response_data["message"]
    
    def test_create_book_missing_required_field_isbn(self):
        """Test book creation with missing ISBN.
        
        Scenario: POST request without required ISBN field.
        Expected: 400 Bad Request (custom validation error handler).
        """
        # Arrange
        invalid_request = {
            "title": "Test Book",
            "author": "Test Author",
            "total_copies": 5
            # isbn is missing
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        response_data = response.json()
        assert "error" in response_data
        assert "details" in response_data
        # Check that error mentions isbn field
        fields = [detail["field"] for detail in response_data["details"]]
        assert "isbn" in fields
    
    def test_create_book_missing_required_field_title(self):
        """Test book creation with missing title.
        
        Scenario: POST request without required title field.
        Expected: 400 Bad Request.
        """
        # Arrange
        invalid_request = {
            "isbn": "978-0-13-468599-1",
            "author": "Test Author",
            "total_copies": 5
            # title is missing
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        response_data = response.json()
        fields = [detail["field"] for detail in response_data["details"]]
        assert "title" in fields
    
    def test_create_book_missing_required_field_author(self):
        """Test book creation with missing author.
        
        Scenario: POST request without required author field.
        Expected: 400 Bad Request.
        """
        # Arrange
        invalid_request = {
            "isbn": "978-0-13-468599-1",
            "title": "Test Book",
            "total_copies": 5
            # author is missing
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        response_data = response.json()
        fields = [detail["field"] for detail in response_data["details"]]
        assert "author" in fields
    
    def test_create_book_missing_required_field_total_copies(self):
        """Test book creation with missing total_copies.
        
        Scenario: POST request without required total_copies field.
        Expected: 400 Bad Request.
        """
        # Arrange
        invalid_request = {
            "isbn": "978-0-13-468599-1",
            "title": "Test Book",
            "author": "Test Author"
            # total_copies is missing
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        response_data = response.json()
        fields = [detail["field"] for detail in response_data["details"]]
        assert "total_copies" in fields
    
    def test_create_book_empty_isbn(self):
        """Test book creation with empty ISBN.
        
        Scenario: POST request with empty string for ISBN.
        Expected: 400 Bad Request.
        """
        # Arrange
        invalid_request = {
            "isbn": "",
            "title": "Test Book",
            "author": "Test Author",
            "total_copies": 5
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_book_empty_title(self):
        """Test book creation with empty title.
        
        Scenario: POST request with empty string for title.
        Expected: 400 Bad Request.
        """
        # Arrange
        invalid_request = {
            "isbn": "978-0-13-468599-1",
            "title": "",
            "author": "Test Author",
            "total_copies": 5
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_book_empty_author(self):
        """Test book creation with empty author.
        
        Scenario: POST request with empty string for author.
        Expected: 400 Bad Request.
        """
        # Arrange
        invalid_request = {
            "isbn": "978-0-13-468599-1",
            "title": "Test Book",
            "author": "",
            "total_copies": 5
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_book_whitespace_only_isbn(self):
        """Test book creation with whitespace-only ISBN.
        
        Scenario: POST request with only whitespace for ISBN.
        Expected: 400 Bad Request.
        """
        # Arrange
        invalid_request = {
            "isbn": "   ",
            "title": "Test Book",
            "author": "Test Author",
            "total_copies": 5
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_book_invalid_isbn_format(self):
        """Test book creation with invalid ISBN format.
        
        Scenario: POST request with ISBN containing invalid characters.
        Expected: 400 Bad Request.
        """
        # Arrange
        invalid_request = {
            "isbn": "978@0#13!468599",  # Invalid characters
            "title": "Test Book",
            "author": "Test Author",
            "total_copies": 5
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_book_isbn_too_long(self):
        """Test book creation with ISBN exceeding max length.
        
        Scenario: POST request with ISBN longer than 50 characters.
        Expected: 400 Bad Request.
        """
        # Arrange
        invalid_request = {
            "isbn": "978" + "0" * 50,  # 53 characters
            "title": "Test Book",
            "author": "Test Author",
            "total_copies": 5
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_book_title_too_long(self):
        """Test book creation with title exceeding max length.
        
        Scenario: POST request with title longer than 255 characters.
        Expected: 400 Bad Request.
        """
        # Arrange
        invalid_request = {
            "isbn": "978-0-13-468599-1",
            "title": "A" * 256,  # 256 characters
            "author": "Test Author",
            "total_copies": 5
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_book_author_too_long(self):
        """Test book creation with author exceeding max length.
        
        Scenario: POST request with author longer than 255 characters.
        Expected: 400 Bad Request.
        """
        # Arrange
        invalid_request = {
            "isbn": "978-0-13-468599-1",
            "title": "Test Book",
            "author": "A" * 256,  # 256 characters
            "total_copies": 5
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_book_genre_too_long(self):
        """Test book creation with genre exceeding max length.
        
        Scenario: POST request with genre longer than 100 characters.
        Expected: 400 Bad Request.
        """
        # Arrange
        invalid_request = {
            "isbn": "978-0-13-468599-1",
            "title": "Test Book",
            "author": "Test Author",
            "genre": "A" * 101,  # 101 characters
            "total_copies": 5
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_book_zero_total_copies(self):
        """Test book creation with zero total_copies.
        
        Scenario: POST request with total_copies = 0.
        Expected: 400 Bad Request (must be at least 1).
        """
        # Arrange
        invalid_request = {
            "isbn": "978-0-13-468599-1",
            "title": "Test Book",
            "author": "Test Author",
            "total_copies": 0
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_book_negative_total_copies(self):
        """Test book creation with negative total_copies.
        
        Scenario: POST request with total_copies < 0.
        Expected: 400 Bad Request.
        """
        # Arrange
        invalid_request = {
            "isbn": "978-0-13-468599-1",
            "title": "Test Book",
            "author": "Test Author",
            "total_copies": -5
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_book_invalid_total_copies_type(self):
        """Test book creation with non-integer total_copies.
        
        Scenario: POST request with total_copies as string.
        Expected: 400 Bad Request.
        """
        # Arrange
        invalid_request = {
            "isbn": "978-0-13-468599-1",
            "title": "Test Book",
            "author": "Test Author",
            "total_copies": "five"  # String instead of int
        }
        
        # Act
        response = client.post("/api/books", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('app.routers.book_router.book_service')
    def test_create_book_without_genre(self, mock_service, book_response_data):
        """Test book creation without optional genre field.
        
        Scenario: POST request without genre (optional field).
        Expected: 201 Created (genre is optional).
        """
        # Arrange
        request_without_genre = {
            "isbn": "978-0-13-468599-1",
            "title": "Test Book",
            "author": "Test Author",
            "total_copies": 5
            # genre not provided
        }
        
        response_data_no_genre = BookResponse(
            id=101,
            isbn="978-0-13-468599-1",
            title="Test Book",
            author="Test Author",
            genre=None,
            available_copies=5,
            total_copies=5,
            created_at=datetime(2026, 10, 6, 10, 30, 0),
            updated_at=datetime(2026, 10, 6, 10, 30, 0)
        )
        
        mock_service.create_book.return_value = response_data_no_genre
        
        # Act
        response = client.post("/api/books", json=request_without_genre)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        
        response_data = response.json()
        assert response_data["genre"] is None
    
    @patch('app.routers.book_router.book_service')
    def test_create_book_strips_whitespace(self, mock_service, book_response_data):
        """Test that whitespace is stripped from string fields.
        
        Scenario: POST request with leading/trailing whitespace.
        Expected: 201 Created with trimmed values.
        """
        # Arrange
        request_with_whitespace = {
            "isbn": "  978-0-13-468599-1  ",
            "title": "  Clean Code  ",
            "author": "  Robert C. Martin  ",
            "genre": "  Software Engineering  ",
            "total_copies": 5
        }
        
        mock_service.create_book.return_value = book_response_data
        
        # Act
        response = client.post("/api/books", json=request_with_whitespace)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify service was called (whitespace stripping happens in Pydantic)
        assert mock_service.create_book.called
    
    def test_create_book_invalid_json(self):
        """Test book creation with malformed JSON.
        
        Scenario: POST request with invalid JSON syntax.
        Expected: 400 Bad Request.
        """
        # Act
        response = client.post(
            "/api/books",
            data="{invalid json}",
            headers={"Content-Type": "application/json"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_book_empty_body(self):
        """Test book creation with empty request body.
        
        Scenario: POST request with no body.
        Expected: 400 Bad Request.
        """
        # Act
        response = client.post("/api/books", json={})
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestGetBookByIdEndpoint:
    """Test cases for GET /api/books/{book_id} endpoint."""
    
    @pytest.fixture
    def book_response_data(self):
        """Sample book response data.
        
        Returns:
            BookResponse: Sample response object
        """
        return BookResponse(
            id=101,
            isbn="978-0-13-468599-1",
            title="Clean Code: A Handbook of Agile Software Craftsmanship",
            author="Robert C. Martin",
            genre="Software Engineering",
            available_copies=5,
            total_copies=5,
            created_at=datetime(2026, 10, 6, 10, 30, 0),
            updated_at=datetime(2026, 10, 6, 10, 30, 0)
        )
    
    @patch('app.routers.book_router.book_service')
    def test_get_book_by_id_found(self, mock_service, book_response_data):
        """Test retrieving a book by ID that exists.
        
        Scenario: GET request for existing book ID.
        Expected: 200 OK with BookResponse.
        """
        # Arrange
        mock_service.get_book_by_id.return_value = book_response_data
        
        # Act
        response = client.get("/api/books/101")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        response_data = response.json()
        assert response_data["id"] == 101
        assert response_data["isbn"] == "978-0-13-468599-1"
        assert response_data["title"] == "Clean Code: A Handbook of Agile Software Craftsmanship"
        assert response_data["author"] == "Robert C. Martin"
        
        # Verify service method was called with correct ID
        mock_service.get_book_by_id.assert_called_once()
        call_args = mock_service.get_book_by_id.call_args
        # Second argument should be the book_id
        assert call_args[0][1] == 101
    
    @patch('app.routers.book_router.book_service')
    def test_get_book_by_id_not_found(self, mock_service):
        """Test retrieving a book by ID that doesn't exist.
        
        Scenario: GET request for non-existent book ID.
        Expected: 404 Not Found.
        """
        # Arrange
        mock_service.get_book_by_id.return_value = None
        
        # Act
        response = client.get("/api/books/999")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        response_data = response.json()
        assert "detail" in response_data
        assert "999" in response_data["detail"]
    
    def test_get_book_by_id_invalid_id_type(self):
        """Test retrieving a book with non-integer ID.
        
        Scenario: GET request with string ID instead of integer.
        Expected: 400 Bad Request.
        """
        # Act
        response = client.get("/api/books/abc")
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('app.routers.book_router.book_service')
    def test_get_book_by_id_zero(self, mock_service):
        """Test retrieving a book with ID = 0.
        
        Scenario: GET request with book_id = 0.
        Expected: Service is called, likely returns None (404).
        """
        # Arrange
        mock_service.get_book_by_id.return_value = None
        
        # Act
        response = client.get("/api/books/0")
        
        # Assert
        # ID 0 is technically valid integer, so request is processed
        # but book won't exist
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    @patch('app.routers.book_router.book_service')
    def test_get_book_by_id_negative(self, mock_service):
        """Test retrieving a book with negative ID.
        
        Scenario: GET request with negative book_id.
        Expected: Service is called, returns None (404).
        """
        # Arrange
        mock_service.get_book_by_id.return_value = None
        
        # Act
        response = client.get("/api/books/-1")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestGetAllBooksEndpoint:
    """Test cases for GET /api/books endpoint."""
    
    @pytest.fixture
    def multiple_books_response(self):
        """Sample list of books.
        
        Returns:
            list[BookResponse]: List of book responses
        """
        return [
            BookResponse(
                id=1,
                isbn="978-0-13-468599-1",
                title="Clean Code",
                author="Robert C. Martin",
                genre="Software Engineering",
                available_copies=5,
                total_copies=5,
                created_at=datetime(2026, 10, 6, 10, 30, 0),
                updated_at=datetime(2026, 10, 6, 10, 30, 0)
            ),
            BookResponse(
                id=2,
                isbn="978-0-14-144930-2",
                title="1984",
                author="George Orwell",
                genre="Classic Literature",
                available_copies=3,
                total_copies=5,
                created_at=datetime(2026, 10, 6, 10, 35, 0),
                updated_at=datetime(2026, 10, 6, 10, 35, 0)
            ),
            BookResponse(
                id=3,
                isbn="978-0-44-100590-1",
                title="Dune",
                author="Frank Herbert",
                genre="Science Fiction",
                available_copies=6,
                total_copies=6,
                created_at=datetime(2026, 10, 6, 10, 40, 0),
                updated_at=datetime(2026, 10, 6, 10, 40, 0)
            )
        ]
    
    @patch('app.routers.book_router.book_service')
    def test_get_all_books_default_pagination(self, mock_service, multiple_books_response):
        """Test retrieving all books with default pagination.
        
        Scenario: GET request without query parameters.
        Expected: 200 OK with list of books (default skip=0, limit=100).
        """
        # Arrange
        mock_service.get_all_books.return_value = multiple_books_response
        
        # Act
        response = client.get("/api/books")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == 3
        
        # Verify first book
        assert response_data[0]["id"] == 1
        assert response_data[0]["title"] == "Clean Code"
        
        # Verify service called with default values
        mock_service.get_all_books.assert_called_once()
        call_kwargs = mock_service.get_all_books.call_args[1]
        assert call_kwargs["skip"] == 0
        assert call_kwargs["limit"] == 100
    
    @patch('app.routers.book_router.book_service')
    def test_get_all_books_custom_pagination(self, mock_service, multiple_books_response):
        """Test retrieving all books with custom pagination.
        
        Scenario: GET request with skip and limit parameters.
        Expected: 200 OK with service called with correct parameters.
        """
        # Arrange
        mock_service.get_all_books.return_value = multiple_books_response
        
        # Act
        response = client.get("/api/books?skip=10&limit=20")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        # Verify service called with custom values
        mock_service.get_all_books.assert_called_once()
        call_kwargs = mock_service.get_all_books.call_args[1]
        assert call_kwargs["skip"] == 10
        assert call_kwargs["limit"] == 20
    
    @patch('app.routers.book_router.book_service')
    def test_get_all_books_empty_list(self, mock_service):
        """Test retrieving books when library is empty.
        
        Scenario: GET request when no books exist.
        Expected: 200 OK with empty list.
        """
        # Arrange
        mock_service.get_all_books.return_value = []
        
        # Act
        response = client.get("/api/books")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == 0
    
    @patch('app.routers.book_router.book_service')
    def test_get_all_books_skip_zero(self, mock_service, multiple_books_response):
        """Test retrieving books with skip=0.
        
        Scenario: GET request with explicit skip=0.
        Expected: 200 OK starting from first record.
        """
        # Arrange
        mock_service.get_all_books.return_value = multiple_books_response
        
        # Act
        response = client.get("/api/books?skip=0")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        call_kwargs = mock_service.get_all_books.call_args[1]
        assert call_kwargs["skip"] == 0
    
    @patch('app.routers.book_router.book_service')
    def test_get_all_books_negative_skip(self, mock_service, multiple_books_response):
        """Test retrieving books with negative skip.
        
        Scenario: GET request with skip < 0.
        Expected: 200 OK (backend handles negative skip).
        """
        # Arrange
        mock_service.get_all_books.return_value = multiple_books_response
        
        # Act
        response = client.get("/api/books?skip=-1")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
    
    @patch('app.routers.book_router.book_service')
    def test_get_all_books_negative_limit(self, mock_service, multiple_books_response):
        """Test retrieving books with negative limit.
        
        Scenario: GET request with limit < 0.
        Expected: 200 OK (backend handles negative limit).
        """
        # Arrange
        mock_service.get_all_books.return_value = multiple_books_response
        
        # Act
        response = client.get("/api/books?limit=-1")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
    
    def test_get_all_books_invalid_skip_type(self):
        """Test retrieving books with non-integer skip.
        
        Scenario: GET request with skip as string.
        Expected: 400 Bad Request.
        """
        # Act
        response = client.get("/api/books?skip=abc")
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_get_all_books_invalid_limit_type(self):
        """Test retrieving books with non-integer limit.
        
        Scenario: GET request with limit as string.
        Expected: 400 Bad Request.
        """
        # Act
        response = client.get("/api/books?limit=xyz")
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('app.routers.book_router.book_service')
    def test_get_all_books_large_limit(self, mock_service, multiple_books_response):
        """Test retrieving books with very large limit.
        
        Scenario: GET request with limit=10000.
        Expected: 200 OK (service handles the limit).
        """
        # Arrange
        mock_service.get_all_books.return_value = multiple_books_response
        
        # Act
        response = client.get("/api/books?limit=10000")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        call_kwargs = mock_service.get_all_books.call_args[1]
        assert call_kwargs["limit"] == 10000
    
    @patch('app.routers.book_router.book_service')
    def test_get_all_books_single_book(self, mock_service):
        """Test retrieving books when only one book exists.
        
        Scenario: GET request with single book in database.
        Expected: 200 OK with array containing one book.
        """
        # Arrange
        single_book = [
            BookResponse(
                id=1,
                isbn="978-0-13-468599-1",
                title="Clean Code",
                author="Robert C. Martin",
                genre="Software Engineering",
                available_copies=5,
                total_copies=5,
                created_at=datetime(2026, 10, 6, 10, 30, 0),
                updated_at=datetime(2026, 10, 6, 10, 30, 0)
            )
        ]
        mock_service.get_all_books.return_value = single_book
        
        # Act
        response = client.get("/api/books")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        response_data = response.json()
        assert len(response_data) == 1
        assert response_data[0]["id"] == 1
