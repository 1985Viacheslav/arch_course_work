import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from database.postgres_db import get_async_session
from user_service.crud import get_user, init_redis_pool, obj_to_dict
from user_service.helpers import get_current_user_from_refresh, get_current_active_user
from user_service.jwt import create_access_token, create_refresh_token
from user_service.models import User
from user_service.schemas.token_schemas import Token
from user_service.schemas.user_schemas import UserReadSchema, UserCreateSchema
from user_service.validation import authenticate_user, get_password_hash

router = APIRouter(
    tags=['auth'],
    prefix='/auth',
)


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )

    refresh_token = create_refresh_token(
        data={"sub": user.username}
    )

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post('/refresh', response_model=Token, response_model_exclude_none=True, )
async def refresh_token(user: UserReadSchema = Depends(get_current_user_from_refresh)):
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post('/logout', dependencies=[Depends(get_current_active_user)])
async def logout():
    return {'message': 'logout'}


@router.post('/register')
async def create_new_user(new_user: UserCreateSchema, session: AsyncSession = Depends(get_async_session),
                          redis: Redis = Depends(init_redis_pool)):
    user_data = new_user.model_dump(exclude={'password'})

    user_data['hashed_password'] = get_password_hash(new_user.password)

    user = User(**user_data)

    session.add(user)

    await session.commit()

    user = await get_user(new_user.username)

    value = UserReadSchema.model_validate(obj_to_dict(user))

    await redis.set(name=user.id, value=json.dumps(value.model_dump()), ex=5 * 60)
