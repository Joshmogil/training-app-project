from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware


from sql_app.crud.models import exerciseList, settings

from sql_app.crud import user_crud
from sql_app.crud import app_crud

from .database import SessionLocal

from .authorization.authschemas import AuthDetails, RegisterDetails

from .workoutBuilder.schedule_compute import fetch_schedule

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
    fetch_schedule(db,1)   

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


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

    return app_crud.update_user_settings(db, newSettings)


