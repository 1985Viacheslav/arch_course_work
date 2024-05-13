from chat_service.group_chat.schemas import GroupChatSchema


async def convert_group_model_to_dict(group: GroupChatSchema):
    """Конвертирует модель группы в словарь для записи в Монго"""
    group.members = [member.model_dump() for member in group.members]
    group.messages = [message.model_dump() for message in group.messages]

    return group
