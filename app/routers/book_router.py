"""Book router for API endpoints.

Defines all book-related API endpoints following REST conventions.
"""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.request.book_request import BookRequest
from app.schemas.response.book_response import BookResponse
from app.services.book_service import BookService

# Configure logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/books",
    tags=["books"],
    responses={
        400: {"description": "Bad Request - Invalid input data"},
        409: {"description": "Conflict - Resource already exists"},
        500: {"description": "Internal Server Error"},
    },
)

# Service instance
book_service = BookService()


@router.post(
    "",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new book",
    description="Creates a new book record in the library management system. "
                "The ISBN must be unique, and available_copies will be automatically "
                "set equal to total_copies.",
    response_description="Successfully created book with generated ID and timestamps",
    responses={
        201: {
            "description": "Book created successfully",
            "content": {
                "application/json": {
                    "example": {
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
                }
            }
        },
        400: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Validation Error",
                        "message": "Request validation failed",
                        "details": [
                            {
                                "field": "title",
                                "message": "Title is required and cannot be empty"
                            },
                            {
                                "field": "total_copies",
                                "message": "Total copies must be a positive integer"
                            }
                        ]
                    }
                }
            }
        },
        409: {
            "description": "Duplicate ISBN",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Duplicate Resource",
                        "message": "A book with ISBN '978-0-13-468599-1' already exists in the system"
                    }
                }
            }
        }
    }
)
async def create_book(
    request: BookRequest,
    db: Session = Depends(get_db)
) -> BookResponse:
    """Create a new book in the library system.
    
    This endpoint accepts book details and creates a new book record.
    The system automatically:
    - Validates all input fields
    - Checks for duplicate ISBN
    - Sets available_copies equal to total_copies
    - Generates unique ID and timestamps
    
    Args:
        request: BookRequest containing book details (isbn, title, author, etc.)
        db: Database session (injected via dependency)
        
    Returns:
        BookResponse: Created book with all fields including generated values
        
    Raises:
        400: If validation fails (invalid data format)
        409: If a book with the same ISBN already exists
        500: If an unexpected server error occurs
    """
    logger.info(f"POST /api/books - Creating book with ISBN: {request.isbn}")
    
    # Delegate business logic to service layer
    book_response = book_service.create_book(db, request)
    
    logger.info(
        f"Book created successfully: ID={book_response.id}, "
        f"ISBN={book_response.isbn}"
    )
    
    return book_response


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Get a book by ID",
    description="Retrieves a specific book by its unique identifier",
    response_description="Book details",
    responses={
        404: {"description": "Book not found"}
    }
)
async def get_book(
    book_id: int,
    db: Session = Depends(get_db)
) -> BookResponse:
    """Get a book by its ID.
    
    Args:
        book_id: Unique identifier of the book
        db: Database session (injected via dependency)
        
    Returns:
        BookResponse: Book details
        
    Raises:
        404: If book not found
    """
    logger.info(f"GET /api/books/{book_id}")
    
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        logger.warning(f"Book not found: ID={book_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    
    return book


@router.get(
    "",
    response_model=List[BookResponse],
    summary="Get all books",
    description="Retrieves a paginated list of all books in the library",
    response_description="List of books"
)
async def get_all_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[BookResponse]:
    """Get all books with pagination.
    
    Args:
        skip: Number of records to skip (offset)
        limit: Maximum number of records to return
        db: Database session (injected via dependency)
        
    Returns:
        List[BookResponse]: List of books
    """
    logger.info(f"GET /api/books - skip={skip}, limit={limit}")
    
    books = book_service.get_all_books(db, skip=skip, limit=limit)
    
    logger.info(f"Returning {len(books)} books")
    return books
