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

            # Table for background tasks (e.g. scraping)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    target TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    payload TEXT,
                    result TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_task_status ON tasks(status)")
            conn.commit()

    def create_task(self, type: str, target: str, payload: Optional[Dict[str, Any]] = None) -> int:
        """Creates a new background task and returns its ID."""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO tasks (type, target, status, payload)
                VALUES (?, ?, 'pending', ?)
            """, (type, target, json.dumps(payload) if payload else None))
            conn.commit()
            return cursor.lastrowid

    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a task by its ID."""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, type, target, status, payload, result, created_at, updated_at
                FROM tasks WHERE id = ?
            """, (task_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "type": row[1],
                    "target": row[2],
                    "status": row[3],
                    "payload": json.loads(row[4]) if row[4] else None,
                    "result": json.loads(row[5]) if row[5] else None,
                    "created_at": row[6],
                    "updated_at": row[7]
                }
        return None

    def update_task_status(self, task_id: int, status: str, result: Optional[Dict[str, Any]] = None):
        """Updates the status and optionally the result of a task."""
        with self._get_connection() as conn:
            conn.execute("""
                UPDATE tasks 
                SET status = ?, result = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (status, json.dumps(result) if result else None, task_id))
            conn.commit()

    def get_tasks(self, status: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieves a list of tasks, optionally filtered by status."""
        query = "SELECT id, type, target, status, payload, result, created_at, updated_at FROM tasks"
        params = []
        if status:
            query += " WHERE status = ?"
            params.append(status)
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        with self._get_connection() as conn:
            cursor = conn.execute(query, params)
            tasks = []
            for row in cursor:
                tasks.append({
                    "id": row[0],
                    "type": row[1],
                    "target": row[2],
                    "status": row[3],
                    "payload": json.loads(row[4]) if row[4] else None,
                    "result": json.loads(row[5]) if row[5] else None,
                    "created_at": row[6],
                    "updated_at": row[7]
                })
            return tasks

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
