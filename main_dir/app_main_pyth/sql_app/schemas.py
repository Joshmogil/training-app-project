from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import orm
from sqlalchemy.sql.sqltypes import String

""" class SettingsBase(BaseModel):
    goal : str
    split : str
    days_per_week : int
    preffered_days : str    

class SettingsCreate(SettingsBase):
    user_id : int

class Settings(SettingsBase):
    id:int

    class Config:
        orm_mode = True """
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


    

