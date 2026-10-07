/**
 * Central export point for all TypeScript types
 * Allows clean imports: import { BookRequest, BookResponse } from 'types'
 */

export type {
  BookRequest,
  BookResponse,
  ValidationError,
  ErrorResponse,
  BookFormData,
} from './types';

export { API_CONFIG, HttpStatus } from './types';