"""Error handling middleware and utilities"""

import logging
from typing import Union

from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for handling exceptions and converting them to JSON responses"""

    async def dispatch(self, request: Request, call_next):
        """Handle requests and catch exceptions"""
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            return await self._handle_exception(exc, request)

    async def _handle_exception(self, exc: Exception, request: Request) -> JSONResponse:
        """Convert exceptions to JSON responses"""
        logger.error(f"Exception occurred: {type(exc).__name__}: {str(exc)}")

        if isinstance(exc, ValidationError):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "detail": "Validation error",
                    "errors": exc.errors(),
                },
            )

        elif isinstance(exc, IntegrityError):
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "detail": "Database integrity constraint violation",
                    "error": str(exc.orig),
                },
            )

        elif isinstance(exc, SQLAlchemyError):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Database error occurred",
                    "error": str(exc),
                },
            )

        elif isinstance(exc, ValueError):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "detail": str(exc),
                },
            )

        else:
            # Generic error response for unexpected exceptions
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal server error",
                    "error": str(exc),
                },
            )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests"""

    async def dispatch(self, request: Request, call_next):
        """Log request details"""
        logger.info(f"{request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
