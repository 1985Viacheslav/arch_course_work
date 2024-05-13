from beanie import PydanticObjectId
from pydantic import BaseModel, Field
from chat_service.message.schemas import MessageSchema
from user_service.user.schemas import UserRead


class PtpChatSchema(BaseModel):
    """
    Создаем схему для хранения PTP-чата
    """
    id: PydanticObjectId | None = Field(validation_alias='_id', default=None)
    user_sender: UserRead
    user_getter: UserRead
    messages: list[MessageSchema] | None = []
