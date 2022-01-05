from sqlalchemy.orm import Session
from sqlalchemy.sql import insert, select

from fastapi import HTTPException

from ..database import engine, users, settings

from ..authorization.authschemas import AuthDetails
from ..authorization.auth import AuthHandler

conn = engine.connect()
auth_handler = AuthHandler()


def create_user(db: Session, user_credentials: AuthDetails):

    s = select(users.c.email).where(users.c.email==user_credentials.email)
    trueIfEmailExists = False
    for row in db.execute(s):
        trueIfEmailExists = True
    
    if trueIfEmailExists is False:

        gen_hashed_password = auth_handler.get_password_hash(user_credentials.password)

        ins = users.insert().values(email=user_credentials.email,hashed_password=gen_hashed_password, is_active = True)        
        result = db.execute(ins)        
        newUserId = result.inserted_primary_key
        
        db.commit()

        userId = ""

        for x in str(newUserId):

            if x.isdigit():

                userId += x

        ins2 = insert(settings).values(user_id=int(userId), goal="hello", split = "hello2", days_per_week=4, preffered_days = "0101010")
        
        print(ins2)

        result = db.execute(ins2)
        db.commit()
        
        return True
    
    return False

def login(db: Session, user_credentials: AuthDetails):

    db_user = get_user_by_email(db, user_credentials.email)

    if (db_user is None) or (not auth_handler.verify_password(user_credentials.password, db_user[2])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')

    token = auth_handler.encode_token(db_user[1])
    return {'token':token}    

def check_if_email_used(db: Session, email: str):

    s = select(users.c.email).where(users.c.email==email)
    
    trueIfEmailExists = False

    for row in db.execute(s):
        trueIfEmailExists = True
        
    return trueIfEmailExists

def get_user_by_email(db: Session, email: str):

    s = select(users).where(users.c.email==email)

    for row in db.execute(s):
        return row
