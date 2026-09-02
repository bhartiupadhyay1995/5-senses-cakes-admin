from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.models.base import Base


class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self._engine = None
        self._session_factory = None

    def init_db(self):
        """Initialize database connection"""
        self._engine = create_engine(
            self.database_url,
            poolclass=NullPool,
            echo=False,
        )
        self._session_factory = sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

    def get_session(self):
        """Get a new database session"""
        if self._session_factory is None:
            raise RuntimeError("Database not initialized. Call init_db() first.")
        return self._session_factory()

    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(self._engine)

    def close(self):
        """Close database connection"""
        if self._engine:
            self._engine.dispose()


# Global database manager instance
db_manager = None


def get_db_manager():
    """Get the global database manager"""
    global db_manager
    if db_manager is None:
        raise RuntimeError("Database manager not initialized")
    return db_manager


def init_db_manager(database_url: str):
    """Initialize the global database manager"""
    global db_manager
    db_manager = DatabaseManager(database_url)
    db_manager.init_db()
    return db_manager
