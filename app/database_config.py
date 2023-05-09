from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# If database credentials are set as environment variables, use them
# otherwise, prompt the user to enter the database credentials
if "DB_USER" in os.environ and "DB_PASSWORD" in os.environ:
    username = os.environ["DB_USER"]
    pw = os.environ["DB_PASSWORD"]
else:
    print("Create an .env file to avoid inserting credentials")
    username = input("username: ")
    pw = input("password: ")

# If the database URL is set as an environment variable, use it
# otherwise, construct the database URL using the entered credentials
if "DATABASE_URL" in os.environ:
    DATABASE_URL = os.environ["DATABASE_URL"].replace("username", username).replace("password", pw)
    print("TEEEEEEEEEESSSSSSSSSSSST")
    print("TEEEEEEEEEESSSSSSSSSSSST")
    print(DATABASE_URL)
else:
    DATABASE_URL = f'postgresql://{username}:{pw}@localhost:5432/craftworks_wiki_db'

# Create a SQLAlchemy engine using the database URL
engine = create_engine(DATABASE_URL)

# Creates a full-text search index if it doesn't exist
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

# Call the optimization function to create the index if needed
optimization(engine)

# Create a session factory for creating new database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for creating new ORM models
Base = declarative_base()
