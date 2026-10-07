# Library Management System - Frontend

## AddBookForm Component

A React TypeScript component for adding new books to the library management system via the FastAPI backend.

## Features

- ✅ **Type-Safe**: Full TypeScript support with comprehensive interfaces
- ✅ **Form Validation**: Client-side and server-side validation
- ✅ **Error Handling**: Comprehensive error handling for 400, 409, and 500 status codes
- ✅ **Accessibility**: ARIA attributes for screen readers
- ✅ **Responsive Design**: Mobile-friendly UI
- ✅ **Native Fetch API**: No external HTTP library dependencies
- ✅ **Real-time Feedback**: Field-level error messages and success notifications

## Installation

```bash
# Install dependencies (if using npm)
npm install react react-dom
npm install --save-dev typescript @types/react @types/react-dom

# Or with yarn
yarn add react react-dom
yarn add --dev typescript @types/react @types/react-dom
```

## Usage

```tsx
import AddBookForm from './components/AddBookForm';

function App() {
  return (
    <div className="App">
      <AddBookForm />
    </div>
  );
}

export default App;
```

## API Integration

### Endpoint
- **URL**: `http://localhost:8000/api/books`
- **Method**: `POST`
- **Content-Type**: `application/json`

### Request Body

```json
{
  "isbn": "978-0-13-468599-1",
  "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
  "author": "Robert C. Martin",
  "genre": "Software Engineering",
  "total_copies": 5
}
```

### Response Codes

| Status Code | Description | Action |
|-------------|-------------|--------|
| **201** | Book created successfully | Show success message, reset form |
| **400** | Validation error | Display field-level errors |
| **409** | Duplicate ISBN | Show "ISBN already exists" error |
| **500** | Server error | Show generic error message |

## Field Validation

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `isbn` | string | Yes | Non-empty, alphanumeric with hyphens, max 50 chars |
| `title` | string | Yes | Non-empty, max 255 chars |
| `author` | string | Yes | Non-empty, max 255 chars |
| `genre` | string | No | Max 100 chars |
| `total_copies` | number | Yes | Minimum value: 1 |

## Error Handling

### 400 Bad Request (Validation Errors)

The component displays field-level validation errors:

```json
{
  "error": "Validation Error",
  "message": "Request validation failed",
  "details": [
    {
      "field": "title",
      "message": "Title is required and cannot be empty"
    },
    {
      "field": "total_copies",
      "message": "Total copies must be a positive integer"
    }
  ]
}
```

### 409 Conflict (Duplicate ISBN)

Shows error message: **"A book with this ISBN already exists."**

### 500 Internal Server Error

Shows generic error: **"An unexpected server error occurred. Please try again later."**

## Component Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── AddBookForm.tsx      # Main component
│   │   └── AddBookForm.css      # Component styles
│   └── types/
│       └── types.ts             # TypeScript type definitions
└── README.md
```

## TypeScript Types

All types are defined in `src/types/types.ts`:

- `BookRequest`: API request payload
- `BookResponse`: API response structure
- `ErrorResponse`: API error format
- `ValidationError`: Field-level validation error
- `BookFormData`: Internal form state
- `API_CONFIG`: API configuration constants
- `HttpStatus`: HTTP status code enum

## Accessibility

- All form fields have proper `aria-label` attributes
- Error messages use `aria-describedby` and `role="alert"`
- Required fields marked with `aria-required="true"`
- Invalid fields marked with `aria-invalid="true"`
- Submit button shows loading state with `aria-busy`

## Styling

The component uses a clean, modern design with:

- Form validation states (success/error)
- Responsive layout (mobile-friendly)
- Smooth animations
- Disabled states during submission
- Clear visual feedback

### Customization

Modify `AddBookForm.css` to customize colors, spacing, and styles:

```css
/* Primary button color */
.btn-primary {
  background-color: #007bff; /* Change this */
}

/* Error color */
.input-error {
  border-color: #dc3545; /* Change this */
}
```

## Backend Requirements

Ensure the FastAPI backend is running:

```bash
# From the backend directory
uvicorn app.main:app --reload --port 8000
```

### CORS Configuration

The FastAPI backend must allow CORS for the frontend:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Development

1. **Start the FastAPI backend:**
   ```bash
   cd path/to/backend
   uvicorn app.main:app --reload --port 8000
   ```

2. **Start your React development server:**
   ```bash
   cd frontend
   npm start
   ```

3. **Access the form:**
   Navigate to `http://localhost:3000` in your browser

## Testing

### Manual Testing Checklist

- [ ] Submit valid book data → Success message appears, form resets
- [ ] Submit with empty required fields → Field-level errors shown
- [ ] Submit with duplicate ISBN → "ISBN already exists" error
- [ ] Submit with `total_copies` < 1 → Validation error
- [ ] Submit while backend is down → Network error message
- [ ] Test on mobile device → Responsive layout works
- [ ] Test with screen reader → ARIA attributes work correctly

## Best Practices Followed

✅ **TypeScript**: Full type safety with interfaces  
✅ **SOLID Principles**: Single Responsibility Principle  
✅ **DRY**: Reusable type definitions  
✅ **Accessibility**: WCAG 2.1 compliant  
✅ **Performance**: No unnecessary re-renders  
✅ **Security**: Input sanitization (trim whitespace)  
✅ **Error Handling**: Comprehensive error states  
✅ **User Experience**: Real-time feedback, loading states  

## Troubleshooting

### CORS Errors

**Problem**: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Solution**: Add CORS middleware to FastAPI backend (see Backend Requirements)

### Network Errors

**Problem**: "Network error: Failed to fetch"

**Solution**: Ensure backend is running at `http://localhost:8000`

### Type Errors

**Problem**: TypeScript compilation errors

**Solution**: Ensure all types are imported from `src/types/types.ts`

## License

MIT

## Support

For issues or questions, please refer to the main project documentation.