from sqlalchemy.orm import Session
from sqlalchemy.sql import insert, select

from fastapi import HTTPException

from sql_app.crud.models import exerciseList

from ..database import engine, users, settings

conn = engine.connect()

def send_user_exercise_preference(db: Session, exerciseList: exerciseList):

    print(exerciseList.user_id)
    print(exerciseList.exercise_list[0])
    
