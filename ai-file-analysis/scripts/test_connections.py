#!/usr/bin/env python3
"""Test database and Redis connections."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.database.connection import engine
from src.database.cache import cache_manager
from src.config.settings import settings


async def test_database_connection():
    """Test database connection."""
    try:
        async with engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            assert result.scalar() == 1
        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


async def test_redis_connection():
    """Test Redis connection."""
    try:
        await cache_manager.connect()
        await cache_manager.set("test_key", "test_value", expire=10)
        value = await cache_manager.get("test_key")
        assert value == "test_value"
        await cache_manager.delete("test_key")
        print("✓ Redis connection successful")
        return True
    except Exception as e:
        print(f"✗ Redis connection failed: {e}")
        return False


async def main():
    """Test all connections."""
    print("Testing connections...")
    print(f"Database URL: {settings.database.url}")
    print(f"Redis URL: {settings.redis.url}")
    print()
    
    db_ok = await test_database_connection()
    redis_ok = await test_redis_connection()
    
    if db_ok and redis_ok:
        print("\n✓ All connections successful!")
        sys.exit(0)
    else:
        print("\n✗ Some connections failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())