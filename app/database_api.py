from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from sqlalchemy import func, or_
from typing import List
import lxml.etree as ET

from app.models import Page
from app.schemas import PageSchema, SearchResult, SearchMask
from app.database_config import engine

async def ingest_xml_page(db: Session, xml_string: str):
    try:
        root = ET.fromstring(xml_string)
        # defining xml namespace
        key = "ns"
        ns = {key : root.nsmap[None]}

        page = dict()
        page["title"] = root.find(f".//{key}:title", ns).text
        page["id"] = int(root.find(f".//{key}:id", ns).text)
        page["content"] = root.find(f".//{key}:text", ns).text
        return await ingest_page(db, page)

    except Exception as exp:
        print(exp)

async def ingest_page(db: Session, page: PageSchema):
    _page = Page(id=page["id"], title=page["title"], content=page["content"])
    db.add(_page)
    db.commit()
    db.refresh(_page)
    return _page

async def search_content(db: Session, search_mask: SearchMask) -> List[SearchResult]:
    # Without indexing
    #results = db.query(Page).filter(or_(Page.title.ilike(f"%{search_mask.content}%"), 
    #                                    Page.content.ilike(f"%{search_mask.content}%"))).all()
    search_query = select([Page]).where(
        func.to_tsvector('english', Page.title.op('||')(' ').op('||')(Page.content)).op('@@')(
            func.plainto_tsquery('english', search_mask.content)
        )
    )
    results = engine.execute(search_query).fetchall()
    return [SearchResult(title=result.title, id=result.id) for result in results]

async def get_pages(db: Session, skip: int = 0, limit: int = 100):
    pages = db.query(Page.id, Page.title).offset(skip).limit(limit).all()
    return [{"title": page[1], "id": page[0]} for page in pages]