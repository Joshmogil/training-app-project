from datetime import date
from sqlalchemy import MetaData, create_engine, select

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:postgres1@localhost:5432/fitness-app"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

metadata = MetaData()
metadata.reflect(bind=engine)

usersTable = metadata.tables['users']
schedulesTable = metadata.tables['user_schedule']
userExercisesTable = metadata.tables['user_exercises']
subSplitsExercisesTable = metadata.tables['sub_splits_exercises']
exercisesTable = metadata.tables['exercises']

def getExerciseData(userId):
    
    #get current day in schedule (sub split id)
    s = select(schedulesTable.c.schedule)
    schedule = ""
    for row in engine.execute(s):
        row = dict(row)
        schedule = row['schedule']
   
    subSplitDay = schedule[date.today().day-1]
    print(subSplitDay)
    #get exercises by current subsplit
    s = select(subSplitsExercisesTable.c.exercises).where(subSplitsExercisesTable.c.sub_splits == subSplitDay)
    
    localExercises = set()

    for row in engine.execute(s):
        row = dict(row)
        localExercises.add(row["exercises"])

    print(localExercises)

    #join exercises on user exercises by exercise id
    #add the exercises and all their data to a list and return it
    exerciseData = {}


    s = select(exercisesTable.join(userExercisesTable)).where(exercisesTable.c.id.in_(localExercises))
    for row in engine.execute(s):
        data = dict(row)
        if data['category'] not in str(exerciseData):
            exerciseData[data['category']] = []
            exerciseData[data['category']].append(data)
        else:
            exerciseData[data['category']].append(data)
        
    return exerciseData

def getVolumePoints(userId):
    vp = 100
    return vp
