import contextlib
from fastapi_users.exceptions import UserAlreadyExists
from user_service.user.manager import get_user_manager
from user_service.user.models import get_user_db
from user_service.user.schemas import UserCreate

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

# функция для создания пользователя отдельно от приложения
async def create_user(email: str, password: str, name: str, last_name: str, session, is_superuser: bool = False):
    try:

        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                user = await user_manager.create(
                    UserCreate(
                        email=email, password=password, is_superuser=is_superuser, name=name, last_name=last_name,
                        is_verified=True
                    )
                )
                return user

    except UserAlreadyExists:
        print(f"User {email} already exists")
