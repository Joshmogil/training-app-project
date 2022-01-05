from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import SessionLocal, engine

from .authorization.authschemas import AuthDetails

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

    return crud.create_user(db, user_credentials)

@app.post("/login")
def login(user_credentials: AuthDetails, db: Session = Depends(get_db)):

    return crud.login(db, user_credentials)





