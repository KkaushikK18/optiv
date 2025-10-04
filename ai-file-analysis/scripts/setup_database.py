#!/usr/bin/env python3
"""Database setup script for AI File Analysis System."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.database.connection import init_database, engine
from src.config.settings import settings


async def setup_database():
    """Set up the database with initial schema."""
    try:
        print("Setting up database...")
        print(f"Database URL: {settings.database.url}")
        
        # Initialize database tables
        await init_database()
        
        print("Database setup completed successfully!")
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        sys.exit(1)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(setup_database())