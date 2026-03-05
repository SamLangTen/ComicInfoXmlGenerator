from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from dataclasses import asdict
import json
import asyncio
import os
from src.config_manager import config_manager
from src.scanner import scan_archives
from src.comic_info import ComicInfo
from src.scraper import LocalFilenameScraper, LlmFilenameScraper
from src.archive import inject_comic_info_xml

app = FastAPI(title="ComicInfoXmlGenerator API")

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
        session_cache[path] = ComicInfo(path=path)
    return asdict(session_cache[path])

@app.post("/api/metadata")
async def update_metadata(data: Dict[str, Any]):
    path = data.get("path")
    if not path:
        return {"status": "error", "message": "Path is required"}
    
    if path not in session_cache:
        session_cache[path] = ComicInfo(path=path)
    
    comic = session_cache[path]
    for key, value in data.items():
        if hasattr(comic, key) and key != "path":
            setattr(comic, key, value)
            
    return {"status": "success"}

class ScrapeRequest(BaseModel):
    paths: List[str]
    strategy: str # local, llm, regex

@app.post("/api/scrape")
async def scrape(request: ScrapeRequest):
    # Log callback for the scraper
    def api_log_callback(msg: str):
        asyncio.create_task(manager.broadcast(msg))

    if request.strategy.lower() == "llm":
        scraper = LlmFilenameScraper(
            api_key=config_manager.get("llm_api_key"),
            base_url=config_manager.get("llm_base_url"),
            model=config_manager.get("llm_model")
        )
    else:
        scraper = LocalFilenameScraper()
    
    # Get comics from cache
    comics_to_scrape = []
    for p in request.paths:
        if p not in session_cache:
            session_cache[p] = ComicInfo(path=p)
        comics_to_scrape.append(session_cache[p])
    
    # Perform batch search
    scraper.search_batch(comics_to_scrape, log_callback=api_log_callback)
    
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
