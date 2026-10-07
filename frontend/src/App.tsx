import React, { useState } from 'react';
import AddBookForm from './components/AddBookForm';
import BookCatalog from './components/BookCatalog';
import './App.css';

type Page = 'catalog' | 'add';

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('catalog');

  return (
    <div className="App">
      <header className="App-header">
        <h1>Library Management System</h1>
        <p>A classical approach to cataloguing knowledge</p>
        
        <nav className="main-navigation">
          <button
            className={`nav-btn ${currentPage === 'catalog' ? 'active' : ''}`}
            onClick={() => setCurrentPage('catalog')}
          >
            Browse Collection
          </button>
          <button
            className={`nav-btn ${currentPage === 'add' ? 'active' : ''}`}
            onClick={() => setCurrentPage('add')}
          >
            Add Volume
          </button>
        </nav>
      </header>

      <main>
        {currentPage === 'catalog' ? <BookCatalog /> : <AddBookForm />}
      </main>

      <footer className="App-footer">
        <p>&copy; {new Date().getFullYear()} Library Management System</p>
      </footer>
    </div>
  );
}

export default App;