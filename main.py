from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

from app.routes import router
from app.database_config import engine
import app.models as models

# Load environment variables from the .env file
load_dotenv()

# Create all tables in the database if they don't already exist
models.Base.metadata.create_all(bind=engine)

# Initialize a FastAPI application
app = FastAPI()

# Include the custom router in the FastAPI application
app.include_router(router)

# Run the FastAPI application using Uvicorn if this script is the main entry point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)