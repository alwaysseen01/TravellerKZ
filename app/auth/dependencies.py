from fastapi import Depends, HTTPException
from typing import Annotated

from jose import jwt, JWTError
from starlette.status import HTTP_401_UNAUTHORIZED

from app.auth.repositories.auth_repository import get_user
from app.models import User
from .schemas import TokenData
from app.auth.repositories.auth_repository import oauth2_scheme
from ..database import get_db
from ..settings import settings


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username, db=Depends(get_db))
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
