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
    Column('id',Integer, Identity(start=1, cycle=True), primary_key=True, index=True),
    Column('email',String(100), unique=True, index=True),
    Column('hashed_password',String(255)),
    Column('is_active',Boolean),
    
)

splits = Table("splits", metadata_obj,
    Column('id',Integer, Identity(start=1, cycle=True), primary_key=True, index=True),
    Column('name',String(55), unique=True, index=True)
    
)

settings =Table("settings", metadata_obj,

    Column('user_id',Integer, ForeignKey("users.id")),
    Column('goal',String(55)),
    Column('split',Integer, ForeignKey("splits.id")),
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

sub_splits = Table("sub_splits", metadata_obj,
    Column('id',Integer, Identity(start=1, cycle=True), primary_key=True, index=True),
    Column('name',String(55), unique=True, index=True)
)

splits_sub_splits = Table("splits_sub_splits", metadata_obj,
    Column('split_id',Integer, ForeignKey("splits.id")),
    Column('sub_splits',Integer, ForeignKey("sub_splits.id")),
)

sub_splits_exercises = Table("sub_splits_exercises", metadata_obj,
    Column('sub_splits',Integer, ForeignKey("sub_splits.id")),
    Column('exercises',Integer, ForeignKey("exercises.id")),
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

#EXERCISE TABLE
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

#SUB_SPLITS AND SUB_SPLITS_EXERCISES TABLE
#Check if there is anything in database
db = SessionLocal()

s = select(sub_splits.c.id).where(sub_splits.c.id == 1)
trueIfSsTableContainsData = False
for row in db.execute(s):
        trueIfSsTableContainsData = True
        
db.close()

if(trueIfSsTableContainsData is False):

    print("Populating sub_splits table ...")

    jsonfile = open("m_sub_splits.json")
    data = json.load(jsonfile)

    db = SessionLocal()

    for x in data:
        
        name = x["name"]
        
        ins = sub_splits.insert().values(name=name)

        result = db.execute(ins)
        newSsId = result.inserted_primary_key

        for y in x["exercises"]:

            newSubSplitId = ""
            for x in str(newSsId):

                if x.isdigit():

                    newSubSplitId += x

            ins = sub_splits_exercises.insert().values(sub_splits=int(newSubSplitId), exercises = y)

            db.execute(ins)

    db.commit()

        
    db.close()






#SPLITS TABLE
#Check if there is anything in database

db = SessionLocal()

s = select(splits.c.id).where(splits.c.id == 1)
trueIfTableContainsData = False
for row in db.execute(s):
        trueIfTableContainsData = True
        
db.close()

if(trueIfTableContainsData is False):

    print("Populating splits table ...")

    jsonfile = open("m_splits.json")
    data = json.load(jsonfile)

    db = SessionLocal()

    for x in data:
        
        name = x["name"]
        
        ins = splits.insert().values(name=name)

        result = db.execute(ins)

        splitId = result.inserted_primary_key

        for y in x["sub_splits"]:
            #inserts for sss table begin
            newSplitId = ""
            for x in str(splitId):

                if x.isdigit():

                    newSplitId += x

            print(y)
            
            s = select(sub_splits.c.id).where(sub_splits.c.name==y)
            ssId = 0
            for row in db.execute(s):
                print(row)
                ssId = row.id


            ins = splits_sub_splits.insert().values(split_id=int(newSplitId), sub_splits = ssId)

            db.execute(ins)

        db.commit()
        
    db.close()
