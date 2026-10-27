"""
Author: Sumit
Created: 10/27/2026
"""

from fastapi import FastAPI

from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}
