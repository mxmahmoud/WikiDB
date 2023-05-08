from fastapi import APIRouter, Request, Request, Depends, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from sqlalchemy.orm import Session
from urllib.parse import parse_qs

from app.database_config import SessionLocal
from app.database_api import ingest_xml_page, search_content, get_pages
from app.schemas import SearchMask

# Create a FastAPI router
router = APIRouter()
LATEST_API_VERSION = "0.1"

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to serve favicon
@router.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse((Path(__file__).parent.parent / "data" / "favicon.ico"))

@router.get("/")
async def root():
    return "Welcome to a really innovative wikki ingestion monster"

# Route to get a summary of the stored pages
@router.get(f"/api/v{LATEST_API_VERSION}/overview")
async def ingest(db: Session = Depends(get_db)):
    pages = dict()
    try:
        pages = await get_pages(db=db)
    finally:
        pass
    return pages

# As requested receives a plain text containing the full xml page, 
# instead of a dedicated json with sorted out values
# Route to ingest a new page using plain text XML content
@router.post(f"/api/v{LATEST_API_VERSION}/ingest")
async def ingest(request: Request, db: Session = Depends(get_db)):
    try:
        xml_string = await request.body()
        await ingest_xml_page(db, xml_string)
    finally:
        pass

    return  {"status": "success"}

# Route to search for pages using POST request
@router.post(f"/api/v{LATEST_API_VERSION}/search")
async def search(search_mask: Request, db: Session = Depends(get_db)):
    # Get the content type from the request headers
    content_type = search_mask.headers.get("Content-Type")

    # Check if the content type is JSON, and parse the JSON payload
    if content_type == "application/json":
        pay_load = await search_mask.json()
        
    # Check if there are any query parameters in the URL and parse them
    elif len(search_mask.url.query) > 0:
        pay_load = parse_qs(search_mask.url.query)
        # Check if the "content" parameter is present in the parsed query parameters
        if "content" not in pay_load:
            # If the "content" parameter is missing, raise an HTTPException with a 400 status code
            raise HTTPException(status_code=400, detail="Unsupported Content-Type")
        else:
            # Extract the "content" value from the parsed query parameters
            pay_load["content"] = pay_load["content"][0]


    pages = dict()
    try:
        pages = await search_content(db, SearchMask(content=pay_load["content"]))
    finally:
        pass
    
    return pages


# Route to search for pages using GET request
@router.get(f"/api/v{LATEST_API_VERSION}/search")
async def search(content: str, db: Session = Depends(get_db)):
    pages = dict()
    try:
        pages = await search_content(db, SearchMask(content=content))
    finally:
        pass
    return pages