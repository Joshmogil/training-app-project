
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, update

from sql_app.crud.models import exerciseList
from sql_app.workoutBuilder.schedule import update_schedule

from ..database import settings, user_exercises, splits_sub_splits, user_misc, periods



def send_user_exercise_preference(db: Session, exerciseList: exerciseList):
    
    user_id = exerciseList.user_id

    for x in exerciseList.exercise_list:
        
        
        id= x.id
        max = x.max
        rc = x.ranked_choice
        fav = x.favorite
        active = x.active

        ins = user_exercises.insert().values(user_id = user_id, exercises_id = id, max = max, ranked_choice = rc, favorite =fav, active =active)        
        result = db.execute(ins)     
        
    db.commit()

def update_user_settings(db:Session, newSettings: settings):

    user_id = newSettings.user_id
    goal = newSettings.goal
    split  = newSettings.split
    pd = newSettings.preffered_days
    cardio = newSettings.cardio
    
    stmt = update(settings).where(settings.c.user_id == newSettings.user_id).values(user_id = user_id ,goal = goal, split = split, preffered_days = pd, cardio = cardio)

    #print(update(settings))

    result = db.execute(stmt)

    db.commit()

    update_schedule(db, user_id)

def update_user_misc(db:Session, newMisc: user_misc):

    user_id = newMisc.user_id
    cp = newMisc.current_period
    vp  = newMisc.variation_pref
    sl = newMisc.str_level
    
    
    stmt = update(user_misc).where(user_misc.c.user_id == newMisc.user_id).values(user_id = user_id,current_period = cp, variation_pref = vp,str_level=sl)

    #print(stmt)
    result = db.execute(stmt)

    db.commit()

    update_schedule(db, user_id)


    