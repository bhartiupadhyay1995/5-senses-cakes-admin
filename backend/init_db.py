#!/usr/bin/env python
"""Database initialization script"""

import os
import sys

from app.config import get_settings
from app.database import init_db_manager
from app.models import Base


def init_database():
    """Initialize the database"""
    settings = get_settings()
    database_url = settings.get_database_url
    
    print(f"Initializing database at: {database_url}")
    
    try:
        # Initialize database manager
        db_manager = init_db_manager(database_url)
        
        # Create all tables
        print("Creating tables...")
        db_manager.create_tables()
        
        print("✓ Database initialized successfully!")
        db_manager.close()
        
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    init_database()
