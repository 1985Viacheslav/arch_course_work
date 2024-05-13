from fastapi_users import schemas
from pydantic import ConfigDict, EmailStr, alias_generators


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    last_name: str
    email: EmailStr
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False


class UserCreate(schemas.BaseUserCreate):
    model_config = ConfigDict(alias_generator=alias_generators.to_camel, from_attributes=True, populate_by_name=True)

    name: str
    last_name: str
    password: str
    email: EmailStr
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False


class UserUpdate(schemas.BaseUserUpdate):
    name: str
    last_name: str
    password: str
    email: EmailStr
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False
