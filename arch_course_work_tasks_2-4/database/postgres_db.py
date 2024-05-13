from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import settings

DATABASE_URL = (f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
                f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")

Base = declarative_base()
# Создание движка и сессии для работы с БД Postgres, используем асинхронный режим работы с БД
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine)


# Функция для получения сессии для работы с БД Postgres
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
