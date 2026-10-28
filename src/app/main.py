"""
Author: Sumit
Created: 10/27/2026
"""

from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.session import get_session
from app.modules.organizations.router import router as organizations_router

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(organizations_router)


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}


@app.get("/health/db")
async def health_db(session: Annotated[AsyncSession, Depends(get_session)]):
    result = await session.execute(text("select 1"))
    return {"database": "ok", "result": result.scalar_one()}
