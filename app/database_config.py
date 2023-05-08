from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

testing = True
if "WIKI_DB_USERNAME" in os.environ and "WIKI_DB_PW" in os.environ:
    username = os.environ["WIKI_DB_USERNAME"]
    pw = os.environ["WIKI_DB_PW"]
else:
    username = input("username: ")
    pw = input("password: ")

if "DATABASE_URL" in os.environ:
    DATABASE_URL = os.environ["DATABASE_URL"].replace("username", username).replace("password", pw)
else:
    DATABASE_URL = f'postgresql://{username}:{pw}@localhost:5432/craftworks_wiki_db'

engine = create_engine(DATABASE_URL)

def optimization(engine):
    index_name = "pages_full_text_search_idx"
    sql_create_index = f"""
    CREATE INDEX {index_name} ON pages USING gin(to_tsvector('english', title || ' ' || content));
    """
    sql_check_index_exists = f"""
    SELECT indexname FROM pg_indexes WHERE indexname = '{index_name}';
    """

    with engine.connect() as conn:
        if not conn.execute(sql_check_index_exists):
            conn.execute(sql_create_index)

optimization(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
