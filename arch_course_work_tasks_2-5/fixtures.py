from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chat_service.group_chat.schemas import GroupChatSchema
from chat_service.message.schemas import MessageSchema
from chat_service.ptp_chat.schemas import PtpChatSchema
from database.mongo_db import PtpChat, GroupChat

from database.postgres_db import get_async_session
from user_service.models import User
from user_service.schemas.user_schemas import UserReadSchema, UserCreateSchema
from user_service.validation import get_password_hash

router = APIRouter(
    tags=['fixtures'],
    prefix='/fixtures'
)


@router.post('/')
async def add_fixtures(session: AsyncSession = Depends(get_async_session)):
    """
    Создание тестовых данных
    """


    try:
        new_user = UserCreateSchema(username="test_user", password="123", last_name="test_last_name", name="test_first_name")
        user_data = new_user.model_dump(exclude={'password'})
        user_data['hashed_password'] = get_password_hash(new_user.password)
        user = User(**user_data)
        session.add(user)

        new_user = UserCreateSchema(username="test_user2", password="1234", last_name="test",
                                    name="testov")

        user_data = new_user.model_dump(exclude={'password'})
        user_data['hashed_password'] = get_password_hash(new_user.password)
        user = User(**user_data)
        session.add(user)

        await session.commit()

        stmt = select(User)
        users = await session.execute(stmt)
        users = users.scalars().all()
        user1 = UserReadSchema.model_validate(users[0], from_attributes=True)

        user2 = UserReadSchema.model_validate(users[1], from_attributes=True)

        message1 = MessageSchema(
            text='text',
            user=user1
        )

        message2 = MessageSchema(
            text='text2',
            user=user2
        )

        group = GroupChatSchema(
            members=[user1.model_dump()],
            messages=[message1, message2],
            group_name="test_group"

        )

        await GroupChat.insert_one(group.model_dump(by_alias=False, exclude={'id'}))

        ptp_chat = PtpChatSchema(
            user_sender=user1.model_dump(),
            user_getter=user2.model_dump(),
            messages=[message1]
        )

        await PtpChat.insert_one(ptp_chat.model_dump(by_alias=False, exclude={'id'}))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
