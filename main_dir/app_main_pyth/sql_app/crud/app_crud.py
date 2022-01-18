import pickle
import sched
from sqlalchemy.orm import Session
from sqlalchemy.sql import insert, select, update

from fastapi import HTTPException

from sql_app.crud.models import ScheduleData, exerciseList

from ..database import engine, users, settings, user_exercises, splits_sub_splits

conn = engine.connect()

def send_user_exercise_preference(db: Session, exerciseList: exerciseList):
    
    user_id = exerciseList.user_id

    for x in exerciseList.exercise_list:
        
        
        id= x.id
        max = x.max
        rc = x.ranked_choice
        fav = x.favorite
        active = x.active

        ins = user_exercises.insert().values(user_id = user_id, exercises_id = id, max = max, ranked_choice = rc, favorite =fav, active =active)        
        result = db.execute(ins)     
        
    db.commit()

def update_user_settings(db:Session, newSettings: settings):

    user_id = newSettings.user_id
    goal = newSettings.goal
    split  = newSettings.split
    dpw = newSettings.days_per_week
    pd = newSettings.preffered_days

    stmt = update(settings).where(settings.c.user_id == newSettings.user_id).values(user_id = user_id ,goal = goal, split = split, days_per_week = dpw, preffered_days =pd)

    print(update(settings))

    result = db.execute(stmt)

    db.commit()

def send_schedule_data(db:Session):

    

    s = select(settings.c)
    scheduleData = []
    for row in db.execute(s):
        sd = ScheduleData()
        row = dict(row)
        sd.user_id = row["user_id"]
        sd.days_per_week = row["days_per_week"]
        sd.preffered_days = row["preffered_days"]
        sd.sub_splits = [0]

        s = select(splits_sub_splits.c.sub_splits).where(row["split"] == splits_sub_splits.c.split_id)
        for row in db.execute(s):
            row = dict(row)
            sd.sub_splits.append(row["sub_splits"])
        

        scheduleData.append(sd)


    return scheduleData
        

    