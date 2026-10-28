"""
Author: Sumit
Created: 10/28/2026
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.modules.users.schemas import UserCreate, UserRead
from app.modules.users.service import EmailAlreadyRegisteredError, UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserService:
    return UserService(session)


ServiceDep = Annotated[UserService, Depends(get_service)]


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(data: UserCreate, service: ServiceDep):
    try:
        return await service.register(data)

    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
