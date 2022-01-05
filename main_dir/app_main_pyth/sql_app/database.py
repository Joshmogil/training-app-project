from sqlalchemy import create_engine, Table, Boolean, Column, ForeignKey, Integer, String, Sequence, MetaData, Identity
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import insert, select
import json

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:postgres1@localhost:5432/fitness-app"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

metadata_obj = MetaData()

users = Table("users", metadata_obj,
    Column('id',Integer, Sequence('some_id_seq'), primary_key=True, index=True),
    Column('email',String(100), unique=True, index=True),
    Column('hashed_password',String(255)),
    Column('is_active',Boolean),
    
)

settings =Table("settings", metadata_obj,

    Column('user_id',Integer, ForeignKey("users.id")),
    Column('goal',String(55)),
    Column('split',String(55)),
    Column('days_per_week',Integer),
    Column('preffered_days',String(7)) 

)

exercises = Table("exercises", metadata_obj,
    Column('id',Integer, Identity(start=1, cycle=True), primary_key=True, index=True),
    Column('name',String(100)),
    Column('category',String(55)),
    Column('regularity_factor',Integer),
    Column('fatigue_factor',Integer),
    Column('parent_variation_id',Integer),
    Column('description',String(2555)),

)

user_exercises = Table("user_exercises", metadata_obj,
    Column('user_id',Integer, ForeignKey("users.id")),
    Column('exercises_id',Integer, ForeignKey("exercises.id")),
    Column('max',Integer),
    Column('ranked_choice', Integer),
    Column('favorite',Boolean),
    Column('active',Boolean)
    
)

metadata_obj.create_all(engine)

#database data loader

#Check if there is anything in database

db = SessionLocal()

s = select(exercises.c.id).where(exercises.c.id == 1)
trueIfExercisesContainsData = False
for row in db.execute(s):
        trueIfExercisesContainsData = True
        
db.close()

if(trueIfExercisesContainsData is False):

    print("Populating exercises table ...")

    jsonfile = open("m_exercises.json")
    data = json.load(jsonfile)

    db = SessionLocal()

    for x in data:
        
        name = x["name"]
        cat = x["category"]
        desc = x["description"]
        rf = x["regularity_factor"]
        ff = x["fatigue_factor"]
        pvi = x["parent_variation_id"]

        ins = exercises.insert().values(name=name,category=cat,description = desc,regularity_factor=rf,fatigue_factor=ff,parent_variation_id=pvi)

        db.execute(ins)
        db.commit()
        
    db.close()