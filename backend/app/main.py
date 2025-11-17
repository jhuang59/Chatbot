import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from .api import chat
from .db import init_db

app = FastAPI(
    title="LLM Chatbot API",
    description="A simple LLM-based chatbot API",
    version="0.1.0"
)

# Configure CORS for frontend
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://frontend:3000",  # For Docker Compose
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chatbot.db")
init_db(DATABASE_URL)

# Initialize database session factory for API routes
from .api.chat import init_db_session
init_db_session(DATABASE_URL)

# Include routers
app.include_router(chat.router)


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to LLM Chatbot API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
