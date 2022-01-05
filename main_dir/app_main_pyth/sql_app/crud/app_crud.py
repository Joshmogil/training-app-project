from sqlalchemy.orm import Session
from sqlalchemy.sql import insert, select

from fastapi import HTTPException

from sql_app.crud.models import exerciseList

from ..database import engine, users, settings, user_exercises

conn = engine.connect()

def send_user_exercise_preference(db: Session, exerciseList: exerciseList):

    print(exerciseList.user_id)
    print(exerciseList.exercise_list[0])
    
    user_id = exerciseList.user_id

    for x in exerciseList.exercise_list:
        print(type(x))
        
        id= x.id
        max = x.max
        rc = x.ranked_choice
        fav = x.favorite
        active = x.active

        ins = user_exercises.insert().values(user_id = user_id, exercises_id = id, max = max, ranked_choice = rc, favorite =fav, active =active)        
        result = db.execute(ins)     
        
    db.commit()
    