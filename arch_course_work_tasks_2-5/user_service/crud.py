import json
import os
from typing import AsyncIterator

from redis import Redis, asyncio as aioredis
from sqlalchemy import select, update, delete, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database.postgres_db import async_session
from settings import settings
from user_service.models import User
from user_service.schemas.user_schemas import UserReadSchema


async def init_redis_pool() -> AsyncIterator[Redis]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}", encoding="utf-8",
                              decode_responses=False)
    yield redis
    await redis.close()


def obj_to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


async def get_user(username: str):
    async with async_session() as session:
        stmt = select(User).filter(User.username == username)
        user = await session.execute(stmt)
        user = user.scalar_one_or_none()

        return user


async def update_user(user: User, data: dict, session: AsyncSession):

    stmt = update(User).where(User.id == user.id).values(**data)
    await session.execute(stmt)
    await session.commit()


async def upload_image_in_db(user: User, avatar_url: str, session: AsyncSession):
    stmt = update(User).where(User.id == user.id).values(avatar_url=avatar_url)
    await session.execute(stmt)
    await session.commit()


async def delete_user(user: User, session: AsyncSession):

    stmt = delete(User).where(User.id == user.id)

    if os.path.exists(user.avatar_url):
        os.remove(user.avatar_url)

    await session.execute(stmt)
    await session.commit()


async def get_user_by_id(user_id: int, session: AsyncSession):
    stmt = select(User).where(User.id == user_id)
    user = await session.scalar(stmt)

    return user

