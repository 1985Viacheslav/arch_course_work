from chat_service.ptp_chat.schemas import PtpChatSchema


async def convert_ptp_chat_model_to_dict(ptp_chat: PtpChatSchema):
    ptp_chat.messages = [message.model_dump() for message in ptp_chat.messages]

    return ptp_chat
