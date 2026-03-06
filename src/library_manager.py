import os
import json
import asyncio
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import asdict
from difflib import SequenceMatcher
from src.config_manager import config_manager
from src.scanner import scan_archives
from src.comic_info import ComicInfo
from src.archive import read_comic_info_xml
from src.database import db_manager

class LibraryManager:
    def __init__(self):
        self.manga_root = config_manager.get("manga_root_directory")
        self.is_scanning = False
        self.auto_scan_task = None

    def start_auto_scan(self):
        if self.auto_scan_task:
            self.auto_scan_task.cancel()
        self.auto_scan_task = asyncio.create_task(self._auto_scan_loop())

    async def _auto_scan_loop(self):
        while True:
            enabled = config_manager.get("auto_scan_enabled")
            interval = config_manager.get("auto_scan_interval_minutes") or 30
            
            if enabled:
                await self.scan()
            
            await asyncio.sleep(max(60, interval * 60))

    def _extract_series_from_filename(self, filename: str) -> str:
        name = re.sub(r'\[.*?\]', '', filename)
        name = Path(name).stem
        name = re.sub(r'(?i)(vol\.|v|#)?\s?\d+.*$', '', name)
        name = re.sub(r'[\-_]', ' ', name)
        return name.strip()

    def _find_best_series_match(self, series_name: str, existing_series: List[str], threshold=0.85) -> Optional[str]:
        if not series_name: return None
        best_match = None
        highest_ratio = 0
        
        for existing in existing_series:
            ratio = SequenceMatcher(None, series_name.lower(), existing.lower()).ratio()
            if ratio > highest_ratio and ratio >= threshold:
                highest_ratio = ratio
                best_match = existing
        
        return best_match

    async def scan(self, log_callback=None):
        if self.is_scanning:
            return
        
        self.manga_root = config_manager.get("manga_root_directory")
        if not self.manga_root or not os.path.exists(self.manga_root):
            if log_callback:
                msg = "Manga root directory not set or invalid."
                if asyncio.iscoroutinefunction(log_callback): await log_callback(msg)
                else: await asyncio.to_thread(log_callback, msg)
            return

        self.is_scanning = True
        if log_callback:
            msg = f"Starting library scan: {self.manga_root}"
            if asyncio.iscoroutinefunction(log_callback): await log_callback(msg)
            else: await asyncio.to_thread(log_callback, msg)

        try:
            files = scan_archives(self.manga_root)
            processed_count = 0
            
            # Temporary cache of series names found in THIS scan or in DB to help grouping
            scan_series_names = set()

            for file_path in files:
                current_mtime = os.path.getmtime(file_path)
                cached = db_manager.get_archive(file_path)
                
                # Incremental Logic: Only process if not in DB or mtime changed
                if cached and cached["mtime"] == current_mtime:
                    scan_series_names.add(cached["series_name"])
                    continue
                
                processed_count += 1
                
                # 1. Load/Read Metadata
                comic = read_comic_info_xml(file_path)
                if not comic:
                    comic = ComicInfo(path=file_path)
                
                metadata = asdict(comic)
                
                # 2. Grouping Logic
                series = metadata.get("Series")
                if not series:
                    series = self._extract_series_from_filename(Path(file_path).name)
                if not series or len(series) < 2:
                    series = Path(file_path).parent.name
                if not series:
                    series = "Unknown"

                # 3. Similarity Matching
                best_match = self._find_best_series_match(series, list(scan_series_names))
                if best_match:
                    series = best_match

                # 4. Save to DB
                db_manager.update_archive(file_path, current_mtime, series, metadata)
                scan_series_names.add(series)

            # Cleanup deleted files from DB
            if files:
                db_manager.clear_missing_archives(files)
            
            if log_callback:
                msg = f"Scan complete. Found {len(files)} archives. (Processed {processed_count} new/changed)"
                if asyncio.iscoroutinefunction(log_callback): await log_callback(msg)
                else: await asyncio.to_thread(log_callback, msg)

        finally:
            self.is_scanning = False

    def get_series_list(self) -> List[Dict[str, Any]]:
        return db_manager.get_all_series()

# Global singleton
library_manager = LibraryManager()
