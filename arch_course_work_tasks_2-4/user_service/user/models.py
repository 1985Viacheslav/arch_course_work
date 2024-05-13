from datetime import datetime
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, Date
from sqlalchemy.ext.asyncio import AsyncSession
from database.postgres_db import Base, get_async_session


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=200), nullable=False)
    last_name: str = Column(String(length=200), nullable=False)
    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    registered_at: Date = Column(TIMESTAMP, default=datetime.utcnow)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
