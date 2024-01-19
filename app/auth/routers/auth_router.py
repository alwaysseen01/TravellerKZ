from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Form, Body
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth.auth import create_access_token, hash_password, create_refresh_token
from app.auth.schemas import UserRead, Token, UserCreate
from app.auth.repositories.auth_repository import AuthRepository
from app.database import get_async_session
from app.db_config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY, ALGORITHM

router = APIRouter(
    tags=["Users"],
    prefix="/auth"
)


@router.get("/users/{username}", response_model=UserRead)
async def get_user_by_username(username: str, session: AsyncSession = Depends(get_async_session)):
    auth_repository = AuthRepository(session)

    user = await auth_repository.get_user_by_username(username)
    return user


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    if form_data.username and form_data.password:
        auth_repository = AuthRepository(session)
        user = await auth_repository.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(data={"sub": user.username}, expires_delta=refresh_token_expires)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    auth_repository = AuthRepository(session)
    db_user = await auth_repository.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    user.hashed_password = hash_password(user.hashed_password)
    return await auth_repository.create_user(user)


@router.post("/login_by_token", response_model=Token)
async def login_with_token(
    access_token: str = Body(...),
    session: AsyncSession = Depends(get_async_session)
):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    auth_repository = AuthRepository(session)

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await auth_repository.get_user_by_username(username=username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    new_refresh_token = create_refresh_token(data={"sub": user.username}, expires_delta=refresh_token_expires)

    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str = Body(...),
    session: AsyncSession = Depends(get_async_session)
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    auth_repository = AuthRepository(session)

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await auth_repository.get_user_by_username(username=username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    new_refresh_token = create_refresh_token(data={"sub": user.username}, expires_delta=refresh_token_expires)

    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
