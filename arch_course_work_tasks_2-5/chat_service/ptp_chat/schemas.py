from beanie import PydanticObjectId
from pydantic import BaseModel, Field
from chat_service.message.schemas import MessageSchema
from user_service.schemas.user_schemas import UserReadSchema


class PtpChatSchema(BaseModel):
    """
    Создаем схему для хранения PTP-чата
    """
    id: PydanticObjectId | None = Field(validation_alias='_id', default=None)
    user_sender: UserReadSchema
    user_getter: UserReadSchema
    messages: list[MessageSchema] | None = []
