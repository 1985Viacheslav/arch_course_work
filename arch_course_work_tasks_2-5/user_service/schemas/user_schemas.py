from pydantic import ConfigDict, alias_generators, BaseModel


class UserReadSchema(BaseModel):
    model_config = ConfigDict(alias_generator=alias_generators.to_camel, from_attributes=True, populate_by_name=True)
    id: int
    name: str | None = None
    last_name: str | None = None
    username: str
    is_active: bool | None = True


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(alias_generator=alias_generators.to_camel, from_attributes=True, populate_by_name=True)

    name: str | None = ''
    last_name: str | None = ''
    password: str
    username: str
    is_active: bool | None = True


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(alias_generator=alias_generators.to_camel, from_attributes=True, populate_by_name=True)
    name: str | None = None
    last_name: str | None = None


class UserInDBSchema(UserReadSchema):
    hashed_password: str
