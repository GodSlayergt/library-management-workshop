"""Book request schema for POST /api/books endpoint.

Defines validation rules for creating a new book.
"""

import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict


class BookRequest(BaseModel):
    """Request schema for creating a new book.
    
    Attributes:
        isbn: International Standard Book Number (required, unique)
        title: Book title (required, max 255 chars)
        author: Author name (required, max 255 chars)
        genre: Book genre/category (optional, max 100 chars)
        total_copies: Total number of copies (required, minimum 1)
    """
    
    isbn: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="International Standard Book Number (ISBN)",
        examples=["978-0-13-468599-1", "978-0134685991"]
    )
    
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Title of the book",
        examples=["Clean Code: A Handbook of Agile Software Craftsmanship"]
    )
    
    author: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Author name",
        examples=["Robert C. Martin"]
    )
    
    genre: Optional[str] = Field(
        None,
        max_length=100,
        description="Genre/category of the book",
        examples=["Software Engineering", "Fiction", "Science"]
    )
    
    total_copies: int = Field(
        ...,
        ge=1,
        description="Total number of copies in the library (must be at least 1)",
        examples=[5, 10]
    )
    
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Automatically strip whitespace from strings
        json_schema_extra={
            "example": {
                "isbn": "978-0-13-468599-1",
                "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
                "author": "Robert C. Martin",
                "genre": "Software Engineering",
                "total_copies": 5
            }
        }
    )
    
    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v: str) -> str:
        """Validate ISBN format.
        
        Ensures ISBN contains only alphanumeric characters and hyphens.
        
        Args:
            v: ISBN string to validate
            
        Returns:
            Validated ISBN string
            
        Raises:
            ValueError: If ISBN format is invalid
        """
        if not v or not v.strip():
            raise ValueError('ISBN cannot be empty')
        
        # ISBN should contain only alphanumeric characters and hyphens
        if not re.match(r'^[0-9A-Za-z\-]+$', v):
            raise ValueError(
                'ISBN must contain only alphanumeric characters and hyphens'
            )
        
        return v.strip()
    
    @field_validator('title', 'author')
    @classmethod
    def validate_required_string(cls, v: str, info) -> str:
        """Validate required string fields are not empty.
        
        Args:
            v: String value to validate
            info: Field validation context
            
        Returns:
            Validated string
            
        Raises:
            ValueError: If string is empty or only whitespace
        """
        if not v or not v.strip():
            field_name = info.field_name.replace('_', ' ').title()
            raise ValueError(f'{field_name} cannot be empty')
        
        return v.strip()
    
    @field_validator('genre')
    @classmethod
    def validate_genre(cls, v: Optional[str]) -> Optional[str]:
        """Validate genre field, strip whitespace if provided.
        
        Args:
            v: Genre string (optional)
            
        Returns:
            Validated genre string or None
        """
        if v is not None and v.strip():
            return v.strip()
        return None
