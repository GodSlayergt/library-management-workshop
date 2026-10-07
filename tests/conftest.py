"""Pytest configuration and shared fixtures.

Provides common test fixtures and configuration for all tests.
"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.session import Base
from app.models.book import Book


@pytest.fixture
def mock_db_session():
    """Create a mock database session for testing.
    
    Returns:
        MagicMock: Mocked SQLAlchemy Session
    """
    return MagicMock(spec=Session)


@pytest.fixture
def sample_book_data():
    """Sample book data for testing.
    
    Returns:
        dict: Sample book data dictionary
    """
    return {
        "isbn": "978-0-13-468599-1",
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "author": "Robert C. Martin",
        "genre": "Software Engineering",
        "total_copies": 5,
        "available_copies": 5
    }


@pytest.fixture
def sample_book_instance():
    """Sample Book ORM instance for testing.
    
    Returns:
        Book: Sample Book model instance
    """
    book = Book(
        id=101,
        isbn="978-0-13-468599-1",
        title="Clean Code: A Handbook of Agile Software Craftsmanship",
        author="Robert C. Martin",
        genre="Software Engineering",
        total_copies=5,
        available_copies=5,
        created_at=datetime(2026, 10, 6, 10, 30, 0),
        updated_at=datetime(2026, 10, 6, 10, 30, 0)
    )
    return book


@pytest.fixture
def in_memory_db():
    """Create an in-memory SQLite database for integration testing.
    
    Yields:
        Session: SQLAlchemy session connected to in-memory database
    """
    # Create in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
