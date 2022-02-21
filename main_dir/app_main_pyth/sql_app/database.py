
from hashlib import sha3_224
from sqlalchemy import create_engine, Table, Boolean, Column, ForeignKey, Integer, String, Sequence, MetaData, Identity, not_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import insert, select
import json


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:postgres1@localhost:5432/wamuu-life"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

metadata_obj = MetaData()

users = Table("users", metadata_obj,
    Column('id',Integer, Identity(start=1, cycle=True), primary_key=True, index=True),
    Column('email',String(100), unique=True, index=True),
    Column('hashed_password',String(255)),
    Column('is_active',Boolean),
    Column('needs_setup',Boolean)
)

splits = Table("splits", metadata_obj,
    Column('id',Integer, Identity(start=1, cycle=True), primary_key=True, index=True),
    Column('name',String(55), unique=True, index=True)
    
)

goals = Table("goals", metadata_obj,
    Column('id',Integer, Identity(start=1, cycle=True), primary_key=True, index=True),
    Column('name',String(55), unique=True, index=True),
    Column('cardio',Boolean),
    Column('base_reps',Integer),
    Column('periods',String(55))
    
)

settings =Table("settings", metadata_obj,

    Column('user_id',Integer, ForeignKey("users.id")),
    Column('goal',String(55)),
    Column('split',Integer, ForeignKey("splits.id")),
    Column('preffered_days',String(7)),
    Column('cardio',Boolean) 

)

user_misc =Table("user_misc", metadata_obj,

    Column('user_id',Integer, ForeignKey("users.id")),
    Column('current_period',String(55)),
    Column('variation_pref',String(55)),
    Column('str_level',String(55))    

)

exercises = Table("exercises", metadata_obj,
    Column('id',Integer, Identity(start=1, cycle=True), primary_key=True, index=True),
    Column('name',String(100)),
    Column('category',String(55)),
    Column('regularity_factor',Integer),
    Column('fatigue_factor',Integer),
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

sub_splits_muscle_groups = Table("sub_splits_muscle_groups", metadata_obj,
    Column('sub_splits',Integer, ForeignKey("sub_splits.id")),
    Column('muscle_groups',Integer, ForeignKey("muscle_groups.id"))
)

goals_exercises = Table("goals_exercises", metadata_obj,
    Column('goals',Integer, ForeignKey("goals.id")),
    Column('exercises',Integer, ForeignKey("exercises.id")),
    Column('core',Boolean)
)

muscle_groups = Table("muscle_groups", metadata_obj,
    Column('id',Integer, Identity(start=1, cycle=True), primary_key=True, index=True),
    Column('name',String(55), unique=True, index=True),
    Column('Novice',Integer),
    Column('Intermediate',Integer),
    Column('Advanced',Integer)
)

muscles_exercises = Table("muscles_exercises", metadata_obj,
    Column('muscles',Integer, ForeignKey("muscle_groups.id")),
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

user_future_workouts = Table("user_future_workouts", metadata_obj,
    Column('user_id',Integer, ForeignKey("users.id"),unique=True),
    Column('workout_object',String(2255)),    
)

user_past_workouts = Table("user_past_workouts", metadata_obj,
    Column('user_id',Integer, ForeignKey("users.id")),
    Column('workout_object',String(2255)),    
)

user_schedule= Table("user_schedule", metadata_obj,
    Column('user_id',Integer, ForeignKey("users.id"),unique=True),
    Column('schedule',String(1000)),    
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

        ins = exercises.insert().values(name=name,category=cat,description = desc,regularity_factor=rf,fatigue_factor=ff)

        db.execute(ins)
        db.commit()
        
    db.close()

#muscle_groups table and muscles _exercises

db = SessionLocal()
s = select(muscle_groups.c.id).where(muscle_groups.c.id == 1)
trueIfTableContainsData = False
for row in db.execute(s):
        trueIfTableContainsData = True   
db.close()

if(trueIfTableContainsData is False):
    print("Populating muscle groups table ...")
    jsonfile = open("m_muscle_groups.json")
    data = json.load(jsonfile)
    db = SessionLocal()

    for x in data:
        name = x["name"]
        nis = x["Novice"]
        iis = x["Intermediate"]
        ais = x["Advanced"]

        ins = muscle_groups.insert().values(name=name, Novice=nis,Intermediate=iis,Advanced=ais)
        result = db.execute(ins)
        muscleGroupId = dict(result.inserted_primary_key)["id"]

        s = select(exercises.c.id).where(exercises.c.description.contains(name))
        
        for row in db.execute(s):
            dict(row)
            ins = muscles_exercises.insert().values(muscles=muscleGroupId, exercises=row["id"])
        
            result = db.execute(ins)
        
    
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

    print("Connecting the dots...")
    for x in data:
        
        name = x["name"]
        
        ins = sub_splits.insert().values(name=name)

        result = db.execute(ins)
        newSsId = result.inserted_primary_key

        for y in x["exercise_categories"]:

            #Cleans up the returned Id 
            newSubSplitId = ""
            for k in str(newSsId):

                if k.isdigit():

                    newSubSplitId += k

            # selects exercises in category y
            s = select(exercises.c.id).where(exercises.c.category == y)
            
            for row in db.execute(s):
                
                exerciseId = row.id

                ins = sub_splits_exercises.insert().values(sub_splits=int(newSubSplitId), exercises = exerciseId)
                db.execute(ins)

    for x in data:
        for y in x["muscle_groups"]:
            
            s = select(muscle_groups.c.id).where(y==muscle_groups.c.name)
            for row in db.execute(s):                
                muscle_groupId = row.id
                s2 = select(sub_splits.c.id).where(sub_splits.c.name == x["name"])
                
                sub_splitId = 0
                for row in db.execute(s2):
                
                    sub_splitId = row.id


                ins = sub_splits_muscle_groups.insert().values(sub_splits=sub_splitId, muscle_groups = muscle_groupId)
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
            s = select(sub_splits.c.id).where(sub_splits.c.name==y)
            ssId = 0
            for row in db.execute(s):       
                ssId = row.id
            ins = splits_sub_splits.insert().values(split_id=int(newSplitId), sub_splits = ssId)
            db.execute(ins)
        db.commit()      
    db.close()


#Goals table and goals_exercises
db = SessionLocal()
s = select(goals.c.id).where(goals.c.id == 1)
trueIfTableContainsData = False
for row in db.execute(s):
        trueIfTableContainsData = True   
db.close()

if(trueIfTableContainsData is False):
    print("Populating goals table ...")
    jsonfile = open("m_goals.json")
    data = json.load(jsonfile)
    db = SessionLocal()
    
    
    insertList = []
    for x in data:
        name = x["name"]
        cardio = x["cardio"]
        reps= x["base_reps"]
        periods = x["periods"]      
        ins = goals.insert().values(name=name, cardio= cardio,base_reps=reps,periods=periods)
        result = db.execute(ins)
        goalId = dict(result.inserted_primary_key)["id"]
        

        s = select(exercises.c.id).where(exercises.c.description.contains("Core("+name+")"))

        for row in db.execute(s):
            dict(row)
            insertList.append((goalId,row["id"],True))

        s = select(exercises.c.id).where((exercises.c.description.contains(name)) & not_(exercises.c.description.contains("Core("+name+")")))

        for row in db.execute(s):
            dict(row)
            insertList.append((goalId,row["id"],False))

        s = select(exercises.c.id).where(exercises.c.description.contains("All"))

        for row in db.execute(s):
            dict(row)

            if((goalId,row["id"],False) and (goalId,row["id"],True) not in insertList):

                insertList.append((goalId,row["id"],False))

    for x in insertList:

        ins = goals_exercises.insert().values(goals=x[0], exercises=x[1],core = x[2])
        result = db.execute(ins)
        
    
    db.commit()      
    db.close()

