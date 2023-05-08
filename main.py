import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from app.database_config import SessionLocal
from app.services import ingest_xml_page, search_content
from app.database_api import get_pages


load_dotenv()

app = FastAPI()
LATEST_VERSION = "0.1"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")

@app.get("/")
async def root():
    return "Welcome to a really innovative wikki ingestion monster"

# As requested receives a plain text containing the full xml page, 
# instead of a dedicated json with sorted out values
@app.get(f"/api/v0.1/overview")
async def ingest():
    pages = dict()
    try:
        pages = await get_pages()
    finally:
        pass
    return pages

# As requested receives a plain text containing the full xml page, 
# instead of a dedicated json with sorted out values
@app.post(f"/api/v0.1/ingest")
async def ingest(request: Request):
    try:
        xml_string = await request.body()
        await ingest_xml_page(xml_string)
    finally:
        pass

    return  {"status": "success"}

@app.post(f"/api/v{LATEST_VERSION}/search")
async def search(search_mask: str):
    try:
        search_content(search_mask)
    finally:
        pass

    return  {"status": "success", "id":"id", "title":"title"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



    
