from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
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
    return db_user

def get_settings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Settings).offset(skip).limit(limit).all()

def modify_user_settings(db: Session, settings: schemas.SettingsCreate, userId:int):
    db_settings = models.Settings(**settings.dict(), user_id = userId)
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings