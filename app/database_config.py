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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
