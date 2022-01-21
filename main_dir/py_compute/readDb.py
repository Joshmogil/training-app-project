from datetime import date
from inspect import _void
from typing import Match
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
settingsTable = metadata.tables['settings']

def getExerciseData(userId):
    
    #get current day in schedule (sub split id)
    subSplitDay = 0
    i = 0
    while subSplitDay == 0 and i<7: #hard logic, if the user does not have a workout planned for today, it will try to find the next workout in the schedule
        s = select(schedulesTable.c.schedule).where(schedulesTable.c.user_id == userId)
        schedule = ""
        for row in engine.execute(s):
            row = dict(row)
            schedule = row['schedule']
    
           
        subSplitDay = schedule[date.today().day+i]
        i += 1
        
    if subSplitDay == 0: #edge case guard
        subSplitDay ==5
    #get exercises by current subsplit
    s = select(subSplitsExercisesTable.c.exercises).where(subSplitsExercisesTable.c.sub_splits == subSplitDay)
    
    localExercises = set()

    for row in engine.execute(s):
        row = dict(row)
        localExercises.add(row["exercises"])

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



def getVolume(userId, exercise): #this is a junk way of doing this, the better way is to use a dependent schedule between volume and intensity
    setsReps = [3,10]

    s = select(settingsTable.c.goal).where(settingsTable.c.user_id == userId)
    
    case = None
    for row in engine.execute(s):
        settings = dict(row)    
        case = settings['goal']
        

    if case == "General Health":
        setsReps = [3,12]

        if exercise['fatigue_factor'] >= 25:
            setsReps = [3,8]

        if exercise['fatigue_factor'] > 30:
            setsReps = [3,6]

    if case == "Strength":
        setsReps = [3,10]

        if exercise['fatigue_factor'] >= 25:
            setsReps = [5,5]

        if exercise['fatigue_factor'] > 30:
            setsReps = [4,5]

    return setsReps

def getExercisePoints(userId):
    ep = 100

    s = select(settingsTable.c.goal).where(settingsTable.c.user_id == userId)
    
    case = None
    for row in engine.execute(s):
        settings = dict(row)    
        case = settings['goal']
        

    if case == "General Health":
        ep = 100


    if case == "Strength":
        ep = 75

    return ep

def getIntensityPoints(userId):
    vp = 100
    return vp