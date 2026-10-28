"""
Author: Sumit
Created: 10/27/2026
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.organizations.models import Organization


class OrganizationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_slug(self, slug: str) -> Organization | None:
        result = await self.session.execute(select(Organization).where(Organization.slug == slug))
        return result.scalar_one_or_none()

    async def list_all(self, limit: int = 50, offset: int = 0) -> list[Organization]:
        result = await self.session.execute(
            select(Organization)
            .order_by(Organization.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def add(self, organization: Organization) -> Organization:
        self.session.add(organization)
        await self.session.flush()
        return organization
