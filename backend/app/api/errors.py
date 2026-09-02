"""Error handling exceptions"""

from fastapi import HTTPException, status


class EntityNotFoundError(HTTPException):
    """Entity not found error"""
    def __init__(self, entity_type: str, entity_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_type} with id {entity_id} not found"
        )


class EntityAlreadyExistsError(HTTPException):
    """Entity already exists error"""
    def __init__(self, entity_type: str, field: str, value: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{entity_type} with {field} '{value}' already exists"
        )


class ValidationError(HTTPException):
    """Validation error"""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message
        )


class DatabaseError(HTTPException):
    """Database error"""
    def __init__(self, message: str = "Database error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )
