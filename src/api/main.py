from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from dataclasses import asdict
from src.config_manager import config_manager
from src.scanner import scan_archives
from src.comic_info import ComicInfo
from src.scraper import LocalFilenameScraper, LlmFilenameScraper

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

class ScrapeRequest(BaseModel):
    paths: List[str]
    strategy: str # local, llm, regex

@app.post("/api/scrape")
async def scrape(request: ScrapeRequest):
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
    scraper.search_batch(comics_to_scrape)
    
    return {"status": "success"}
