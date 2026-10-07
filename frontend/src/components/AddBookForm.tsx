import React, { useState, FormEvent, ChangeEvent } from 'react';
import { BookRequest, BookResponse, ErrorResponse, BookFormData, API_CONFIG, HttpStatus } from '../types/types';
import './AddBookForm.css';

const AddBookForm: React.FC = () => {
  // Form state
  const [formData, setFormData] = useState<BookFormData>({
    isbn: '',
    title: '',
    author: '',
    genre: '',
    totalCopies: '',
  });

  // UI state
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [successMessage, setSuccessMessage] = useState<string>('');
  const [generalError, setGeneralError] = useState<string>('');
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  // Handle input changes
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    
    setFormData(prev => ({
      ...prev,
      [name]: name === 'totalCopies' ? (value === '' ? '' : Number(value)) : value,
    }));

    // Clear field error when user starts typing
    if (fieldErrors[name]) {
      setFieldErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  // Reset form
  const resetForm = () => {
    setFormData({
      isbn: '',
      title: '',
      author: '',
      genre: '',
      totalCopies: '',
    });
    setFieldErrors({});
    setGeneralError('');
  };

  // Handle form submission
  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    // Clear previous messages
    setSuccessMessage('');
    setGeneralError('');
    setFieldErrors({});
    setIsSubmitting(true);

    try {
      // Prepare request payload
      const requestBody: BookRequest = {
        isbn: formData.isbn.trim(),
        title: formData.title.trim(),
        author: formData.author.trim(),
        total_copies: Number(formData.totalCopies),
      };

      // Include genre only if provided
      if (formData.genre.trim()) {
        requestBody.genre = formData.genre.trim();
      }

      // Make POST request to FastAPI backend
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.BOOKS}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      // Handle success (201 Created)
      if (response.status === HttpStatus.CREATED) {
        const data: BookResponse = await response.json();
        setSuccessMessage('Book added successfully');
        resetForm();
        
        // Auto-hide success message after 5 seconds
        setTimeout(() => setSuccessMessage(''), 5000);
        
        console.log('Book created:', data);
        return;
      }

      // Handle errors
      const errorData: ErrorResponse = await response.json();

      // Handle 400 Bad Request (Validation Errors)
      if (response.status === HttpStatus.BAD_REQUEST) {
        if (errorData.details && Array.isArray(errorData.details)) {
          // Map field-level validation errors
          const errors: Record<string, string> = {};
          errorData.details.forEach((detail) => {
            // Convert snake_case to camelCase for field names
            const fieldName = detail.field === 'total_copies' ? 'totalCopies' : detail.field;
            errors[fieldName] = detail.message;
          });
          setFieldErrors(errors);
        } else {
          setGeneralError(errorData.message || 'Request validation failed');
        }
        return;
      }

      // Handle 409 Conflict (Duplicate ISBN)
      if (response.status === HttpStatus.CONFLICT) {
        setGeneralError('A book with this ISBN already exists.');
        setFieldErrors({ isbn: 'This ISBN is already in the system' });
        return;
      }

      // Handle 500 Internal Server Error
      if (response.status === HttpStatus.INTERNAL_SERVER_ERROR) {
        setGeneralError(errorData.message || 'An unexpected server error occurred. Please try again later.');
        return;
      }

      // Handle other unexpected errors
      setGeneralError(`Unexpected error: ${response.status} ${response.statusText}`);
      
    } catch (error) {
      // Handle network errors or JSON parsing errors
      if (error instanceof Error) {
        setGeneralError(`Network error: ${error.message}. Please check if the server is running.`);
      } else {
        setGeneralError('An unexpected error occurred. Please try again.');
      }
      console.error('Error creating book:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="add-book-form-container">
      <h2>Catalogue Entry</h2>
      <p className="catalog-subtitle">Register a new volume to the collection</p>
      
      {/* Success Message */}
      {successMessage && (
        <div className="alert alert-success" role="alert">
          {successMessage}
        </div>
      )}

      {/* General Error Message */}
      {generalError && (
        <div className="alert alert-error" role="alert">
          {generalError}
        </div>
      )}

      <form onSubmit={handleSubmit} noValidate>
        {/* ISBN Field */}
        <div className="form-group">
          <label htmlFor="isbn">
            ISBN <span className="required">*</span>
          </label>
          <input
            type="text"
            id="isbn"
            name="isbn"
            value={formData.isbn}
            onChange={handleChange}
            placeholder="978-0-13-468599-1"
            required
            className={fieldErrors.isbn ? 'input-error' : ''}
            disabled={isSubmitting}
            aria-label="ISBN"
            aria-required="true"
            aria-invalid={!!fieldErrors.isbn}
            aria-describedby={fieldErrors.isbn ? 'isbn-error' : undefined}
          />
          {fieldErrors.isbn && (
            <span id="isbn-error" className="error-message" role="alert">
              {fieldErrors.isbn}
            </span>
          )}
        </div>

        {/* Title Field */}
        <div className="form-group">
          <label htmlFor="title">
            Title <span className="required">*</span>
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="The Elements of Typographic Style"
            maxLength={255}
            required
            className={fieldErrors.title ? 'input-error' : ''}
            disabled={isSubmitting}
            aria-label="Title"
            aria-required="true"
            aria-invalid={!!fieldErrors.title}
            aria-describedby={fieldErrors.title ? 'title-error' : undefined}
          />
          {fieldErrors.title && (
            <span id="title-error" className="error-message" role="alert">
              {fieldErrors.title}
            </span>
          )}
        </div>

        {/* Author Field */}
        <div className="form-group">
          <label htmlFor="author">
            Author <span className="required">*</span>
          </label>
          <input
            type="text"
            id="author"
            name="author"
            value={formData.author}
            onChange={handleChange}
            placeholder="Robert Bringhurst"
            maxLength={255}
            required
            className={fieldErrors.author ? 'input-error' : ''}
            disabled={isSubmitting}
            aria-label="Author"
            aria-required="true"
            aria-invalid={!!fieldErrors.author}
            aria-describedby={fieldErrors.author ? 'author-error' : undefined}
          />
          {fieldErrors.author && (
            <span id="author-error" className="error-message" role="alert">
              {fieldErrors.author}
            </span>
          )}
        </div>

        {/* Genre Field */}
        <div className="form-group">
          <label htmlFor="genre">Genre</label>
          <input
            type="text"
            id="genre"
            name="genre"
            value={formData.genre}
            onChange={handleChange}
            placeholder="Typography & Design"
            maxLength={100}
            className={fieldErrors.genre ? 'input-error' : ''}
            disabled={isSubmitting}
            aria-label="Genre"
            aria-invalid={!!fieldErrors.genre}
            aria-describedby={fieldErrors.genre ? 'genre-error' : undefined}
          />
          {fieldErrors.genre && (
            <span id="genre-error" className="error-message" role="alert">
              {fieldErrors.genre}
            </span>
          )}
        </div>

        {/* Total Copies Field */}
        <div className="form-group">
          <label htmlFor="totalCopies">
            Copies in Collection <span className="required">*</span>
          </label>
          <input
            type="number"
            id="totalCopies"
            name="totalCopies"
            value={formData.totalCopies}
            onChange={handleChange}
            placeholder="5"
            min="1"
            required
            className={fieldErrors.totalCopies ? 'input-error' : ''}
            disabled={isSubmitting}
            aria-label="Total Copies"
            aria-required="true"
            aria-invalid={!!fieldErrors.totalCopies}
            aria-describedby={fieldErrors.totalCopies ? 'totalCopies-error' : undefined}
          />
          {fieldErrors.totalCopies && (
            <span id="totalCopies-error" className="error-message" role="alert">
              {fieldErrors.totalCopies}
            </span>
          )}
        </div>

        {/* Form Actions */}
        <div className="form-actions">
          <button
            type="submit"
            className="btn btn-primary"
            disabled={isSubmitting}
            aria-busy={isSubmitting}
          >
            {isSubmitting ? 'Cataloguing...' : 'Add to Collection'}
          </button>
          
          <button
            type="button"
            className="btn btn-secondary"
            onClick={resetForm}
            disabled={isSubmitting}
          >
            Clear Form
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddBookForm;