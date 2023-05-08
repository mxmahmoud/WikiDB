from fastapi import APIRouter, Request, Request
from fastapi.responses import FileResponse
from pathlib import Path
from app.database_config import SessionLocal
from app.database_api import ingest_xml_page, search_content, get_pages


LATEST_VERSION = "0.1"

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse((Path(__file__).parent / "data" / "favicon.ico"))

@router.get("/")
async def root():
    return "Welcome to a really innovative wikki ingestion monster"


@router.get(f"/api/v0.1/overview")
async def ingest():
    pages = dict()
    try:
        pages = await get_pages()
    finally:
        pass
    return pages

# As requested receives a plain text containing the full xml page, 
# instead of a dedicated json with sorted out values
@router.post(f"/api/v0.1/ingest")
async def ingest(request: Request):
    try:
        xml_string = await request.body()
        await ingest_xml_page(xml_string)
    finally:
        pass

    return  {"status": "success"}

@router.post(f"/api/v{LATEST_VERSION}/search")
async def search(search_mask: str):
    try:
        search_content(search_mask)
    finally:
        pass

    return  {"status": "success", "id":"id", "title":"title"}
