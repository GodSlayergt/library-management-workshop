"""Application settings and configuration.

Uses Pydantic Settings for environment-based configuration management.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.
    
    Attributes:
        PROJECT_NAME: Name of the API project
        VERSION: API version
        API_V1_PREFIX: URL prefix for API v1 endpoints
        DATABASE_URL: SQLAlchemy database connection string
        DEBUG: Enable debug mode (verbose logging, SQL echo)
        ENVIRONMENT: Deployment environment (dev, staging, prod)
    """
    
    # API Configuration
    PROJECT_NAME: str = "Library Management System - Book API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    DESCRIPTION: str = "REST API for managing books in the library system"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./library.db"
    
    # Application Settings
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # CORS Configuration (for frontend integration)
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore extra fields in .env
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.
    
    Uses LRU cache to ensure singleton pattern - settings are loaded once.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()


# Global settings instance
settings = get_settings()
