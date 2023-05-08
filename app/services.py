from app.schemas import PageSchema, SearchResult
import lxml.etree as ET

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