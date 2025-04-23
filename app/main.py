from fastapi import FastAPI
from app.api import chat

app = FastAPI(title="FreshBot AI")

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
