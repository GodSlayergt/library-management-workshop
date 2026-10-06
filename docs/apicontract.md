 # Library Management System - REST API Contract

## Add Book Feature

### Endpoint: Add a New Book

**HTTP Method:** `POST`

**Path:** `/api/books`

**Description:** Creates a new book record in the library management system.

---

### Request

#### Headers
    ```
    Content-Type: application/json
    ```

#### Request Body Schema

| Field            | Type     | Required | Description                                      | Validation Rules                                    |
|------------------|----------|----------|--------------------------------------------------|-----------------------------------------------------|
| `isbn`           | string   | Yes      | International Standard Book Number               | Must be unique, non-empty, alphanumeric with hyphens allowed |
| `title`          | string   | Yes      | Title of the book                                | Non-empty, max length 255 characters                |
| `author`         | string   | Yes      | Author name                                      | Non-empty, max length 255 characters                |
| `genre`          | string   | No       | Genre/category of the book                       | Max length 100 characters                           |
| `total_copies`   | integer  | Yes      | Total number of copies available in the library  | Must be a positive integer (≥ 1)                    |

#### Example Request Body
    ```json
    {
      "isbn": "978-0-13-468599-1",
      "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
      "author": "Robert C. Martin",
      "genre": "Software Engineering",
      "total_copies": 5
    }
    ```

---

### Response

#### Success Response (201 Created)

**Status Code:** `201 Created`

**Response Body Schema:**

| Field              | Type     | Description                                      |
|--------------------|----------|--------------------------------------------------|
| `id`               | integer  | Unique identifier for the book                   |
| `isbn`             | string   | International Standard Book Number               |
| `title`            | string   | Title of the book                                |
| `author`           | string   | Author name                                      |
| `genre`            | string   | Genre/category of the book                       |
| `available_copies` | integer  | Number of copies currently available for loan    |
| `total_copies`     | integer  | Total number of copies in the library            |
| `created_at`       | string   | Timestamp when the book was created (ISO 8601)   |
| `updated_at`       | string   | Timestamp when the book was last updated (ISO 8601) |

#### Example Success Response
    ```json
    {
      "id": 101,
      "isbn": "978-0-13-468599-1",
      "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
      "author": "Robert C. Martin",
      "genre": "Software Engineering",
      "available_copies": 5,
      "total_copies": 5,
      "created_at": "2026-10-06T10:30:00Z",
      "updated_at": "2026-10-06T10:30:00Z"
    }
    ```

---

#### Error Responses

##### 400 Bad Request
**Description:** Invalid request body or validation failure.

**Example Response:**
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

##### 409 Conflict
**Description:** A book with the same ISBN already exists.

**Example Response:**
    ```json
    {
      "error": "Duplicate Resource",
      "message": "A book with ISBN '978-0-13-468599-1' already exists in the system"
    }
    ```

##### 500 Internal Server Error
**Description:** Unexpected server error.

**Example Response:**
    ```json
    {
      "error": "Internal Server Error",
      "message": "An unexpected error occurred while processing your request. Please try again later."
    }
    ```

---

### cURL Example

    ```bash
    curl -X POST http://localhost:8080/api/books \
      -H "Content-Type: application/json" \
      -d '{
        "isbn": "978-0-13-468599-1",
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "author": "Robert C. Martin",
        "genre": "Software Engineering",
        "total_copies": 5
      }'
    ```

---

### Business Rules

1. **Automatic Available Copies:** When a new book is added, `available_copies` is automatically set equal to `total_copies`.
2. **ISBN Uniqueness:** The system enforces uniqueness on the `isbn` field. Attempting to add a book with a duplicate ISBN will result in a `409 Conflict` response.
3. **Timestamps:** The `created_at` and `updated_at` fields are automatically populated by the system.
4. **Minimum Copies:** At least one copy (`total_copies ≥ 1`) must be specified when adding a book.

---

### Notes

- All timestamps follow the ISO 8601 format (e.g., `2026-10-06T10:30:00Z`).
- The `genre` field is optional and can be omitted from the request.
- The API returns the complete book object upon successful creation, including system-generated fields (`id`, `created_at`, `updated_at`, `available_copies`).