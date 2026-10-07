"""FastAPI application entry point.

Bootstraps the FastAPI application with all routers, middleware, and exception handlers.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.settings import settings
from app.database.session import Base, engine
from app.exceptions.exception_handlers import register_exception_handlers
from app.routers import book_router

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan manager.
    
    Handles startup and shutdown events for the FastAPI application.
    Creates database tables on startup.
    
    Args:
        app: FastAPI application instance
        
    Yields:
        Control to the application
    """
    # Startup: Create database tables
    logger.info("Starting up application...")
    logger.info("Creating database tables...")
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise
    
    logger.info(f"Application started successfully in {settings.ENVIRONMENT} mode")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan,
    debug=settings.DEBUG,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("CORS middleware configured")

# Register exception handlers
register_exception_handlers(app)

# Register routers
app.include_router(book_router.router)
logger.info("API routers registered")


# Health check endpoint
@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    description="Returns the health status of the application",
    status_code=status.HTTP_200_OK,
    response_description="Application is healthy"
)
async def health_check() -> JSONResponse:
    """Health check endpoint.
    
    Returns the current health status of the application.
    Useful for monitoring, load balancers, and container orchestration.
    
    Returns:
        JSONResponse: Health status with application metadata
        
    Example:
        >>> GET /health
        {
            "status": "healthy",
            "version": "1.0.0",
            "environment": "development"
        }
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "service": settings.PROJECT_NAME
        }
    )


# Root endpoint
@app.get(
    "/",
    tags=["root"],
    summary="Root endpoint",
    description="Returns API information and available endpoints",
    status_code=status.HTTP_200_OK
)
async def root() -> JSONResponse:
    """Root endpoint with API information.
    
    Returns:
        JSONResponse: API metadata and documentation links
    """
    return JSONResponse(
        content={
            "message": f"Welcome to {settings.PROJECT_NAME}",
            "version": settings.VERSION,
            "documentation": "/docs",
            "redoc": "/redoc",
            "health": "/health"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting FastAPI application with Uvicorn...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info"
    )
