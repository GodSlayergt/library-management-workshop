"""Global exception handlers for FastAPI application.

Centralized error handling to ensure consistent API error responses.
"""

import logging
from typing import Union

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions.duplicate_resource_exception import DuplicateResourceException

# Configure logger
logger = logging.getLogger(__name__)


async def duplicate_resource_exception_handler(
    request: Request, 
    exc: DuplicateResourceException
) -> JSONResponse:
    """Handle DuplicateResourceException (409 Conflict).
    
    Returns a 409 Conflict response when attempting to create a resource
    that already exists (e.g., duplicate ISBN).
    
    Args:
        request: FastAPI request object
        exc: DuplicateResourceException instance
        
    Returns:
        JSONResponse with 409 status code and error details
    """
    logger.warning(
        f"Duplicate resource conflict: {exc.resource_type} with "
        f"identifier '{exc.identifier}' already exists"
    )
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Duplicate Resource",
            "message": exc.message,
            "details": {
                "resource_type": exc.resource_type,
                "identifier": exc.identifier
            }
        }
    )


async def validation_exception_handler(
    request: Request, 
    exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    """Handle Pydantic validation errors (400 Bad Request).
    
    Returns a 400 Bad Request response when request data fails validation.
    
    Args:
        request: FastAPI request object
        exc: RequestValidationError or ValidationError instance
        
    Returns:
        JSONResponse with 400 status code and validation error details
    """
    logger.warning(f"Request validation failed: {exc.errors()}")
    
    # Format validation errors for user-friendly response
    details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        details.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Validation Error",
            "message": "Request validation failed",
            "details": details
        }
    )


async def sqlalchemy_exception_handler(
    request: Request, 
    exc: SQLAlchemyError
) -> JSONResponse:
    """Handle SQLAlchemy database errors (500 Internal Server Error).
    
    Returns a 500 Internal Server Error response for database failures.
    Logs the actual error but returns a generic message to avoid exposing internals.
    
    Args:
        request: FastAPI request object
        exc: SQLAlchemyError instance
        
    Returns:
        JSONResponse with 500 status code and generic error message
    """
    logger.error(f"Database error occurred: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "A database error occurred while processing your request. Please try again later."
        }
    )


async def generic_exception_handler(
    request: Request, 
    exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions (500 Internal Server Error).
    
    Catch-all handler for any unhandled exceptions.
    Logs the full error but returns a generic message for security.
    
    Args:
        request: FastAPI request object
        exc: Exception instance
        
    Returns:
        JSONResponse with 500 status code and generic error message
    """
    logger.error(
        f"Unexpected error occurred: {type(exc).__name__} - {str(exc)}",
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred while processing your request. Please try again later."
        }
    )


def register_exception_handlers(app) -> None:
    """Register all exception handlers with the FastAPI application.
    
    Args:
        app: FastAPI application instance
        
    Example:
        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> register_exception_handlers(app)
    """
    app.add_exception_handler(DuplicateResourceException, duplicate_resource_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    
    logger.info("Exception handlers registered successfully")
