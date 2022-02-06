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
subSplitsTable = metadata.tables['splits_sub_splits']
exercisesTable = metadata.tables['exercises']
settingsTable = metadata.tables['settings']

def getExerciseData(userId):
    
    s=select(settingsTable.c.split).where(userId == settingsTable.c.user_id)
    userSplit = 1
    for row in engine.execute(s):       
        userSplit = dict(row)["split"]
    
    userSubSplits = []
    s=select(subSplitsTable.c.sub_splits).where(userSplit == subSplitsTable.c.split_id)
    for row in engine.execute(s):       
        userSubSplits.append(dict(row)["sub_splits"])


    return userSubSplits



