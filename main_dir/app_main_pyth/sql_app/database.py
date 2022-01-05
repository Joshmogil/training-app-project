from sqlalchemy import create_engine, Table, Boolean, Column, ForeignKey, Integer, String, Sequence, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:postgres1@localhost:5432/fitness-app"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

metadata_obj = MetaData()

users = Table("users", metadata_obj,
    Column('id',Integer, Sequence('some_id_seq'), primary_key=True, index=True),
    Column('email',String, unique=True, index=True),
    Column('hashed_password',String),
    Column('is_active',Boolean),
    
)

settings =Table("settings", metadata_obj,

    Column('user_id',Integer, ForeignKey("users.id")),
    Column('goal',String),
    Column('split',String),
    Column('days_per_week',Integer),
    Column('preffered_days',String) 

)

metadata_obj.create_all(engine)
