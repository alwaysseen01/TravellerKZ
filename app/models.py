from sqlalchemy import Column, Integer, String, Boolean, Enum, MetaData
from sqlalchemy.orm import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), unique=True, index=True)
    first_name = Column(String(256), index=True)
    last_name = Column(String(256), index=True)
    email = Column(String(256), unique=True, index=True)
    hashed_password = Column(String(256))
    disabled = Column(Boolean, default=False)
    role = Column(Enum("user", "admin", name="role"), default="user")
