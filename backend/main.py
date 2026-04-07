from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import webhook
from backend.database.database import Base, engine
import backend.models.lead
import backend.models.message
import backend.models.agency

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook.router)

@app.get("/")
async def root():
    return {"status": "ok"}

import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)