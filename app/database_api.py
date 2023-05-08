from sqlalchemy.orm import Session, load_only
import lxml.etree as ET

from app.models import Page
from app.schemas import PageSchema
from app.schemas import PageSchema, SearchResult


async def ingest_xml_page(xml_string: str):
    try:
        root = ET.fromstring(xml_string)
        key = "ns"
        ns = {key : root.nsmap[None]}
        #title = root.xpath('*[local-name() = "title"]')[0].text
        #id = root.xpath('*[local-name() = "id"]')[0].text
        #text = root.xpath('*[local-name() = "text"]')[0].text
        
        page = dict()
        page["title"] = root.find(f".//{key}:title", ns).text
        page["id"] = int(root.find(f".//{key}:id", ns).text)
        page["text"] = root.find(f".//{key}:text", ns).text
        return await ingest_page(page)

    except Exception as exp:
        print(exp)

async def ingest_page(page: PageSchema):
    pass

async def search_content(search_mask: str) -> SearchResult:
    pass

def create_page(db: Session, page: PageSchema):
    _page = Page(id=page.id, title=page.title, content=page.content)
    db.add(_page)
    db.commit()
    db.refresh(_page)
    return _page

def get_pages(db: Session, skip: int = 0, limit: int = 100):
    pages = db.query(Page.id, Page.title).options(load_only("id", "title")).offset(skip).limit(limit).all()
    return [{"id": page[0], "title": page[1]} for page in pages]