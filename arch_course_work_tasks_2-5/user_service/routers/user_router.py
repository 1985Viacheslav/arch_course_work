import json
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_cache.decorator import cache
from redis.asyncio.client import Redis
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres_db import get_async_session
from user_service.crud import update_user, get_user, delete_user, init_redis_pool, obj_to_dict, get_user_by_id
from user_service.helpers import get_current_active_user, request_key_builder
from user_service.models import User
from user_service.schemas.user_schemas import UserReadSchema, UserUpdateSchema

router = APIRouter(
    tags=['user'],
    prefix='/user',
)

@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserReadSchema)
@cache(expire=300)
async def get_me(current_user: Annotated[User, Depends(get_current_active_user)]):

    return current_user


@router.get('/{user_id}', response_model=UserReadSchema, dependencies=[Depends(get_current_active_user)])
@cache(expire=300, key_builder=request_key_builder)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await get_user_by_id(user_id=user_id, session=session)

    return user


@router.patch('/me', response_model=UserReadSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_me(new_data: UserUpdateSchema, current_user: Annotated[User, Depends(get_current_active_user)],
                    session: AsyncSession = Depends(get_async_session), redis: Redis = Depends(init_redis_pool)):
    new_data = new_data.model_dump(exclude_none=True)

    await update_user(user=current_user, data=new_data, session=session)

    user = await get_user(current_user.username)

    key = user.id
    value = UserReadSchema.model_validate(obj_to_dict(user))
    await redis.set(key, json.dumps(value.model_dump()), 5 * 60)

    return await get_user(current_user.username)


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(current_user: Annotated[User, Depends(get_current_active_user)],
                    session: AsyncSession = Depends(get_async_session), redis: Redis = Depends(init_redis_pool)):

    await delete_user(user=current_user, session=session)

    await redis.delete(current_user.id)

    return {'message': 'User deleted'}


@router.get('/search/{mask}', response_model=UserReadSchema, dependencies=[Depends(get_current_active_user)])
@cache(expire=300)
async def get_user_by_mask(mask: str, session: AsyncSession = Depends(get_async_session)):
    # Поиск пользователя по имени и фамилии
    try:
        stmt = select(User).filter(or_(User.name.contains('%' + mask + '%'),
                                   User.last_name.contains('%' + mask + '%')))

        user = await session.execute(stmt)
        user = user.scalar()

        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail='User not found')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/', response_model=UserReadSchema, dependencies=[Depends(get_current_active_user)])
@cache(expire=300)
async def get_user_by_username(username: str):
    # Поиск пользователя по username

    try:

        if user := await get_user(username):
            return user
        else:
            raise HTTPException(status_code=404, detail='User not found')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
