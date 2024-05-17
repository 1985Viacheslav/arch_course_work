import datetime

from pydantic import BaseModel, Field

from user_service.schemas.user_schemas import UserReadSchema


class MessageSchema(BaseModel):
    """ Модель сообщения """
    text: str
    user: UserReadSchema
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
