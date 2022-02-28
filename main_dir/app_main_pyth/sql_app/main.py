from tkinter import Misc
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware



from sql_app.crud.models import exerciseList, settings, misc

from sql_app.crud import user_crud
from sql_app.crud import app_crud
from sql_app.crud import dynamicDB_crud
from sql_app.workoutBuilder.schedule import create_schedule, update_schedule
from sql_app.workoutBuilder.workout import generateMonthOfWorkouts

from .database import SessionLocal

from .authorization.authschemas import AuthDetails, RegisterDetails



####USE BELOW COMMAND TO START####
#uvicorn sql_app.main:app --reload


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Registration and login

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.get("/cors")
def cors_test(db: Session = Depends(get_db)):
    generateMonthOfWorkouts(db,1) 

@app.post("/register")
def create_user(reg_details: RegisterDetails, db: Session = Depends(get_db)):

    return user_crud.create_user(db, reg_details)

@app.post("/login")
def login(user_credentials: AuthDetails, db: Session = Depends(get_db)):

    JWT = user_crud.login(db, user_credentials)

    return JWT

#app functions
@app.post("/exercises")
def send_user_exercise_preferences(exerciseList: exerciseList, db: Session = Depends(get_db)):

    return app_crud.send_user_exercise_preference(db, exerciseList)

@app.post("/settings")
def update_user_settings(newSettings: settings, db: Session = Depends(get_db)):

    update_schedule(db,1)

    return app_crud.update_user_settings(db, newSettings)

@app.post("/misc")
def update_user_misc(userMisc: misc, db: Session = Depends(get_db)):

    return app_crud.update_user_misc(db, userMisc)


