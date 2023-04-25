from pydantic import BaseModel, EmailStr
from typing import Optional, Union, List

from pydantic.datetime_parse import datetime

from .link import Link


class UserBase(BaseModel):
    username: Optional[str] = None



class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str
    user_ip: str
    user_agent: str


class UserDB(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    is_active: bool
    registered_at: datetime
    user_links: Optional[List[Link]] = list()

    class Config:
        orm_mode = True




# Additional properties stored in DB


