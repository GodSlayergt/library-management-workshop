import React, { useState, useEffect, ChangeEvent } from 'react';
import { BookResponse, API_CONFIG, HttpStatus } from '../types/types';
import './BookCatalog.css';

interface CatalogFilters {
  searchTerm: string;
  filterType: 'all' | 'author' | 'genre';
}

const BookCatalog: React.FC = () => {
  // State
  const [books, setBooks] = useState<BookResponse[]>([]);
  const [filteredBooks, setFilteredBooks] = useState<BookResponse[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');
  const [filters, setFilters] = useState<CatalogFilters>({
    searchTerm: '',
    filterType: 'all',
  });

  // Fetch all books on mount
  useEffect(() => {
    fetchBooks();
  }, []);

  // Apply filters whenever books or filters change
  useEffect(() => {
    applyFilters();
  }, [books, filters]);

  const fetchBooks = async () => {
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.BOOKS}?limit=1000`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.status === HttpStatus.OK) {
        const data: BookResponse[] = await response.json();
        setBooks(data);
        console.log(`Fetched ${data.length} books`);
      } else {
        setError('Failed to fetch books from the library.');
      }
    } catch (err) {
      if (err instanceof Error) {
        setError(`Network error: ${err.message}. Please check if the server is running.`);
      } else {
        setError('An unexpected error occurred while fetching books.');
      }
      console.error('Error fetching books:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const applyFilters = () => {
    if (!filters.searchTerm.trim()) {
      setFilteredBooks(books);
      return;
    }

    const searchLower = filters.searchTerm.toLowerCase().trim();
    
    const filtered = books.filter(book => {
      switch (filters.filterType) {
        case 'author':
          return book.author.toLowerCase().includes(searchLower);
        case 'genre':
          return book.genre?.toLowerCase().includes(searchLower) ?? false;
        case 'all':
          return (
            book.title.toLowerCase().includes(searchLower) ||
            book.author.toLowerCase().includes(searchLower) ||
            book.genre?.toLowerCase().includes(searchLower) ||
            book.isbn.toLowerCase().includes(searchLower)
          );
        default:
          return true;
      }
    });

    setFilteredBooks(filtered);
  };

  const handleSearchChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFilters(prev => ({
      ...prev,
      searchTerm: e.target.value,
    }));
  };

  const handleFilterTypeChange = (type: 'all' | 'author' | 'genre') => {
    setFilters(prev => ({
      ...prev,
      filterType: type,
    }));
  };

  const handleRefresh = () => {
    fetchBooks();
  };

  const clearFilters = () => {
    setFilters({
      searchTerm: '',
      filterType: 'all',
    });
  };

  // Get unique authors and genres for quick filters
  const uniqueAuthors = Array.from(new Set(books.map(b => b.author))).sort();
  const uniqueGenres = Array.from(new Set(books.map(b => b.genre).filter(Boolean))).sort();

  return (
    <div className="book-catalog-container">
      <header className="catalog-header">
        <h2>Library Catalogue</h2>
        <p className="catalog-subtitle">Explore the collection by author or genre</p>
      </header>

      {/* Search and Filter Controls */}
      <div className="catalog-controls">
        <div className="search-section">
          <div className="filter-type-selector">
            <button
              className={`filter-btn ${filters.filterType === 'all' ? 'active' : ''}`}
              onClick={() => handleFilterTypeChange('all')}
            >
              All Fields
            </button>
            <button
              className={`filter-btn ${filters.filterType === 'author' ? 'active' : ''}`}
              onClick={() => handleFilterTypeChange('author')}
            >
              By Author
            </button>
            <button
              className={`filter-btn ${filters.filterType === 'genre' ? 'active' : ''}`}
              onClick={() => handleFilterTypeChange('genre')}
            >
              By Genre
            </button>
          </div>

          <div className="search-input-group">
            <input
              type="text"
              value={filters.searchTerm}
              onChange={handleSearchChange}
              placeholder={
                filters.filterType === 'author' ? 'Search by author name...' :
                filters.filterType === 'genre' ? 'Search by genre...' :
                'Search books, authors, genres, or ISBN...'
              }
              className="search-input"
              aria-label="Search books"
            />
            {filters.searchTerm && (
              <button onClick={clearFilters} className="clear-btn" aria-label="Clear search">
                ✕
              </button>
            )}
          </div>
        </div>

        <button onClick={handleRefresh} className="refresh-btn" disabled={isLoading}>
          {isLoading ? 'Refreshing...' : 'Refresh Collection'}
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="catalog-alert catalog-error" role="alert">
          {error}
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="catalog-loading">
          <div className="loading-spinner"></div>
          <p>Retrieving volumes from the archives...</p>
        </div>
      )}

      {/* Results Summary */}
      {!isLoading && (
        <div className="results-summary">
          <p>
            {filteredBooks.length === 0 && books.length === 0 ? (
              'The library catalogue is currently empty.'
            ) : filteredBooks.length === 0 && books.length > 0 ? (
              `No volumes found matching your search. Total collection: ${books.length} volumes.`
            ) : filters.searchTerm ? (
              `Found ${filteredBooks.length} volume${filteredBooks.length !== 1 ? 's' : ''} matching "${filters.searchTerm}" (of ${books.length} total)`
            ) : (
              `Displaying ${filteredBooks.length} volume${filteredBooks.length !== 1 ? 's' : ''} in the collection`
            )}
          </p>
        </div>
      )}

      {/* Book List */}
      {!isLoading && filteredBooks.length > 0 && (
        <div className="book-grid">
          {filteredBooks.map((book) => (
            <div key={book.id} className="book-card">
              <div className="book-card-header">
                <h3 className="book-title">{book.title}</h3>
                <span className="book-id">№ {book.id}</span>
              </div>
              
              <div className="book-details">
                <div className="detail-row">
                  <span className="detail-label">Author</span>
                  <span className="detail-value">{book.author}</span>
                </div>
                
                {book.genre && (
                  <div className="detail-row">
                    <span className="detail-label">Genre</span>
                    <span className="detail-value">{book.genre}</span>
                  </div>
                )}
                
                <div className="detail-row">
                  <span className="detail-label">ISBN</span>
                  <span className="detail-value isbn">{book.isbn}</span>
                </div>
                
                <div className="copies-info">
                  <div className="copy-stat">
                    <span className="stat-label">Available</span>
                    <span className="stat-value available">{book.available_copies}</span>
                  </div>
                  <div className="copy-stat">
                    <span className="stat-label">Total</span>
                    <span className="stat-value total">{book.total_copies}</span>
                  </div>
                </div>
              </div>
              
              <div className="book-card-footer">
                <span className="catalog-date">
                  Catalogued {new Date(book.created_at).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {!isLoading && books.length === 0 && (
        <div className="empty-state">
          <p className="empty-message">The library shelves await their first volume.</p>
          <p className="empty-hint">Begin by adding books to the collection.</p>
        </div>
      )}

      {/* Quick Browse Sections */}
      {!isLoading && books.length > 0 && !filters.searchTerm && (
        <aside className="quick-browse">
          <section className="browse-section">
            <h4>Browse by Author</h4>
            <div className="browse-list">
              {uniqueAuthors.slice(0, 10).map(author => (
                <button
                  key={author}
                  className="browse-link"
                  onClick={() => setFilters({ filterType: 'author', searchTerm: author })}
                >
                  {author}
                </button>
              ))}
              {uniqueAuthors.length > 10 && (
                <span className="browse-more">+ {uniqueAuthors.length - 10} more authors</span>
              )}
            </div>
          </section>

          <section className="browse-section">
            <h4>Browse by Genre</h4>
            <div className="browse-list">
              {uniqueGenres.slice(0, 10).map(genre => (
                <button
                  key={genre}
                  className="browse-link"
                  onClick={() => setFilters({ filterType: 'genre', searchTerm: genre! })}
                >
                  {genre}
                </button>
              ))}
              {uniqueGenres.length > 10 && (
                <span className="browse-more">+ {uniqueGenres.length - 10} more genres</span>
              )}
            </div>
          </section>
        </aside>
      )}
    </div>
  );
};

export default BookCatalog;