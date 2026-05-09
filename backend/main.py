from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Any

# Initialize FastAPI application
app = FastAPI(
    title="Signal API",
    description="Core API backend for the Signal trend analysis platform."
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=dict[str, str])
async def root_health_check() -> dict[str, str]:
    """
    Health-check endpoint to verify the API is running.
    """
    return {
        "status": "online",
        "system": "Signal API is running"
    }

@app.get("/api/trends", response_model=list[dict[str, Any]])
async def get_mock_trends() -> list[dict[str, Any]]:
    """
    Mock endpoint returning a list of fake trends for testing purposes.
    """
    return [
        {
            "topic": "AI Agents",
            "category": "Technology",
            "growth": 85
        },
        {
            "topic": "Sustainable Packaging",
            "category": "Environment",
            "growth": 62
        },
        {
            "topic": "Remote Work Tools",
            "category": "Business",
            "growth": 45
        }
    ]
