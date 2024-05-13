from fastapi import APIRouter, HTTPException, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres_db import get_async_session
from .auth import auth_backend
from .manager import get_user_manager
from .models import User
from user_service.user.schemas import UserRead

router = APIRouter(
    tags=['users'],
    prefix='/users',
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)


@router.get('/{name}/{last_name}', response_model=UserRead, dependencies=[Depends(current_superuser)])
async def get_user_by_name_and_last_name(name: str, last_name: str, session: AsyncSession = Depends(get_async_session)):
    # Поиск пользователя по имени и фамилии
    try:
        stmt = select(User).filter(User.name.contains('%' + name + '%')).filter(
            User.last_name.contains('%' + last_name + '%'))

        user = await session.execute(stmt)
        user = user.scalar()

        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail='User not found')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/', response_model=UserRead, dependencies=[Depends(current_superuser)])
async def get_user_by_email(email: str, session: AsyncSession = Depends(get_async_session)):
    # Поиск пользователя по email

    try:

        stmt = select(User).filter(User.email==email)

        user = await session.execute(stmt)

        if user:
            return user.scalar()
        else:
            raise HTTPException(status_code=404, detail='User not found')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
