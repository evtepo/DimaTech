from uuid import UUID

from pydantic import BaseModel


class UserMixin(BaseModel):
    first_name: str
    last_name: str
    email: str
    is_stuff: bool = False


class UserCreate(UserMixin):
    password: str


class UserUpdate(UserMixin): ...


class UserInfo(BaseModel):
    id: UUID
    email: str
    full_name: str


class UserLogIn(BaseModel):
    email: str
    password: str


class UserDelete(BaseModel):
    email: str
