"""
SQLite cache manager for API responses.
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os


class CacheManager:
    """Manages SQLite cache for API responses."""
    
    def __init__(self, db_path: str = "data/cache/api_cache.db"):
        """Initialize cache manager."""
        self.db_path = db_path
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._init_db()
    
    def _init_db(self):
        """Create cache table if not exists."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cached_api_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                query_key TEXT NOT NULL,
                response_data TEXT,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ttl_days INTEGER DEFAULT 30,
                UNIQUE(source, query_key)
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cache_lookup 
            ON cached_api_responses(source, query_key)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cache_expiry 
            ON cached_api_responses(fetched_at, ttl_days)
        """)
        
        conn.commit()
        conn.close()
    
    def get(self, source: str, query_key: str, ttl_days: int = 30) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached data if not expired.
        
        Args:
            source: Data source name (e.g., "land_registry", "companies_house")
            query_key: Unique query identifier
            ttl_days: Time-to-live in days
            
        Returns:
            Cached data dict or None if not found/expired
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT response_data, fetched_at 
            FROM cached_api_responses 
            WHERE source = ? AND query_key = ?
        """, (source, query_key))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return None
        
        response_data, fetched_at = result
        
        # Check if expired
        fetched_datetime = datetime.fromisoformat(fetched_at)
        age_days = (datetime.now() - fetched_datetime).days
        
        if age_days >= ttl_days:
            return None
        
        return json.loads(response_data)
    
    def set(self, source: str, query_key: str, data: Dict[str, Any], ttl_days: int = 30):
        """
        Store data in cache.
        
        Args:
            source: Data source name
            query_key: Unique query identifier
            data: Data to cache
            ttl_days: Time-to-live in days
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO cached_api_responses 
            (source, query_key, response_data, fetched_at, ttl_days)
            VALUES (?, ?, ?, ?, ?)
        """, (
            source,
            query_key,
            json.dumps(data),
            datetime.now().isoformat(),
            ttl_days
        ))
        
        conn.commit()
        conn.close()
    
    def clear_expired(self):
        """Remove all expired cache entries."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM cached_api_responses 
            WHERE julianday('now') - julianday(fetched_at) > ttl_days
        """)
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def clear_all(self):
        """Clear entire cache."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM cached_api_responses")
        
        conn.commit()
        conn.close()
