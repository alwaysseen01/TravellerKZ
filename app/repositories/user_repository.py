from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_by_username(self, username: str):
        result = await self.session.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        return user

    async def get_user_by_email(self, email: str):
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        return user

    async def create_user(self, user: UserCreate):
        new_user = User(**user.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
