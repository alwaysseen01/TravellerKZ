from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.repositories.user_repository import UserRepository
from app.schemas import UserRead

router = APIRouter(
    tags=["Users"],
)


@router.get("/users/{username}", response_model=UserRead)
async def get_user_by_username(username: str, session: AsyncSession = Depends(get_async_session)):
    user_repository = UserRepository(session)

    user = await user_repository.get_user_by_username(username)
    return user


@router.get("/users/{email}", response_model=UserRead)
async def get_user_by_email(email: str, session: AsyncSession = Depends(get_async_session)):
    user_repository = UserRepository(session)

    user = await user_repository.get_user_by_email(email)
    return user
