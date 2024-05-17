from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chat_service.group_chat.router import router as group_router
from chat_service.ptp_chat.router import router as ptp_router_router
from fixtures import router as fixture_router
from user_service.routers.auth_router import router as auth_router
from user_service.routers.user_router import router as user_router
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
# Инициализация FastAPI
app = FastAPI(
    title='MessengerProject'
)

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# Инициализация CORS
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение всех роутеров


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(ptp_router_router)
app.include_router(group_router)
app.include_router(fixture_router)
