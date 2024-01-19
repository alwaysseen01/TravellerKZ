from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserRead(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str | None = None
    role: str


class UserCreate(BaseModel):
    username: str
    hashed_password: str
    first_name: str
    last_name: str
    email: str | None = None
    role: str


class UserInDB(UserRead):
    hashed_password: str
