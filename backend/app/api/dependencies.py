"""Dependency injection utilities"""

from sqlalchemy.orm import Session

from app.database import get_db_manager
from app.repositories import RepositoryFactory


def get_db_session() -> Session:
    """Get database session for dependency injection"""
    db_manager = get_db_manager()
    session = db_manager.get_session()
    try:
        yield session
    finally:
        session.close()


def get_repositories(session: Session = None) -> RepositoryFactory:
    """Get repositories factory for dependency injection"""
    if session is None:
        db_manager = get_db_manager()
        session = db_manager.get_session()
    return RepositoryFactory(session)
