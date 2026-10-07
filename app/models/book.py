"""Book SQLAlchemy ORM model.

Defines the Book entity with all required fields and constraints.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func

from app.database.session import Base


class Book(Base):
    """Book entity representing a book in the library management system.
    
    Attributes:
        id: Unique identifier (primary key)
        isbn: International Standard Book Number (unique)
        title: Book title
        author: Author name
        genre: Book genre/category (optional)
        available_copies: Number of copies available for loan
        total_copies: Total number of copies in the library
        created_at: Timestamp when the book was added
        updated_at: Timestamp when the book was last modified
    """
    
    __tablename__ = "books"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Book information
    isbn = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="International Standard Book Number (unique identifier)"
    )
    title = Column(
        String(255),
        nullable=False,
        comment="Title of the book"
    )
    author = Column(
        String(255),
        nullable=False,
        comment="Author name"
    )
    genre = Column(
        String(100),
        nullable=True,
        comment="Genre/category of the book"
    )
    
    # Copy tracking
    available_copies = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Number of copies currently available for loan"
    )
    total_copies = Column(
        Integer,
        nullable=False,
        comment="Total number of copies in the library"
    )
    
    # Timestamps (automatically managed)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        comment="Timestamp when the book was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="Timestamp when the book was last updated"
    )
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_isbn', 'isbn'),  # Fast ISBN lookups
        Index('idx_title', 'title'),  # Search by title
        Index('idx_author', 'author'),  # Search by author
    )
    
    def __repr__(self) -> str:
        """String representation of the Book instance."""
        return (
            f"<Book(id={self.id}, isbn='{self.isbn}', title='{self.title}', "
            f"author='{self.author}', available={self.available_copies}/{self.total_copies})>"
        )
