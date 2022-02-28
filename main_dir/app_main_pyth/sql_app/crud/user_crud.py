from sqlalchemy.orm import Session
from sqlalchemy.sql import insert, select

from fastapi import HTTPException
from sql_app.workoutBuilder.schedule import create_schedule

from ..database import engine, users, settings, user_misc, goals, periods

from ..authorization.authschemas import AuthDetails, RegisterDetails
from ..authorization.auth import AuthHandler

conn = engine.connect()
auth_handler = AuthHandler()


def create_user(db: Session, reg_details: RegisterDetails):

    if (reg_details.password != reg_details.confirmPassword):
        raise HTTPException(status_code=401, detail='Password and Confirm password must match')

    s = select(users.c.email).where(users.c.email==reg_details.email)
    trueIfEmailExists = False
    for row in db.execute(s):
        trueIfEmailExists = True
    
    if trueIfEmailExists is False:

        gen_hashed_password = auth_handler.get_password_hash(reg_details.password)

        ins = users.insert().values(email=reg_details.email,hashed_password=gen_hashed_password, is_active = True, needs_setup = True)        
        result = db.execute(ins)        
        newUserId = result.inserted_primary_key
        
        db.commit()

        userId = ""

        for x in str(newUserId):

            if x.isdigit():

                userId += x
        
        userId =int(userId)

        ins2 = insert(settings).values(user_id=userId, goal="Health", split = 3, preffered_days = "0101010", cardio = 1)

        result = db.execute(ins2)
        db.commit()

        ins = insert(user_misc).values(user_id=userId,current_period="Conditioning",variation_pref="Medium",str_level="Novice")

        result = db.execute(ins)
        db.commit()

        create_schedule(db, userId)
        
        return True
    
    return False

def login(db: Session, user_credentials: AuthDetails):

    db_user = get_user_by_email(db, user_credentials.email)

    if (db_user is None) or (not auth_handler.verify_password(user_credentials.password, db_user[2])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')

    user_response = dict(db_user)
    print(type(user_response))
    user_response.pop("hashed_password")
    print(user_response)

    token = auth_handler.encode_token(db_user[1])

    

    return {'token':token, 'user':user_response}    

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

def get_user_data(db: Session, userId: int):

    s = select(settings.c).where(settings.c.user_id == userId)

    for row in db.execute(s):
        return dict(row)

def get_user_misc(db: Session, userId: int):

    s = select(user_misc.c).where(user_misc.c.user_id == userId)

    for row in db.execute(s):
        return dict(row)

def get_user_goals(db: Session, goalName: int):

    s = select(goals.c).where(goals.c.name == goalName)

    for row in db.execute(s):
        return dict(row)

def get_user_period_info(db: Session, userId: int):

    s = select(user_misc.c).where(user_misc.c.user_id == userId)

    userPeriod = ""
    for row in db.execute(s):
        userPeriod = dict(row)["current_period"]

    #print(userPeriod)

    s = select(periods.c).where(periods.c.name == userPeriod)

    for row in db.execute(s):
        return dict(row)