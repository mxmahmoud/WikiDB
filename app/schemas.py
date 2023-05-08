from pydantic import BaseModel
from typing import Optional

# For validation purposes on the receiving end
# not necessary since we are just receiving a plain text, which contains the xml 
class PageSchema(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True

class SearchMask(BaseModel):
    content: Optional[str] = None

class SearchResult(BaseModel):
    id: int
    title: str