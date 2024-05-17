from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chat_service.group_chat.schemas import GroupChatSchema
from chat_service.group_chat.utils import convert_group_model_to_dict
from chat_service.message.schemas import MessageSchema
from chat_service.ptp_chat.router import get_current_active_user
from database.mongo_db import GroupChat
from database.postgres_db import get_async_session
from user_service.models import User
from user_service.schemas.user_schemas import UserReadSchema

# Инициализация fastapi_users для проверки авторизации





# Создание маршрутов

router = APIRouter(
    tags=["group_chat"],
    prefix="/group_chat",
)


# Далее идет реализация эндпоинтов
@router.post("/create", response_model=GroupChatSchema)
async def create_group(group_name: str, user: User = Depends(get_current_active_user)):
    """
    Получаем имя группы и пользователя,
    затем создаем новый объект(групповой чат) в базе данных и возвращаем его

    """

    try:
        group_chat = GroupChatSchema(group_name=group_name, members=[user])
        new_group = await GroupChat.insert_one(group_chat.model_dump(by_alias=False, exclude={'id'}))

        group = await GroupChat.find_one({"_id": new_group.inserted_id})

        return group

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add_member/{group_id}/{user_id}", response_model=GroupChatSchema,
             dependencies=[Depends(get_current_active_user)])
async def add_member_to_group(group_id: str, user_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Получаем id группы и id пользователя,
    затем добавляем пользователя в группу и возвращаем измененный объект(групповой чат)

    """
    try:
        stmt = select(User).filter(User.id == user_id)
        user = await session.execute(stmt)
        user = UserReadSchema.model_validate(user.scalar(), from_attributes=True)

        group = GroupChatSchema.model_validate(await GroupChat.find_one({"_id": ObjectId(group_id)}),
                                               from_attributes=True)
        group.members.append(user)

        group = await convert_group_model_to_dict(group)

        group = await GroupChat.find_one_and_update({'_id': ObjectId(group.id)}, {'$set': {'members': group.members}})

        return group

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/send_message/{group_id}', response_model=MessageSchema)
async def send_message(message_text: str, group_id: str, user: User = Depends(get_current_active_user)):
    """
    Получаем id группы и сообщение, сообщение добавляется в группу и возвращаем измененный объект(групповой чат)

    """
    try:

        message = MessageSchema(text=message_text, user=user)
        group = GroupChatSchema.model_validate(await GroupChat.find_one({"_id": ObjectId(group_id)}),
                                               from_attributes=True)
        group.messages.append(message)
        group = await convert_group_model_to_dict(group)

        await GroupChat.update_one({'_id': ObjectId(group.id)},
                                   {'$set': {'messages': group.messages}})

        return message

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{group_id}', dependencies=[Depends(get_current_active_user)], response_model=GroupChatSchema)
async def get_group(group_id: str):
    """
    Получаем id группы, возвращаем объект(групповой чат)

    """

    try:
        group = await GroupChat.find_one({'_id': ObjectId(group_id)})

        return group

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
