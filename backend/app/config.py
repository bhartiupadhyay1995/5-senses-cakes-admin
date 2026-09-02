import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    postgres_user: str = os.getenv("POSTGRES_USER", "cakes_user")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "cakes_password_dev")
    postgres_db: str = os.getenv("POSTGRES_DB", "5_senses_cakes")
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    database_url: Optional[str] = os.getenv("DATABASE_URL")
    
    # Backend
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def get_database_url(self) -> str:
        """Get database URL"""
        if self.database_url:
            return self.database_url
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment == "development"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
