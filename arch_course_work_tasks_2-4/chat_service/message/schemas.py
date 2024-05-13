import datetime

from pydantic import BaseModel, Field

from user_service.user.schemas import UserRead


class MessageSchema(BaseModel):
    """ Модель сообщения """
    text: str
    user: UserRead
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
