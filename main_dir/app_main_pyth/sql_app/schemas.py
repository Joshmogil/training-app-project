from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import orm
from sqlalchemy.sql.sqltypes import String

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

class LoginResponse(BaseModel):
    token: str
    user: User


    

