from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers
from user_service.user.router import router as user_router
from chat_service.ptp_chat.router import router as ptp_router_router
from chat_service.group_chat.router import router as group_router
from user_service.user.auth import auth_backend
from user_service.user.manager import get_user_manager
from user_service.user.models import User
from user_service.user.schemas import UserRead, UserCreate, UserUpdate
from fixtures import router as fixture_router

# Инициализация FastAPI

app = FastAPI(
    title='MessengerProject'
)

# Инициализация FastAPIUsers, для авторизации

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

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

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(user_router)
app.include_router(ptp_router_router)
app.include_router(group_router)
app.include_router(fixture_router)
