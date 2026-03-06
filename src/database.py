import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.config_manager import config_manager

class DatabaseManager:
    def __init__(self):
        self.db_path = config_manager.get_data_path("library.db")
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            # Table for comic archives and their metadata
            conn.execute("""
                CREATE TABLE IF NOT EXISTS archives (
                    path TEXT PRIMARY KEY,
                    mtime REAL,
                    series_name TEXT,
                    metadata_json TEXT
                )
            """)
            # Index for fast series lookup
            conn.execute("CREATE INDEX IF NOT EXISTS idx_series ON archives(series_name)")
            conn.commit()

    def update_archive(self, path: str, mtime: float, series_name: str, metadata: Dict[str, Any]):
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO archives (path, mtime, series_name, metadata_json)
                VALUES (?, ?, ?, ?)
            """, (path, mtime, series_name, json.dumps(metadata, ensure_ascii=False)))
            conn.commit()

    def get_archive(self, path: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT mtime, series_name, metadata_json FROM archives WHERE path = ?", (path,))
            row = cursor.fetchone()
            if row:
                return {
                    "mtime": row[0],
                    "series_name": row[1],
                    "metadata": json.loads(row[2])
                }
        return None

    def get_all_series(self) -> List[Dict[str, Any]]:
        """Returns all series and their comic paths."""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT series_name, path FROM archives ORDER BY series_name ASC, path ASC")
            groups = {}
            for row in cursor:
                series_name, path = row
                if series_name not in groups:
                    groups[series_name] = []
                groups[series_name].append(path)
            
            result = []
            for name, paths in groups.items():
                result.append({
                    "name": name,
                    "count": len(paths),
                    "paths": paths,
                    "cover_path": paths[0] if paths else None
                })
            return result

    def clear_missing_archives(self, existing_paths: List[str]):
        """Remove archives that no longer exist on disk."""
        with self._get_connection() as conn:
            # This is a simple implementation, for large libraries we might want a more efficient approach
            placeholders = ','.join(['?'] * len(existing_paths))
            conn.execute(f"DELETE FROM archives WHERE path NOT IN ({placeholders})", existing_paths)
            conn.commit()

    def get_library_stats(self) -> Dict[str, int]:
        """Returns counts for series and archives."""
        with self._get_connection() as conn:
            archive_count = conn.execute("SELECT COUNT(*) FROM archives").fetchone()[0]
            series_count = conn.execute("SELECT COUNT(DISTINCT series_name) FROM archives").fetchone()[0]
            return {
                "archive_count": archive_count,
                "series_count": series_count
            }

# Global singleton
db_manager = DatabaseManager()
