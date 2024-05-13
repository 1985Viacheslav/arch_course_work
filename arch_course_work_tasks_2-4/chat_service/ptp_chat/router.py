from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chat_service.ptp_chat.schemas import PtpChatSchema
from chat_service.message.schemas import MessageSchema
from chat_service.ptp_chat.utils import convert_ptp_chat_model_to_dict
from database.postgres_db import get_async_session
from user_service.user.auth import auth_backend
from user_service.user.manager import get_user_manager
from user_service.user.models import User
from database.mongo_db import PtpChat
from user_service.user.schemas import UserRead

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

router = APIRouter(
    tags=["ptp_chat"],
    prefix="/ptp_chat",
)


@router.post('/send_message/{user_getter_id}', response_model=MessageSchema)
async def send_message(message_text: str, user_getter_id: int, user: User = Depends(current_active_verified_user),
                       session: AsyncSession = Depends(get_async_session)):
    """
    Получаем на вход сообщение и отправляем его пользователю, сохраняем в базе данных и возвращаем сообщение

    """
    try:
        message = MessageSchema(
            user=user,
            text=message_text
        )
        user = UserRead.model_validate(user, from_attributes=True)
        ptp_chat = await PtpChat.find_one({'user_sender': user.model_dump()})

        if ptp_chat is None:
            user_getter = await session.execute(select(User).filter(User.id == user_getter_id))

            ptp_chat = PtpChatSchema(
                user_sender=user,
                user_getter=UserRead.model_validate(user_getter.scalar(), from_attributes=True)
            )

            await PtpChat.insert_one(ptp_chat.model_dump(by_alias=False, exclude={'id'}))

            ptp_chat = await PtpChat.find_one({'user_sender': user.model_dump()})

        ptp_chat = PtpChatSchema.model_validate(ptp_chat, from_attributes=True)

        ptp_chat.messages.append(message)

        ptp_chat = await convert_ptp_chat_model_to_dict(ptp_chat)

        await PtpChat.update_one({'_id': ptp_chat.id}, {'$set': {'messages': ptp_chat.messages}})

        return message

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/get_messages', response_model=list[PtpChatSchema])
async def get_messages(user: User = Depends(current_active_verified_user)):
    """
    Получаем все сообщения пользователя
    """

    try:
        user = UserRead.model_validate(user, from_attributes=True)

        cursor = PtpChat.find(filter={'user_sender': user.model_dump()})

        ptp_chats_to_user = await cursor.to_list(length=None)

        return ptp_chats_to_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
