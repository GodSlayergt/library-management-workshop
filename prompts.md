# SDE Training

**Slingshot Guide**: https://docs-slingshot.sapientaiproducts.com/vscode/

## System Design

### 1. Generate an ER Diagram
Generate an entity-relationship diagram in Mermaid format for a Library Management System. Entities: Book (id, isbn, title, author, genre, available_copies, total_copies, created_at, updated_at), Member (id, name, email, phone, status, created_at), Loan (id, book_id, member_id, issue_date, due_date, return_date, status). Show all relationships and cardinality.

### 2. Generate a REST API Contract
Using the ER diagram above, generate a complete REST API contract in Markdown for the Library Management System. Focus only on the Add Book feature for now: POST /api/books. Include: HTTP method, path, request body JSON schema with field descriptions and validation rules, success response (201 Created with response body), error responses (400, 409, 500) with example JSON, and a curl example. Save in a code block. 

### 3. Generate backend project structure
Suggest a clean fast api project package structure for a Library Management REST API.  Use fast api and python to create layered architecture: routers, service, repository, model/entity, schemas/request, schemas/response, exception, config. Show the full folder tree with filenames and a one-line description of each file.


## 4. Development

**Repository for Agent Skils**
- https://github.com/anthropics/skills/tree/main/skills/frontend-design

### 5. Agent Hooks

**Create Hook 1 — Service Quality Review**
•	Title: Review Service on Save
•	Description: Automatically review service modules for quality issues
•	Event type: Save
•	File path pattern: services/**
•	Debounce: 500ms
•	Agent Prompt: Review this FastAPI service module. Check for: missing input validation, incorrect exception handling, business logic gaps, improper async usage, and opportunities to improve readability or maintainability. Report any issues found as a numbered list.
•	Click AI Enhance Prompt to let Slingshot improve your prompt automatically.

**Create Hook 2 — Router Validation Check:**
•	Title: Validate Router on Save
•	Event type: Save
•	File path pattern: routers/**
•	Debounce: 500ms
•	Agent Prompt: Review this FastAPI router. Check: correct HTTP status codes, request and response schema usage, dependency injection patterns, error handling, route design consistency, and API contract compliance with docs/api-contract.md.


### 6. Local Prompt:

name: "fastapi-endpoint"
description: "Generate a complete FastAPI REST endpoint with router, service, repository, schemas, and exception handling"
category: "backend/python"
tags: ["python", "fastapi", "rest", "sqlalchemy"]

Generate a complete FastAPI REST endpoint for the feature: <feature-name>.Entity fields: <entity-fields>.Use a layered architecture with:- routers- services- repositories- models/entities- schemas/request- schemas/response- exceptions- configInclude:- FastAPI APIRouter endpoint(s)- SQLAlchemy model/entity- Repository layer- Service layer- Pydantic request and response schemas with validation- Appropriate HTTPException handling- Custom exception entry if applicable- Dependency injection for database 

### 7. Build Backend Prompt

Using the API contract in docs/api-contract.md, create the complete FastAPI backend for the "Add a New Book" feature (POST /api/books).

Project structure:
app/
├── routers/
├── services/
├── repositories/
├── models/
├── schemas/request/
├── schemas/response/
├── exceptions/
├── config/
└── database/

Include:

- models/book.py
  - SQLAlchemy Book model with:
    - id
    - isbn
    - title
    - author
    - genre
    - available_copies
    - total_copies
    - created_at
    - updated_at

- repositories/book_repository.py
  - CRUD operations
  - find_by_isbn method

- schemas/request/book_request.py
  - Pydantic request schema
  - isbn: required
  - title: required
  - total_copies: minimum value 1
  - additional validation where appropriate

- schemas/response/book_response.py
  - Pydantic response schema

- services/book_service.py
  - create_book method
  - check for duplicate ISBN
  - set available_copies = total_copies
  - save book through repository
  - return response schema

- routers/book_router.py
  - POST /api/books endpoint
  - returns HTTP 201 Created
  - uses request validation
  - delegates business logic to service layer

- exceptions/duplicate_resource_exception.py
  - custom exception for duplicate ISBN

- exceptions/exception_handlers.py
  - handle validation errors → 400
  - DuplicateResourceException → 409
  - generic exceptions → 500

- database/session.py
  - SQLAlchemy engine and session management

- config/settings.py
  - application settings using Pydantic Settings
  - database configuration
  - API configuration

- main.py
  - FastAPI application bootstrap
  - router registration
  - exception handler registration
  - health endpoint

Use:
- FastAPI
- SQLAlchemy ORM
- Pydantic v2
- SQLite for development
- Dependency injection for database sessions

Add:
- GET /health endpoint
- OpenAPI / Swagger documentation
- Type hints throughout
- Pytest service-layer unit tests with mocked repository dependencies

Follow FastAPI, SQLAlchemy, and Pydantic best practices and maintain strict separation between router, service, repository, model, and schema layers.


### 8. Workspace:
- **Workspace Rag** : Where is the ISBN check implemented? Show me the method
- **Workspace Text** : find all @PostMapping annotations in the project

### 9. Inline Prompt
- **Above create_book**: #Explain what this method does and identify any edge cases not currently handled
- **Below create_book**: # Generate a get_available_books method that queries the repository for books with available_copies > 0 and returns a list of BookResponse schemas.
- **Multi-line Prompt**: 
    """  Add a Python docstring to create_book.
    Include:
    - Args
    - Returns
    - Raises DuplicateResourceException """

### 10. Connecting/Finalizing Prompts

- Using what already exists make it so I can run the python program. Add a main.py or txt if necessary and explain how to run it
- Move AddBookForm.tsx into a frontend folder so that it can be run with npm install and npm start

### 11. Slingshot-guidelines.md

  Slingshot Team Guidelines
  - Use Python type hints for all function parameters and return values
  - Use Pydantic schemas for all API request and response models
  - Keep business logic in the service layer; routers should only handle HTTP concerns
  - Never return SQLAlchemy entities directly from API endpoints — always return response schemas
  - Custom exceptions must inherit from Exception and include meaningful error messages
  - All service methods must include Python docstrings with Args, Returns, and Raises sections
  - Use dependency injection for database sessions in FastAPI routes and services
  - Follow FastAPI and SQLAlchemy best practices for validation, error handling, and data access
  - React components must use functional components with TypeScript interfaces for all props
  - API calls must handle loading, success, and error states explicitly
  - Use fetch() with proper error handling and strongly typed request/response models
  - Avoid duplicated business logic across routers, services, and repositories
  - Write Pytest unit tests for service-layer business logic

## Testing

### 12. QE API Agent
Use the API contract in docs/api-contract.md to test the POST /api/books endpoint running at http://localhost:8080/api/books. Generate and execute test scenarios: (1) Positive: POST with valid book data — expect 201 and the created book in response. (2) Negative: POST without title — expect 400 with validation error. (3) Negative: POST without isbn — expect 400. (4) Duplicate: POST the same book twice — second should return 409. Execute all tests and provide a detailed report with HTTP status codes, response bodies, and pass/fail status for each.

## Deploy

### 13. Docker File Prompt
Generate a multi-stage Dockerfile for the Library Management FastAPI application. Stage 1 (build): use python:3.12-slim, install dependencies from requirements.txt. Stage 2 (runtime): use python:3.12-slim, copy the application and installed dependencies, expose port 8000, and start the application with Uvicorn.

Also generate a docker-compose.yml that starts the app on port 8000 and maps the SQLite database directory as a volume.

Add a .dockerignore excluding .venv/, __pycache__/, .git/, and node_modules/.


# Day 2:

## Write Repository Document:
**System Prompt:** You are a senior technical documentation engineer. You create accurate, practical repository documentation based only on the files available in the checked-out repository. Do not invent setup steps, architecture details, commands, endpoints, or dependencies that are not supported by the repository contents. Prefer clear headings, concise explanations, and developer-friendly instructions.

**User Query:** Create a root-level file named exactly {{$var[documentationFile]s}} for the checked-out repository. Safety and repository target: - The intended repository is {{$var[expectedRepoUrl]s}}. - Before making changes, inspect the git remote URL and repository contents. If the checked-out project is clearly not this repository, stop and explain the mismatch without creating or modifying files. Documentation requirements: - Create or replace only the root-level file named exactly {{$var[documentationFile]s}}. - Analyze the repository structure and important files before writing. - Produce a broad repository guide, not just API documentation. - Cover, where supported by the repository contents: 1. Project overview and purpose 2. Repository structure 3. Prerequisites and setup 4. How to run, build, and test the project 5. Key application workflows or features 6. Architecture and important implementation details 7. Configuration, environment variables, or data/storage notes 8. Troubleshooting or maintenance notes - Use Markdown with clear headings and practical examples. - Do not make unrelated code or file changes. - After writing the file, verify that {{$var[documentationFile]s}} exists at the repository root and summarize what was added.


Bodhi: https://www.publicissapient.com/platforms/bodhi

Sustain Links: 
https://www.publicissapient.com/company/news/sapient-sustain-autonomous-it-operations
https://www.publicissapient.com/platforms/sustain
https://www.publicissapient.com/resources/demos?tab=sustain#content-card
https://www.publicissapient.com/resources/demos/pattern-iq
https://www.publicissapient.com/resources/demos/lead-failure


