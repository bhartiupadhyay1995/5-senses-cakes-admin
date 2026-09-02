"""Main FastAPI application"""

import logging

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import api_router
from app.config import get_settings
from app.database import init_db_manager
from app.middleware.error_handling import ErrorHandlingMiddleware, RequestLoggingMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="5 Senses Cakes API",
        description="API for personalized cake business management",
        version="0.1.0",
    )
    
    # Initialize database
    database_url = settings.get_database_url
    init_db_manager(database_url)
    
    # Add middleware (order matters - added in reverse order)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Configure based on environment
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check endpoint
    @app.get("/health")
    def health_check():
        """Health check endpoint"""
        return {"status": "ok", "service": "5-senses-cakes-api"}
    
    # Include API routes
    app.include_router(api_router)
    
    # Root endpoint with API documentation
    @app.get("/")
    def root():
        """Root endpoint"""
        return {
            "service": "5 Senses Cakes API",
            "version": "0.1.0",
            "docs": "/docs",
            "redoc": "/redoc",
        }
    
    @app.on_event("startup")
    async def startup():
        """Startup event"""
        logger.info("5 Senses Cakes API starting...")
        logger.info(f"Environment: {settings.environment}")
        logger.info(f"Database: {settings.postgres_db}")
    
    @app.on_event("shutdown")
    async def shutdown():
        """Shutdown event"""
        from app.database import get_db_manager
        try:
            db_manager = get_db_manager()
            db_manager.close()
        except RuntimeError:
            pass  # Database not initialized
        logger.info("5 Senses Cakes API stopped")
    
    return app


app = create_app()
