"""Book response schema for API responses.

Defines the structure of book data returned from API endpoints.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class BookResponse(BaseModel):
    """Response schema for book data.
    
    Returned when creating or retrieving a book.
    
    Attributes:
        id: Unique identifier for the book
        isbn: International Standard Book Number
        title: Book title
        author: Author name
        genre: Book genre/category (may be None)
        available_copies: Number of copies available for loan
        total_copies: Total number of copies in the library
        created_at: Timestamp when the book was created
        updated_at: Timestamp when the book was last updated
    """
    
    id: int = Field(
        ...,
        description="Unique identifier for the book",
        examples=[101]
    )
    
    isbn: str = Field(
        ...,
        description="International Standard Book Number",
        examples=["978-0-13-468599-1"]
    )
    
    title: str = Field(
        ...,
        description="Title of the book",
        examples=["Clean Code: A Handbook of Agile Software Craftsmanship"]
    )
    
    author: str = Field(
        ...,
        description="Author name",
        examples=["Robert C. Martin"]
    )
    
    genre: Optional[str] = Field(
        None,
        description="Genre/category of the book",
        examples=["Software Engineering"]
    )
    
    available_copies: int = Field(
        ...,
        description="Number of copies currently available for loan",
        examples=[5]
    )
    
    total_copies: int = Field(
        ...,
        description="Total number of copies in the library",
        examples=[5]
    )
    
    created_at: datetime = Field(
        ...,
        description="Timestamp when the book was created (ISO 8601 format)",
        examples=["2026-10-06T10:30:00Z"]
    )
    
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the book was last updated (ISO 8601 format)",
        examples=["2026-10-06T10:30:00Z"]
    )
    
    model_config = ConfigDict(
        from_attributes=True,  # Enable ORM mode (Pydantic v2)
        json_encoders={
            datetime: lambda v: v.isoformat()  # Serialize datetime to ISO 8601
        },
        json_schema_extra={
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
    )
