import asyncio

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate


class EmailAlreadyRegisteredError(Exception):
    def __init__(self, email: str) -> None:
        super().__init__("Email already registered")
        self.email = email


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = UserRepository(session)

    async def register(self, data: UserCreate) -> User:
        if await self.repo.get_by_email(data.email):
            raise EmailAlreadyRegisteredError(data.email)

        hashed = await asyncio.to_thread(hash_password, data.password)

        user = User(
            email=data.email,
            hashed_password=hashed,
            full_name=data.full_name,
        )
        try:
            await self.repo.add(user)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise EmailAlreadyRegisteredError(data.email) from None

        return user