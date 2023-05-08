from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

from app.routes import router
from app.database_config import engine
import app.models as models

load_dotenv()

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



    
