from sqlalchemy import create_engine, Table, Boolean, Column, ForeignKey, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()

metadata_obj = MetaData()

users = Table("users", metadata_obj,
    Column('id',Integer, primary_key=True, index=True),
    Column('email',String, unique=True, index=True),
    Column('hashed_password',String),
    Column('is_active',Boolean),
    sqlite_autoincrement=True
)

settings =Table("settings", metadata_obj,

    Column('user_id',Integer, ForeignKey("users.id"))

)

metadata_obj.create_all(engine)
