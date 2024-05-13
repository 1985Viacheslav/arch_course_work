import motor.motor_asyncio
from settings import settings

url_prod = f'mongodb://{settings.MONGO_INITDB_ROOT_USERNAME}:{settings.MONGO_INITDB_ROOT_PASSWORD}@mongo:27017'
url_localhost = f'mongodb://localhost:27017'

# Подключение к MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(
    url_prod,
    uuidRepresentation="standard"
)

db = client['chats']

# Получение коллекций наших моделей
GroupChat = db['group_chat']
PtpChat = db['ptp_chat']

