from sqlalchemy import  Column, Integer, String
from app.database_config import Base


class Page(Base):
    __tablename__ ="pages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)



