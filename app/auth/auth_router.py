from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Form, Body
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth.auth import create_access_token, hash_password, create_refresh_token, authenticate_user
from app.auth.auth_schemas import Token
from app.database import get_async_session
from app.db_config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY, ALGORITHM
from app.repositories.user_repository import UserRepository
from app.schemas import UserRead, UserCreate

router = APIRouter(
    tags=["Admin panel AUTH"],
    prefix="/auth"
)


@router.post("/login", response_model=Token, name="Login by form data (username, password etc.)")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    """
    :param form_data: username, password etc.
    :param session: AsyncSession
    :return: access_token, refresh_token, token_type

    This function is used to log in the system with form data (username, password etc.)
    and return access and refresh tokens.
    """
    if form_data.username and form_data.password:
        user = await authenticate_user(form_data.username, form_data.password, session)
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


@router.post("/login_by_token", response_model=Token, name="Login by previously received ACCESS TOKEN")
async def login_by_token(
    access_token: str = Body(...),
    session: AsyncSession = Depends(get_async_session)
):
    """
    :param access_token: ACCESS TOKEN taken from 'body' of the request
    :param session: AsyncSession
    :return: access_token, refresh_token, token_type

    This function is used to log in the system with previously received access token
    and return new access and refresh tokens.
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )

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

    user_repository = UserRepository(session)
    user = await user_repository.get_user_by_username(username=username)

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


@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    """
    :param user: UserCreate
    :param session: AsyncSession
    :return: User

    This function is used to register new user (insert new user into the database via 'user_repository')
    and return 'User' model instance.
    """
    user_repository = UserRepository(session)
    previously_registered_user_check_by_username = await user_repository.get_user_by_username(user.username)
    previously_registered_user_check_by_email = await user_repository.get_user_by_email(user.email)

    if previously_registered_user_check_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    elif previously_registered_user_check_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user.hashed_password = hash_password(user.hashed_password)
    return await user_repository.create_user(user)


@router.post("/refresh", response_model=Token, name="Refresh tokens by previously received REFRESH TOKEN")
async def refresh_token(
    refresh_token: str = Body(...),
    session: AsyncSession = Depends(get_async_session)
):
    """
    :param refresh_token: REFRESH TOKEN taken from 'body' of the request
    :param session: AsyncSession
    :return: access_token, refresh_token, token_type

    This function is used to log in the system with previously received refresh token
    in case of '401 Unauthorized' by '/login_by_token' endpoint response (loss or damaged access token)
    and return new access and refresh tokens.
    """
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )

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

    user_repository = UserRepository(session)
    user = await user_repository.get_user_by_username(username=username)

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
