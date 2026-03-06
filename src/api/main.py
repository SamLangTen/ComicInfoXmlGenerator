from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from dataclasses import asdict
import json
import asyncio
import os
import hashlib
from src.config_manager import config_manager
from src.scanner import scan_archives
from src.comic_info import ComicInfo
from src.scraper import LocalFilenameScraper, LlmFilenameScraper, BooksScraper
from src.archive import inject_comic_info_xml, extract_cover_image
from src.library_manager import library_manager
from src.database import db_manager

app = FastAPI(title="ComicInfoXmlGenerator API")

@app.on_event("startup")
async def startup_event():
    # Initial library scan in background
    asyncio.create_task(library_manager.scan())
    # Start the auto-scan loop
    library_manager.start_auto_scan()

@app.get("/api/library/series")
async def get_series():
    return library_manager.get_series_list()

@app.get("/api/cover")
async def get_cover(path: str):
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Archive not found")
    
    # 1. Check Disk Cache
    # Create a hash based on path and mtime to handle file updates
    mtime = os.path.getmtime(path)
    cache_key = hashlib.md5(f"{path}_{mtime}".encode()).hexdigest()
    cache_path = config_manager.get_data_path(f"cache/covers/{cache_key}.jpg")
    
    if cache_path.exists():
        return FileResponse(cache_path, media_type="image/jpeg")
    
    # 2. Extract and Cache
    # Run extraction in a separate thread since it's blocking I/O
    image_bytes = await asyncio.to_thread(extract_cover_image, path)
    if not image_bytes:
        raise HTTPException(status_code=404, detail="No cover found in archive")
    
    # Save to cache
    try:
        with open(cache_path, "wb") as f:
            f.write(image_bytes)
    except Exception as e:
        print(f"Error saving cache: {e}")
        
    return Response(content=image_bytes, media_type="image/jpeg")

@app.post("/api/library/scan")
async def trigger_library_scan():
    asyncio.create_task(library_manager.scan(
        log_callback=lambda msg: manager.broadcast(msg)
    ))
    return {"status": "scanning"}

@app.get("/api/library/status")
async def get_library_status():
    stats = db_manager.get_library_stats()
    return {
        "is_scanning": library_manager.is_scanning,
        "manga_root": library_manager.manga_root,
        "series_count": stats["series_count"],
        "file_count": stats["archive_count"]
    }

# Serve Frontend Static Assets
web_dist_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "web/dist")

# ... existing cache and manager ...

# In-memory session cache: path -> ComicInfo
session_cache: Dict[str, ComicInfo] = {}

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

@app.websocket("/api/logs")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

class ConfigUpdate(BaseModel):
    llm_base_url: str = None
    llm_api_key: str = None
    llm_model: str = None
    appearance_mode: str = None
    default_scraper: str = None
    manga_root_directory: str = None
    auto_scan_enabled: bool = None
    auto_scan_interval_minutes: int = None

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.get("/api/config")
async def get_config():
    return config_manager.config

@app.post("/api/config")
async def update_config(update: ConfigUpdate):
    data = update.model_dump(exclude_unset=True)
    for key, value in data.items():
        config_manager.set(key, value)
    return {"status": "success"}

class ScanRequest(BaseModel):
    directory: str

@app.post("/api/scan")
async def scan(request: ScanRequest):
    files = scan_archives(request.directory)
    return {"files": files}

@app.get("/api/metadata")
async def get_metadata(path: str):
    if path not in session_cache:
        # Try to load from DB first
        cached = db_manager.get_archive(path)
        if cached:
            session_cache[path] = ComicInfo.from_dict(cached["metadata"])
        else:
            session_cache[path] = ComicInfo(path=path)
    return asdict(session_cache[path])

@app.post("/api/metadata")
async def update_metadata(data: Dict[str, Any]):
    path = data.get("path")
    if not path:
        return {"status": "error", "message": "Path is required"}
    
    if path not in session_cache:
        cached = db_manager.get_archive(path)
        if cached:
            session_cache[path] = ComicInfo.from_dict(cached["metadata"])
        else:
            session_cache[path] = ComicInfo(path=path)
    
    comic = session_cache[path]
    for key, value in data.items():
        if hasattr(comic, key) and key != "path":
            setattr(comic, key, value)
            
    return {"status": "success"}

class ScrapeRequest(BaseModel):
    paths: List[str]
    strategy: str # local, llm, regex, books

@app.post("/api/scrape")
async def scrape(request: ScrapeRequest):
    print(f"DEBUG: Scrape endpoint reached. Strategy: {request.strategy}, Paths: {len(request.paths)}")
    
    # Capture the current event loop to use in the thread-safe callback
    loop = asyncio.get_running_loop()

    # Log callback for the scraper (will be called from a worker thread)
    def api_log_callback(msg: str):
        print(f"SCRAPER LOG: {msg}")
        # Safely schedule the broadcast on the main event loop
        asyncio.run_coroutine_threadsafe(manager.broadcast(msg), loop)

    await manager.broadcast(f"Starting scrape with strategy: {request.strategy}")

    if request.strategy.lower() == "llm":
        scraper = LlmFilenameScraper(
            api_key=config_manager.get("llm_api_key"),
            base_url=config_manager.get("llm_base_url"),
            model=config_manager.get("llm_model")
        )
    elif request.strategy.lower() == "books":
        scraper = BooksScraper()
    else:
        scraper = LocalFilenameScraper()
    
    # Get comics from cache/DB
    comics_to_scrape = []
    for p in request.paths:
        if p not in session_cache:
            cached = db_manager.get_archive(p)
            if cached:
                session_cache[p] = ComicInfo.from_dict(cached["metadata"])
            else:
                session_cache[p] = ComicInfo(path=p)
        comics_to_scrape.append(session_cache[p])
    
    print(f"DEBUG: Starting search_batch for {len(comics_to_scrape)} items")
    # Perform batch search (This is sync, consider running in thread if blocking is an issue)
    await asyncio.to_thread(scraper.search_batch, comics_to_scrape, api_log_callback)
    
    print(f"DEBUG: search_batch completed")
    # Update DB after scraping to persist results
    for comic in comics_to_scrape:
        if comic.path:
            mtime = os.path.getmtime(comic.path)
            db_manager.update_archive(comic.path, mtime, comic.Series, asdict(comic))
    
    await manager.broadcast("Scrape process completed successfully.")
    return {"status": "success"}

class InjectRequest(BaseModel):
    paths: List[str]

@app.post("/api/inject")
async def inject(request: InjectRequest):
    results = {}
    for p in request.paths:
        if p not in session_cache:
            results[p] = "error: not in cache"
            continue
        
        try:
            inject_comic_info_xml(p, session_cache[p])
            results[p] = "success"
        except Exception as e:
            results[p] = f"error: {str(e)}"
            
    return {"status": "success", "results": results}

# Serve static files and index.html for unknown routes
if os.path.exists(web_dist_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(web_dist_path, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # If the path starts with api, it should have been caught by the other routes
        if full_path.startswith("api"):
            return {"error": "Not Found"}
        return FileResponse(os.path.join(web_dist_path, "index.html"))
else:
    print(f"Warning: web/dist not found at {web_dist_path}. UI will not be served.")
