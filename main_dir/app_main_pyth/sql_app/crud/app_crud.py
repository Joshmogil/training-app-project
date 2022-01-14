from sqlalchemy.orm import Session
from sqlalchemy.sql import insert, select, update

from fastapi import HTTPException

from sql_app.crud.models import exerciseList

from ..database import engine, users, settings, user_exercises

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