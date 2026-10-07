"""Book repository for database operations.

Implements the Repository pattern to encapsulate data access logic.
"""

from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.book import Book


class BookRepository:
    """Repository for Book entity database operations.
    
    Encapsulates all database queries and commands for the Book entity,
    providing a clean interface for the service layer.
    """
    
    @staticmethod
    def create(db: Session, book_data: dict) -> Book:
        """Create a new book record in the database.
        
        Args:
            db: Database session
            book_data: Dictionary containing book fields
            
        Returns:
            Book: Created Book instance with generated ID and timestamps
            
        Raises:
            SQLAlchemyError: If database operation fails
            
        Example:
            >>> book_data = {
            ...     "isbn": "978-0-13-468599-1",
            ...     "title": "Clean Code",
            ...     "author": "Robert C. Martin",
            ...     "genre": "Software Engineering",
            ...     "total_copies": 5,
            ...     "available_copies": 5
            ... }
            >>> book = BookRepository.create(db, book_data)
        """
        try:
            book = Book(**book_data)
            db.add(book)
            db.commit()
            db.refresh(book)  # Refresh to get generated ID and timestamps
            return book
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    @staticmethod
    def find_by_id(db: Session, book_id: int) -> Optional[Book]:
        """Find a book by its ID.
        
        Args:
            db: Database session
            book_id: Unique identifier of the book
            
        Returns:
            Book instance if found, None otherwise
            
        Example:
            >>> book = BookRepository.find_by_id(db, 101)
        """
        return db.query(Book).filter(Book.id == book_id).first()
    
    @staticmethod
    def find_by_isbn(db: Session, isbn: str) -> Optional[Book]:
        """Find a book by its ISBN.
        
        Args:
            db: Database session
            isbn: International Standard Book Number
            
        Returns:
            Book instance if found, None otherwise
            
        Example:
            >>> book = BookRepository.find_by_isbn(db, "978-0-13-468599-1")
        """
        return db.query(Book).filter(Book.isbn == isbn).first()
    
    @staticmethod
    def find_all(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
        """Retrieve all books with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip (offset)
            limit: Maximum number of records to return
            
        Returns:
            List of Book instances
            
        Example:
            >>> books = BookRepository.find_all(db, skip=0, limit=10)
        """
        return db.query(Book).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, book: Book, update_data: dict) -> Book:
        """Update an existing book record.
        
        Args:
            db: Database session
            book: Book instance to update
            update_data: Dictionary of fields to update
            
        Returns:
            Updated Book instance
            
        Raises:
            SQLAlchemyError: If database operation fails
            
        Example:
            >>> book = BookRepository.find_by_id(db, 101)
            >>> updated_book = BookRepository.update(db, book, {"total_copies": 10})
        """
        try:
            for key, value in update_data.items():
                if hasattr(book, key):
                    setattr(book, key, value)
            db.commit()
            db.refresh(book)
            return book
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    @staticmethod
    def delete(db: Session, book: Book) -> bool:
        """Delete a book record from the database.
        
        Args:
            db: Database session
            book: Book instance to delete
            
        Returns:
            True if deletion was successful
            
        Raises:
            SQLAlchemyError: If database operation fails
            
        Example:
            >>> book = BookRepository.find_by_id(db, 101)
            >>> BookRepository.delete(db, book)
        """
        try:
            db.delete(book)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    @staticmethod
    def count(db: Session) -> int:
        """Count total number of books in the database.
        
        Args:
            db: Database session
            
        Returns:
            Total count of books
            
        Example:
            >>> total_books = BookRepository.count(db)
        """
        return db.query(Book).count()

    # created with get available books method in the book_service
    def find_available_books(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Book]:
        """Query books with available_copies > 0.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Book entities with available copies
        """
        return (
            db.query(Book)
            .filter(Book.available_copies > 0)
            .offset(skip)
            .limit(limit)
            .all()
        )