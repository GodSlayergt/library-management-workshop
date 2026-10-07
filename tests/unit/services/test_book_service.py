"""Unit tests for BookService.

Tests business logic with mocked repository dependencies.
"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from app.exceptions.duplicate_resource_exception import DuplicateResourceException
from app.models.book import Book
from app.repositories.book_repository import BookRepository
from app.schemas.request.book_request import BookRequest
from app.schemas.response.book_response import BookResponse
from app.services.book_service import BookService


class TestBookServiceCreateBook:
    """Test cases for BookService.create_book method."""
    
    def test_create_book_success(self, mock_db_session, sample_book_data, sample_book_instance):
        """Test successful book creation.
        
        Scenario: Create a new book with valid data and no duplicate ISBN.
        Expected: Book is created with available_copies = total_copies.
        """
        # Arrange
        mock_repository = MagicMock(spec=BookRepository)
        mock_repository.find_by_isbn.return_value = None  # No duplicate
        mock_repository.create.return_value = sample_book_instance
        
        service = BookService(repository=mock_repository)
        
        request = BookRequest(
            isbn=sample_book_data["isbn"],
            title=sample_book_data["title"],
            author=sample_book_data["author"],
            genre=sample_book_data["genre"],
            total_copies=sample_book_data["total_copies"]
        )
        
        # Act
        result = service.create_book(mock_db_session, request)
        
        # Assert
        assert isinstance(result, BookResponse)
        assert result.isbn == sample_book_data["isbn"]
        assert result.title == sample_book_data["title"]
        assert result.author == sample_book_data["author"]
        assert result.genre == sample_book_data["genre"]
        assert result.total_copies == sample_book_data["total_copies"]
        assert result.available_copies == sample_book_data["total_copies"]  # Business rule
        assert result.id == 101
        
        # Verify repository methods were called correctly
        mock_repository.find_by_isbn.assert_called_once_with(
            mock_db_session, 
            sample_book_data["isbn"]
        )
        mock_repository.create.assert_called_once()
        
        # Verify available_copies was set correctly in create call
        create_call_args = mock_repository.create.call_args[0]
        book_data_passed = create_call_args[1]
        assert book_data_passed["available_copies"] == sample_book_data["total_copies"]
    
    def test_create_book_duplicate_isbn(self, mock_db_session, sample_book_data, sample_book_instance):
        """Test book creation with duplicate ISBN.
        
        Scenario: Attempt to create a book with an ISBN that already exists.
        Expected: DuplicateResourceException is raised.
        """
        # Arrange
        mock_repository = MagicMock(spec=BookRepository)
        mock_repository.find_by_isbn.return_value = sample_book_instance  # Duplicate found
        
        service = BookService(repository=mock_repository)
        
        request = BookRequest(
            isbn=sample_book_data["isbn"],
            title=sample_book_data["title"],
            author=sample_book_data["author"],
            genre=sample_book_data["genre"],
            total_copies=sample_book_data["total_copies"]
        )
        
        # Act & Assert
        with pytest.raises(DuplicateResourceException) as exc_info:
            service.create_book(mock_db_session, request)
        
        # Verify exception details
        assert exc_info.value.resource_type == "Book"
        assert exc_info.value.identifier == sample_book_data["isbn"]
        assert sample_book_data["isbn"] in str(exc_info.value)
        
        # Verify find_by_isbn was called but create was NOT called
        mock_repository.find_by_isbn.assert_called_once_with(
            mock_db_session, 
            sample_book_data["isbn"]
        )
        mock_repository.create.assert_not_called()
    
    def test_create_book_available_copies_equals_total_copies(self, mock_db_session, sample_book_instance):
        """Test that available_copies is set equal to total_copies.
        
        Scenario: Create a book with various total_copies values.
        Expected: available_copies always equals total_copies.
        """
        # Arrange
        mock_repository = MagicMock(spec=BookRepository)
        mock_repository.find_by_isbn.return_value = None
        mock_repository.create.return_value = sample_book_instance
        
        service = BookService(repository=mock_repository)
        
        test_cases = [1, 5, 10, 100]
        
        for total_copies in test_cases:
            # Arrange
            request = BookRequest(
                isbn=f"978-{total_copies}",
                title="Test Book",
                author="Test Author",
                total_copies=total_copies
            )
            
            # Act
            service.create_book(mock_db_session, request)
            
            # Assert
            create_call_args = mock_repository.create.call_args[0]
            book_data = create_call_args[1]
            assert book_data["available_copies"] == total_copies
            assert book_data["total_copies"] == total_copies
    
    def test_create_book_without_genre(self, mock_db_session, sample_book_instance):
        """Test creating a book without a genre (optional field).
        
        Scenario: Create a book without providing the optional genre field.
        Expected: Book is created successfully with genre as None.
        """
        # Arrange
        mock_repository = MagicMock(spec=BookRepository)
        mock_repository.find_by_isbn.return_value = None
        mock_repository.create.return_value = sample_book_instance
        
        service = BookService(repository=mock_repository)
        
        request = BookRequest(
            isbn="978-0-12-345678-9",
            title="Test Book",
            author="Test Author",
            total_copies=3
            # genre not provided
        )
        
        # Act
        result = service.create_book(mock_db_session, request)
        
        # Assert
        assert isinstance(result, BookResponse)
        mock_repository.create.assert_called_once()
        
        # Verify genre is None in the data passed to repository
        create_call_args = mock_repository.create.call_args[0]
        book_data = create_call_args[1]
        assert book_data["genre"] is None


class TestBookServiceGetBook:
    """Test cases for BookService get methods."""
    
    def test_get_book_by_id_found(self, mock_db_session, sample_book_instance):
        """Test retrieving a book by ID when it exists.
        
        Scenario: Request a book by ID that exists in the database.
        Expected: BookResponse is returned with correct data.
        """
        # Arrange
        mock_repository = MagicMock(spec=BookRepository)
        mock_repository.find_by_id.return_value = sample_book_instance
        
        service = BookService(repository=mock_repository)
        
        # Act
        result = service.get_book_by_id(mock_db_session, 101)
        
        # Assert
        assert isinstance(result, BookResponse)
        assert result.id == 101
        assert result.isbn == sample_book_instance.isbn
        mock_repository.find_by_id.assert_called_once_with(mock_db_session, 101)
    
    def test_get_book_by_id_not_found(self, mock_db_session):
        """Test retrieving a book by ID when it doesn't exist.
        
        Scenario: Request a book by ID that does not exist.
        Expected: None is returned.
        """
        # Arrange
        mock_repository = MagicMock(spec=BookRepository)
        mock_repository.find_by_id.return_value = None
        
        service = BookService(repository=mock_repository)
        
        # Act
        result = service.get_book_by_id(mock_db_session, 999)
        
        # Assert
        assert result is None
        mock_repository.find_by_id.assert_called_once_with(mock_db_session, 999)
    
    def test_get_book_by_isbn_found(self, mock_db_session, sample_book_instance):
        """Test retrieving a book by ISBN when it exists.
        
        Scenario: Request a book by ISBN that exists in the database.
        Expected: BookResponse is returned with correct data.
        """
        # Arrange
        mock_repository = MagicMock(spec=BookRepository)
        mock_repository.find_by_isbn.return_value = sample_book_instance
        
        service = BookService(repository=mock_repository)
        
        # Act
        result = service.get_book_by_isbn(mock_db_session, "978-0-13-468599-1")
        
        # Assert
        assert isinstance(result, BookResponse)
        assert result.isbn == "978-0-13-468599-1"
        mock_repository.find_by_isbn.assert_called_once_with(
            mock_db_session, 
            "978-0-13-468599-1"
        )
    
    def test_get_book_by_isbn_not_found(self, mock_db_session):
        """Test retrieving a book by ISBN when it doesn't exist.
        
        Scenario: Request a book by ISBN that does not exist.
        Expected: None is returned.
        """
        # Arrange
        mock_repository = MagicMock(spec=BookRepository)
        mock_repository.find_by_isbn.return_value = None
        
        service = BookService(repository=mock_repository)
        
        # Act
        result = service.get_book_by_isbn(mock_db_session, "978-0-00-000000-0")
        
        # Assert
        assert result is None
        mock_repository.find_by_isbn.assert_called_once_with(
            mock_db_session, 
            "978-0-00-000000-0"
        )
    
    def test_get_all_books(self, mock_db_session, sample_book_instance):
        """Test retrieving all books with pagination.
        
        Scenario: Request a paginated list of books.
        Expected: List of BookResponse objects is returned.
        """
        # Arrange
        mock_repository = MagicMock(spec=BookRepository)
        mock_repository.find_all.return_value = [sample_book_instance]
        
        service = BookService(repository=mock_repository)
        
        # Act
        result = service.get_all_books(mock_db_session, skip=0, limit=10)
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], BookResponse)
        assert result[0].id == 101
        mock_repository.find_all.assert_called_once_with(mock_db_session, skip=0, limit=10)
    
    def test_get_total_books_count(self, mock_db_session):
        """Test getting total count of books.
        
        Scenario: Request the total number of books in the system.
        Expected: Integer count is returned.
        """
        # Arrange
        mock_repository = MagicMock(spec=BookRepository)
        mock_repository.count.return_value = 42
        
        service = BookService(repository=mock_repository)
        
        # Act
        result = service.get_total_books_count(mock_db_session)
        
        # Assert
        assert result == 42
        assert isinstance(result, int)
        mock_repository.count.assert_called_once_with(mock_db_session)
    
    def test_get_available_books(self, mock_db_session):
        """Test retrieving available books (with available_copies > 0).
        
        Scenario: Request books that are currently available for borrowing.
        Expected: List of BookResponse objects for books with available_copies > 0.
        """
        # Arrange
        available_book1 = Book(
            id=1,
            isbn="978-0-13-468599-1",
            title="Clean Code",
            author="Robert C. Martin",
            genre="Software Engineering",
            total_copies=5,
            available_copies=3,  # Available
            created_at=datetime(2026, 10, 6, 10, 30, 0),
            updated_at=datetime(2026, 10, 6, 10, 30, 0)
        )
        
        available_book2 = Book(
            id=2,
            isbn="978-0-14-144930-2",
            title="1984",
            author="George Orwell",
            genre="Classic Literature",
            total_copies=5,
            available_copies=1,  # Available
            created_at=datetime(2026, 10, 6, 10, 35, 0),
            updated_at=datetime(2026, 10, 6, 10, 35, 0)
        )
        
        mock_repository = MagicMock(spec=BookRepository)
        mock_repository.find_available_books.return_value = [available_book1, available_book2]
        
        service = BookService(repository=mock_repository)
        
        # Act
        result = service.get_available_books(mock_db_session, skip=0, limit=10)
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(book, BookResponse) for book in result)
        assert result[0].id == 1
        assert result[0].available_copies == 3
        assert result[1].id == 2
        assert result[1].available_copies == 1
        mock_repository.find_available_books.assert_called_once_with(
            mock_db_session, 
            skip=0, 
            limit=10
        )
    
    def test_get_available_books_empty_list(self, mock_db_session):
        """Test retrieving available books when none are available.
        
        Scenario: All books are checked out (available_copies = 0).
        Expected: Empty list is returned.
        """
        # Arrange
        mock_repository = MagicMock(spec=BookRepository)
        mock_repository.find_available_books.return_value = []
        
        service = BookService(repository=mock_repository)
        
        # Act
        result = service.get_available_books(mock_db_session, skip=0, limit=10)
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0
        mock_repository.find_available_books.assert_called_once_with(
            mock_db_session, 
            skip=0, 
            limit=10
        )
    
    def test_get_available_books_custom_pagination(self, mock_db_session, sample_book_instance):
        """Test retrieving available books with custom pagination.
        
        Scenario: Request available books with custom skip and limit values.
        Expected: Repository is called with correct pagination parameters.
        """
        # Arrange
        mock_repository = MagicMock(spec=BookRepository)
        mock_repository.find_available_books.return_value = [sample_book_instance]
        
        service = BookService(repository=mock_repository)
        
        # Act
        result = service.get_available_books(mock_db_session, skip=20, limit=50)
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 1
        mock_repository.find_available_books.assert_called_once_with(
            mock_db_session, 
            skip=20, 
            limit=50
        )
