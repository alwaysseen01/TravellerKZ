from pydantic import BaseModel


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
