import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from Routes import router as api_router


# Load environment variables
load_dotenv()


# Create FastAPI application
app = FastAPI(
    title="LegalEase API",
    description="Backend service for AI-powered legal document generation",
    version="1.0.0"
)


# Enable CORS for Streamlit frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(api_router)


# Health check endpoint
@app.get("/", tags=["Health"])
def root_health_check():
    return {
        "status": "online",
        "message": "LegalEase API is running successfully",
        "model_configured": os.getenv(
            "GEMINI_MODEL",
            "gemini-1.5-pro"
        )
    }


# Run application directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "Main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )