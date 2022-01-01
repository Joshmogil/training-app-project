from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String, MetaData
from sqlalchemy.orm import relationship

#from .database import Base



    





""" class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    settings = relationship("Settings", back_populates="user")

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)  
    goal = Column(String, default="full_body")
    split = Column(String, default="general_health")
    days_per_week = Column(Integer, default=4)
    preffered_days = Column(String, default="0110110") # 1 = preffered day, 0 = not preferred day
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="settings") """




