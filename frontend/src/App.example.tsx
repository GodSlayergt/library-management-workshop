/**
 * Example App.tsx file showing how to integrate AddBookForm
 * into a React application
 */

import React from 'react';
import AddBookForm from './components/AddBookForm';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Library Management System</h1>
        <p>Add books to your library catalog</p>
      </header>

      <main>
        <AddBookForm />
      </main>

      <footer className="App-footer">
        <p>&copy; 2026 Library Management System</p>
      </footer>
    </div>
  );
}

export default App;

/**
 * Optional: App.css for the example above
 * 
 * .App {
 *   min-height: 100vh;
 *   display: flex;
 *   flex-direction: column;
 *   background-color: #f5f5f5;
 * }
 * 
 * .App-header {
 *   background-color: #282c34;
 *   color: white;
 *   padding: 2rem;
 *   text-align: center;
 * }
 * 
 * .App-header h1 {
 *   margin: 0 0 0.5rem 0;
 *   font-size: 2.5rem;
 * }
 * 
 * .App-header p {
 *   margin: 0;
 *   font-size: 1.2rem;
 *   opacity: 0.8;
 * }
 * 
 * main {
 *   flex: 1;
 *   padding: 2rem 1rem;
 * }
 * 
 * .App-footer {
 *   background-color: #282c34;
 *   color: white;
 *   padding: 1rem;
 *   text-align: center;
 * }
 */