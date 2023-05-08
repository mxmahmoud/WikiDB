from pydantic import BaseModel
from typing import Optional

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