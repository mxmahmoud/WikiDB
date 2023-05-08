from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from sqlalchemy import func, or_
from typing import List
import lxml.etree as ET

from app.models import Page
from app.schemas import PageSchema, SearchResult, SearchMask
from app.database_config import engine

# Function to ingest XML page data into the database
async def ingest_xml_page(db: Session, xml_string: str):
    try:
        # Parsing the plain text
        root = ET.fromstring(xml_string)

        # Defining the XML namespace
        key = "ns"
        ns = {key : root.nsmap[None]}

        # Extract page data from the XML and store it in a dictionary
        page = dict()
        page["title"] = root.find(f".//{key}:title", ns).text
        page["id"] = int(root.find(f".//{key}:id", ns).text)
        page["content"] = root.find(f".//{key}:text", ns).text

        # Ingest the page data into the database
        return await ingest_page(db, page)

    except Exception as exp:
        print(exp)

# Function to ingest a single page into the database
async def ingest_page(db: Session, page: PageSchema):
    _page = Page(id=page["id"], title=page["title"], content=page["content"])
    db.add(_page)
    db.commit()
    db.refresh(_page)
    return _page

# Function to search for content in the database using a search mask
async def search_content(db: Session, search_mask: SearchMask, limit: int = 20) -> List[SearchResult]:
    # Without indexing
    #results = db.query(Page).filter(or_(Page.title.ilike(f"%{search_mask.content}%"), 
    #                                    Page.content.ilike(f"%{search_mask.content}%"))).all()
    
    # Perform full-text search using a search query
    search_query = select([Page.id, Page.title]).where(
        func.to_tsvector('english', Page.title.op('||')(' ').op('||')(Page.content)).op('@@')(
            func.plainto_tsquery('english', search_mask.content)
        )
    )
    results = engine.execute(search_query).fetchmany(limit)

    return results

# Function to get a list of pages with pagination
async def get_pages(db: Session, skip: int = 0, limit: int = 100):
     # Query the database for pages with pagination (using offset and limit)
    pages = db.query(Page.id, Page.title).offset(skip).limit(limit).all()

    return pages