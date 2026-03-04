from fastapi import FastAPI

app = FastAPI(title="ComicInfoXmlGenerator API")

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
