from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Any

from backend.services.data_fetcher import get_reddit_trends, get_hackernews_trends
from backend.services.ai_analyzer import analyze_trends

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
def get_trends() -> list[dict[str, Any]]:
    """
    Endpoint returning real trends from Reddit and Hacker News.
    """
    reddit_data = get_reddit_trends(limit=5)
    hn_data = get_hackernews_trends(limit=5)
    
    # Combine both lists
    return reddit_data + hn_data

@app.get("/api/summary", response_model=dict[str, Any])
async def get_summary() -> dict[str, Any]:
    """
    Endpoint that fetches real trends and generates an AI summary using Gemini.
    """
    # a) Call Reddit and HackerNews
    reddit_data = get_reddit_trends(limit=5)
    hn_data = get_hackernews_trends(limit=5)
    combined_data = reddit_data + hn_data
    
    # b) Pass combined list to analyze_trends
    summary = await analyze_trends(combined_data)
    
    # c) Return the Gemini dictionary
    return summary
