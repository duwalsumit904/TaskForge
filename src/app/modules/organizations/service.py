"""
Author: Sumit
Created: 10/28/2026
"""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.organizations.models import Organization
from app.modules.organizations.repository import OrganizationRepository
from app.modules.organizations.schemas import OrganizationCreate


class SlugAlreadyExistsError(Exception):
    def __init__(self, slug: str) -> None:
        super().__init__(f"organization slug '{slug}' is already taken")

        self.slug = slug


class OrganizationService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = OrganizationRepository(session)

    async def create(self, data: OrganizationCreate) -> Organization:
        if await self.repo.get_by_slug(data.slug):
            raise SlugAlreadyExistsError

        organization = Organization(name=data.name, slug=data.slug)

        try:
            await self.repo.add(organization)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise SlugAlreadyExistsError(data.slug) from None
        return organization

    async def list_organizations(self, limit: int = 50, offset: int = 0) -> list[Organization]:
        return await self.repo.list_all(limit=limit, offset=offset)
