/**
 * TypeScript type definitions for the Library Management System
 * Book-related API types
 */

/**
 * Request payload for creating a new book
 * Matches the FastAPI BookRequest schema
 */
export interface BookRequest {
  /** International Standard Book Number (required, unique) */
  isbn: string;
  /** Book title (required, max 255 chars) */
  title: string;
  /** Author name (required, max 255 chars) */
  author: string;
  /** Genre/category (optional, max 100 chars) */
  genre?: string;
  /** Total number of copies (required, minimum 1) */
  total_copies: number;
}

/**
 * Response schema for book data
 * Matches the FastAPI BookResponse schema
 */
export interface BookResponse {
  /** Unique identifier for the book */
  id: number;
  /** International Standard Book Number */
  isbn: string;
  /** Book title */
  title: string;
  /** Author name */
  author: string;
  /** Genre/category (may be null) */
  genre: string | null;
  /** Number of copies currently available for loan */
  available_copies: number;
  /** Total number of copies in the library */
  total_copies: number;
  /** ISO 8601 timestamp when the book was created */
  created_at: string;
  /** ISO 8601 timestamp when the book was last updated */
  updated_at: string;
}

/**
 * Field-level validation error from API
 */
export interface ValidationError {
  /** Field name that failed validation */
  field: string;
  /** Human-readable error message */
  message: string;
  /** Error type (e.g., "value_error", "type_error") */
  type?: string;
}

/**
 * API error response structure
 */
export interface ErrorResponse {
  /** Error category (e.g., "Validation Error", "Duplicate Resource") */
  error: string;
  /** Human-readable error message */
  message: string;
  /** Field-level validation errors (only for 400 responses) */
  details?: ValidationError[];
}

/**
 * Form data structure (client-side only)
 * Uses camelCase for React/TypeScript conventions
 */
export interface BookFormData {
  isbn: string;
  title: string;
  author: string;
  genre: string;
  totalCopies: number | '';
}

/**
 * API configuration
 */
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000',
  ENDPOINTS: {
    BOOKS: '/api/books',
  },
} as const;

/**
 * HTTP Status codes used in the API
 */
export enum HttpStatus {
  OK = 200,
  CREATED = 201,
  BAD_REQUEST = 400,
  CONFLICT = 409,
  INTERNAL_SERVER_ERROR = 500,
}