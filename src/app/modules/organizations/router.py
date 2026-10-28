from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.modules.organizations.schemas import OrganizationCreate, OrganizationRead
from app.modules.organizations.service import (
    OrganizationService,
    SlugAlreadyExistsError,
)

router = APIRouter(prefix="/organizations", tags=["organizations"])


def get_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> OrganizationService:
    return OrganizationService(session)


ServiceDep = Annotated[OrganizationService, Depends(get_service)]


@router.post("", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
async def create_organization(data: OrganizationCreate, service: ServiceDep):
    try:
        return await service.create(data)
    except SlugAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("", response_model=list[OrganizationRead])
async def list_organizations(
    service: ServiceDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    return await service.list_organizations(limit=limit, offset=offset)
