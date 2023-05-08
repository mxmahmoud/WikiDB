from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import Optional

# for validation purposes on the receiving end
# not necessary since we are just receiving a plain text, which contains the xml 
class PageSchema(BaseModel):
    #id: Optional[UUID] = uuid4
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True

class SearchMask(BaseModel):
    search_mask: str

class SearchResult(BaseModel):
    id: int
    title: str