"""Book service layer for business logic.

Implements business rules and coordinates between router and repository layers.
"""

import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from app.exceptions.duplicate_resource_exception import DuplicateResourceException
from app.models.book import Book
from app.repositories.book_repository import BookRepository
from app.schemas.request.book_request import BookRequest
from app.schemas.response.book_response import BookResponse

# Configure logger
logger = logging.getLogger(__name__)


class BookService:
    """Service layer for Book-related business logic.
    
    Coordinates between the API layer (routers) and data layer (repositories),
    implementing business rules and validation.
    """
    
    def __init__(self, repository: BookRepository = None):
        """Initialize the service with a repository.
        
        Args:
            repository: BookRepository instance (defaults to BookRepository)
        """
        self.repository = repository or BookRepository()
     #Explain what this method does and identify any edge cases not currently handled
    def create_book(self, db: Session, request: BookRequest) -> BookResponse:
        """Create a new book in the system.
        
        Business rules:
        1. Check for duplicate ISBN (must be unique)
        2. Set available_copies equal to total_copies (new books are all available)
        3. Save book through repository
        4. Return response schema
        
        Args:
            db: Database session
            request: BookRequest containing book data
            
        Returns:
            BookResponse: Created book with generated ID and timestamps
            
        Raises:
            DuplicateResourceException: If a book with the same ISBN already exists
            SQLAlchemyError: If database operation fails
            
        Example:
            >>> request = BookRequest(
            ...     isbn="978-0-13-468599-1",
            ...     title="Clean Code",
            ...     author="Robert C. Martin",
            ...     genre="Software Engineering",
            ...     total_copies=5
            ... )
            >>> service = BookService()
            >>> book_response = service.create_book(db, request)
        """
        logger.info(f"Creating new book with ISBN: {request.isbn}")
        
        # Business Rule 1: Check for duplicate ISBN
        existing_book = self.repository.find_by_isbn(db, request.isbn)
        if existing_book:
            logger.warning(f"Duplicate ISBN detected: {request.isbn}")
            raise DuplicateResourceException(
                resource_type="Book",
                identifier=request.isbn,
                message=f"A book with ISBN '{request.isbn}' already exists in the system"
            )
        
        # Business Rule 2: Set available_copies = total_copies for new books
        book_data = request.model_dump()
        book_data["available_copies"] = request.total_copies
        
        logger.debug(f"Book data prepared: {book_data}")
        
        # Business Rule 3: Save book through repository
        created_book = self.repository.create(db, book_data)
        
        logger.info(
            f"Book created successfully: ID={created_book.id}, "
            f"ISBN={created_book.isbn}, Title='{created_book.title}'"
        )
        
        # Business Rule 4: Return response schema
        return BookResponse.model_validate(created_book)
    
    def get_book_by_id(self, db: Session, book_id: int) -> Optional[BookResponse]:
        """Retrieve a book by its ID.
        
        Args:
            db: Database session
            book_id: Unique identifier of the book
            
        Returns:
            BookResponse if found, None otherwise
            
        Example:
            >>> service = BookService()
            >>> book = service.get_book_by_id(db, 101)
        """
        logger.info(f"Fetching book with ID: {book_id}")
        
        book = self.repository.find_by_id(db, book_id)
        if book:
            logger.debug(f"Book found: {book}")
            return BookResponse.model_validate(book)
        
        logger.warning(f"Book not found with ID: {book_id}")
        return None
    
    def get_book_by_isbn(self, db: Session, isbn: str) -> Optional[BookResponse]:
        """Retrieve a book by its ISBN.
        
        Args:
            db: Database session
            isbn: International Standard Book Number
            
        Returns:
            BookResponse if found, None otherwise
            
        Example:
            >>> service = BookService()
            >>> book = service.get_book_by_isbn(db, "978-0-13-468599-1")
        """
        logger.info(f"Fetching book with ISBN: {isbn}")
        
        book = self.repository.find_by_isbn(db, isbn)
        if book:
            logger.debug(f"Book found: {book}")
            return BookResponse.model_validate(book)
        
        logger.warning(f"Book not found with ISBN: {isbn}")
        return None
    
    def get_all_books(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[BookResponse]:
        """Retrieve all books with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip (offset)
            limit: Maximum number of records to return
            
        Returns:
            List of BookResponse objects
            
        Example:
            >>> service = BookService()
            >>> books = service.get_all_books(db, skip=0, limit=10)
        """
        logger.info(f"Fetching books with skip={skip}, limit={limit}")
        
        books = self.repository.find_all(db, skip=skip, limit=limit)
        logger.debug(f"Found {len(books)} books")
        
        return [BookResponse.model_validate(book) for book in books]
    
    def get_total_books_count(self, db: Session) -> int:
        """Get the total count of books in the system.
        
        Args:
            db: Database session
            
        Returns:
            Total number of books
            
        Example:
            >>> service = BookService()
            >>> count = service.get_total_books_count(db)
        """
        count = self.repository.count(db)
        logger.info(f"Total books count: {count}")
        return count

    # Generate a get_available_books method that queries the repository for books with available_copies > 0 and returns a list of BookResponse schemas.
    def get_available_books(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[BookResponse]:
        """Retrieve all books with available copies.
        
        Filters books where available_copies > 0, useful for displaying
        books that can currently be borrowed.
        
        Args:
            db: Database session
            skip: Number of records to skip (offset)
            limit: Maximum number of records to return
            
        Returns:
            List of BookResponse objects for books with available_copies > 0
            
        Example:
            >>> service = BookService()
            >>> available_books = service.get_available_books(db, skip=0, limit=10)
        """
        logger.info(f"Fetching available books with skip={skip}, limit={limit}")
        
        books = self.repository.find_available_books(db, skip=skip, limit=limit)
        logger.debug(f"Found {len(books)} available books")
        
        return [BookResponse.model_validate(book) for book in books]