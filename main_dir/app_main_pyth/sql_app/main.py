from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app.crud.models import exerciseList

from .crud import user_crud
from .crud import app_crud


from . import schemas
from .database import SessionLocal, engine

from .authorization.authschemas import AuthDetails


####USE BELOW COMMAND TO START####
#uvicorn sql_app.main:app --reload


app = FastAPI()

#Registration and login

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register")
def create_user(user_credentials: AuthDetails, db: Session = Depends(get_db)):

    return user_crud.create_user(db, user_credentials)

@app.post("/login")
def login(user_credentials: AuthDetails, db: Session = Depends(get_db)):

    return user_crud.login(db, user_credentials)

#app fucntions
@app.post("/test")
def send_user_exercise_preferences(exerciseList: exerciseList, db: Session = Depends(get_db)):

    return app_crud.send_user_exercise_preference(db, exerciseList)



