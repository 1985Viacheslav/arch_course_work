from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, alias_generators, Field

from chat_service.message.schemas import MessageSchema
from user_service.schemas.user_schemas import UserReadSchema


class GroupChatSchema(BaseModel):
    """
    Создаем схему группового чата
    """
    model_config = ConfigDict(alias_generator=alias_generators.to_camel, populate_by_name=True,
                              arbitrary_types_allowed=True)

    id: PydanticObjectId | None = Field(validation_alias='_id', default=None)
    members: list[UserReadSchema] | None = []
    messages: list[MessageSchema] | None = []
    group_name: str



