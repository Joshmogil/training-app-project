from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from .authorization.authschemas import AuthDetails
from .authorization.auth import AuthHandler

app = FastAPI()

auth_handler = AuthHandler()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Registration and login

@app.post("/register")
def create_user(user_credentials: AuthDetails):

    return crud.create_user(user_credentials)

@app.post("/login")
def login(user_credentials: AuthDetails):

    return crud.login(user_credentials)

""" @app.post("/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = crud.get_user_by_email(db, email=user.email) 
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth_handler.get_password_hash(user.password)
    
    return crud.create_user(db=db, user=user, hashedPassword= hashed_password)

@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = crud.get_user_by_email(db, email =user.email) 

    if (user is None) or (not auth_handler.verify_password(user.password, db_user.hashed_password)):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')

    token = auth_handler.encode_token(db_user.email)
    return {'token':token} """




""" @app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#Core functionality below
@app.post("/user/settings/")
def modify_settings_for_user(settings: schemas.SettingsCreate, db: Session = Depends(get_db)):
    
    return crud.modify_user_settings(db=db, settings=settings, user_id= settings.user_id)
 """