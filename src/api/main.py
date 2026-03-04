from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from dataclasses import asdict
from src.config_manager import config_manager
from src.scanner import scan_archives
from src.comic_info import ComicInfo

app = FastAPI(title="ComicInfoXmlGenerator API")

# In-memory session cache: path -> ComicInfo
session_cache: Dict[str, ComicInfo] = {}

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
