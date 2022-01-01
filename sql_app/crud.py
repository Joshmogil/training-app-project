from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.functions import user
from sqlalchemy.sql import insert, select

from fastapi import HTTPException

from .database import engine, users, settings

from .authorization.authschemas import AuthDetails
from .authorization.auth import AuthHandler

conn = engine.connect()
auth_handler = AuthHandler()

def create_user(user_credentials: AuthDetails):

    if check_if_email_used(user_credentials.email) is False:

        gen_hashed_password = auth_handler.get_password_hash(user_credentials.password)

        ins = users.insert().values(email=user_credentials.email,hashed_password=gen_hashed_password, is_active = True)

        result = conn.execute(ins)

        return True
    
    return False

def login(user_credentials: AuthDetails):

    db_user = get_user_by_email(user_credentials.email)

    if (db_user is None) or (not auth_handler.verify_password(user_credentials.password, db_user[2])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')

    token = auth_handler.encode_token(db_user[1])
    return {'token':token}    

def check_if_email_used(email: str):

    s = select(users.c.email).where(users.c.email==email)
    
    trueIfEmailExists = False

    for row in conn.execute(s):
        trueIfEmailExists = True
        
    return trueIfEmailExists

def get_user_by_email(email: str):

    s = select(users).where(users.c.email==email)

    for row in conn.execute(s):
        return row

    
        

""" def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_password_hash_by_email(db: Session, email: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    return db_user.hashed_password


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate, hashedPassword):  
    db_user = models.User(email=user.email, hashed_password=hashedPassword)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user """



""" 
def get_settings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Settings).offset(skip).limit(limit).all()

def modify_user_settings(db: Session, settings: schemas.SettingsCreate, userId:int):
    db_settings = models.Settings(**settings.dict(), user_id = userId)
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings """