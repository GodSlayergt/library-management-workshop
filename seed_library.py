#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seed script to populate the library with sample books.

Adds a curated collection of classic and contemporary books across various genres.
Uses only Python standard library (no external dependencies).
"""

import json
import urllib.request
import urllib.error
import time
import sys
from typing import Dict, List, Tuple

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# API endpoint
API_URL = "http://localhost:8000/api/books"

# Sample books collection - organized by genre
SAMPLE_BOOKS: List[Dict] = [
    # Typography & Design
    {
        "isbn": "978-0-88179-206-5",
        "title": "The Elements of Typographic Style",
        "author": "Robert Bringhurst",
        "genre": "Typography & Design",
        "total_copies": 3
    },
    {
        "isbn": "978-1-56898-458-3",
        "title": "Thinking with Type",
        "author": "Ellen Lupton",
        "genre": "Typography & Design",
        "total_copies": 2
    },
    {
        "isbn": "978-0-9539938-0-8",
        "title": "Grid Systems in Graphic Design",
        "author": "Josef Müller-Brockmann",
        "genre": "Typography & Design",
        "total_copies": 2
    },
    
    # Software Engineering
    {
        "isbn": "978-0-13-468599-1",
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "author": "Robert C. Martin",
        "genre": "Software Engineering",
        "total_copies": 5
    },
    {
        "isbn": "978-0-13-475759-9",
        "title": "Clean Architecture",
        "author": "Robert C. Martin",
        "genre": "Software Engineering",
        "total_copies": 4
    },
    {
        "isbn": "978-0-13-597783-2",
        "title": "The Pragmatic Programmer",
        "author": "David Thomas & Andrew Hunt",
        "genre": "Software Engineering",
        "total_copies": 3
    },
    {
        "isbn": "978-0-13-235088-4",
        "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
        "author": "Gang of Four",
        "genre": "Software Engineering",
        "total_copies": 2
    },
    {
        "isbn": "978-0-13-475940-1",
        "title": "Refactoring: Improving the Design of Existing Code",
        "author": "Martin Fowler",
        "genre": "Software Engineering",
        "total_copies": 3
    },
    
    # Classic Literature
    {
        "isbn": "978-0-14-143951-8",
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "genre": "Classic Literature",
        "total_copies": 4
    },
    {
        "isbn": "978-0-14-144930-2",
        "title": "1984",
        "author": "George Orwell",
        "genre": "Classic Literature",
        "total_copies": 5
    },
    {
        "isbn": "978-0-14-027526-3",
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "genre": "Classic Literature",
        "total_copies": 3
    },
    {
        "isbn": "978-0-14-118280-3",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "genre": "Classic Literature",
        "total_copies": 4
    },
    {
        "isbn": "978-0-14-303943-3",
        "title": "Moby-Dick",
        "author": "Herman Melville",
        "genre": "Classic Literature",
        "total_copies": 2
    },
    
    # Science Fiction
    {
        "isbn": "978-0-44-100590-1",
        "title": "Dune",
        "author": "Frank Herbert",
        "genre": "Science Fiction",
        "total_copies": 6
    },
    {
        "isbn": "978-0-55-338256-3",
        "title": "Foundation",
        "author": "Isaac Asimov",
        "genre": "Science Fiction",
        "total_copies": 3
    },
    {
        "isbn": "978-0-44-101477-4",
        "title": "Neuromancer",
        "author": "William Gibson",
        "genre": "Science Fiction",
        "total_copies": 2
    },
    {
        "isbn": "978-0-59-308536-4",
        "title": "The Martian",
        "author": "Andy Weir",
        "genre": "Science Fiction",
        "total_copies": 4
    },
    
    # Philosophy
    {
        "isbn": "978-0-14-044221-0",
        "title": "Meditations",
        "author": "Marcus Aurelius",
        "genre": "Philosophy",
        "total_copies": 3
    },
    {
        "isbn": "978-0-14-044792-5",
        "title": "The Republic",
        "author": "Plato",
        "genre": "Philosophy",
        "total_copies": 2
    },
    {
        "isbn": "978-0-14-243728-1",
        "title": "Beyond Good and Evil",
        "author": "Friedrich Nietzsche",
        "genre": "Philosophy",
        "total_copies": 2
    },
    
    # History
    {
        "isbn": "978-0-30-677857-3",
        "title": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "genre": "History",
        "total_copies": 5
    },
    {
        "isbn": "978-0-67-975600-4",
        "title": "Guns, Germs, and Steel",
        "author": "Jared Diamond",
        "genre": "History",
        "total_copies": 3
    },
    {
        "isbn": "978-1-47-367492-4",
        "title": "The History of the Ancient World",
        "author": "Susan Wise Bauer",
        "genre": "History",
        "total_copies": 2
    },
    
    # Biography
    {
        "isbn": "978-1-50-113251-3",
        "title": "Steve Jobs",
        "author": "Walter Isaacson",
        "genre": "Biography",
        "total_copies": 4
    },
    {
        "isbn": "978-0-67-944232-6",
        "title": "Leonardo da Vinci",
        "author": "Walter Isaacson",
        "genre": "Biography",
        "total_copies": 3
    },
    {
        "isbn": "978-0-14-303943-7",
        "title": "The Diary of a Young Girl",
        "author": "Anne Frank",
        "genre": "Biography",
        "total_copies": 3
    },
    
    # Business & Economics
    {
        "isbn": "978-0-06-256541-9",
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "genre": "Business & Economics",
        "total_copies": 4
    },
    {
        "isbn": "978-0-06-201666-9",
        "title": "Good to Great",
        "author": "Jim Collins",
        "genre": "Business & Economics",
        "total_copies": 3
    },
    {
        "isbn": "978-1-59-184789-1",
        "title": "The Lean Startup",
        "author": "Eric Ries",
        "genre": "Business & Economics",
        "total_copies": 4
    },
]


def add_book(book: Dict) -> Tuple[bool, str]:
    """Add a single book to the library.
    
    Args:
        book: Dictionary containing book details
        
    Returns:
        Tuple of (success: bool, status: str)
    """
    try:
        # Prepare request
        data = json.dumps(book).encode('utf-8')
        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        # Make request
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 201:
                result = json.loads(response.read().decode('utf-8'))
                print(f"[OK] Added: {book['title']} by {book['author']} (ID: {result['id']})")
                return True, "success"
            else:
                print(f"[FAIL] {book['title']} - Status {response.status}")
                return False, "failed"
                
    except urllib.error.HTTPError as e:
        if e.code == 409:
            print(f"[SKIP] Duplicate: {book['title']} (ISBN already exists)")
            return False, "duplicate"
        else:
            error_msg = e.read().decode('utf-8') if e.fp else str(e)
            print(f"[ERROR] HTTP {e.code}: {book['title']}")
            return False, "failed"
    except urllib.error.URLError:
        print(f"[ERROR] Connection failed: Cannot connect to API")
        return False, "connection_error"
    except Exception as e:
        print(f"[ERROR] {book['title']}: {str(e)}")
        return False, "failed"


def check_api_health() -> bool:
    """Check if the API is accessible.
    
    Returns:
        True if API is healthy, False otherwise
    """
    try:
        req = urllib.request.Request("http://localhost:8000/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status == 200
    except:
        return False


def main():
    """Main function to seed the library."""
    print("="*70)
    print("Library Seeding Script")
    print("="*70)
    print(f"Target API: {API_URL}")
    print(f"Total books to add: {len(SAMPLE_BOOKS)}")
    print("="*70)
    print()
    
    # Check if API is accessible
    print("Checking API health... ", end="")
    if check_api_health():
        print("[OK] API is accessible\n")
    else:
        print("[ERROR] Cannot reach API")
        print("\nPlease start the FastAPI server first:")
        print("  uvicorn app.main:app --reload --port 8000\n")
        return
    
    # Add books
    success_count = 0
    duplicate_count = 0
    failed_count = 0
    connection_error = False
    
    for i, book in enumerate(SAMPLE_BOOKS, 1):
        print(f"[{i}/{len(SAMPLE_BOOKS)}] ", end="")
        
        success, status = add_book(book)
        
        if success:
            success_count += 1
        elif status == "duplicate":
            duplicate_count += 1
        elif status == "connection_error":
            failed_count += 1
            connection_error = True
            break  # Stop if we can't connect
        else:
            failed_count += 1
        
        # Small delay to avoid overwhelming the API
        time.sleep(0.2)
    
    # Summary
    print()
    print("="*70)
    print("Summary")
    print("="*70)
    print(f"Successfully added: {success_count} books")
    print(f"Duplicates skipped: {duplicate_count} books")
    print(f"Failed: {failed_count} books")
    print(f"Total processed: {success_count + duplicate_count + failed_count} books")
    print("="*70)
    
    if connection_error:
        print("\n[WARNING] Stopped due to connection error.")
        print("Please ensure the FastAPI server is running.")
    elif success_count > 0:
        print("\n[SUCCESS] The library has been populated with sample books!")
        print("Visit http://localhost:3000 to browse the collection.")
    
    print()


if __name__ == "__main__":
    main()
