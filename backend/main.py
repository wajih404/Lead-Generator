from fastapi import FastAPI

from backend.routes import webhook
from backend.database.database import Base, engine
import backend.models.lead
import backend.models.message
import backend.models.agency

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(webhook.router)

@app.get("/")
async def root():
    return {"status": "ok"}