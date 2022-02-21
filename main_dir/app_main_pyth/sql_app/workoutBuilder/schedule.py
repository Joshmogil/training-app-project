from typing import List, Optional
from datetime import date, datetime, timedelta
from calendar import monthrange

from sqlalchemy import update 
from sql_app.database import SessionLocal, user_schedule
from sqlalchemy.sql import select
from ..database import settings, splits_sub_splits


class ScheduleData():

    user_id: Optional[int]
    cardio: Optional[bool]
    preffered_days: Optional[str]
    sub_splits: Optional[List[int]]

def build_schedule(scheduleData : ScheduleData):#scheduleData : ScheduleData

    subSplits = scheduleData.sub_splits 
    prefferedDays = scheduleData.preffered_days

    workoutDays = set({})

    i = 0
    for x in prefferedDays:
        
        if i == 0 and x == str(1):
            workoutDays.add(1)
        if i == 1 and x == str(1):
            workoutDays.add(2)
        if i == 2 and x == str(1):
            workoutDays.add(3)
        if i == 3 and x == str(1):
            workoutDays.add(4)
        if i == 4 and x == str(1):
            workoutDays.add(5)
        if i == 5 and x == str(1):
            workoutDays.add(6)
        if i == 6 and x == str(1):
            workoutDays.add(7)
        
        i+=1      

    day0 = date.today()
    
    splitSchedule = ""
    listIndex = 0
    i = 0 
    for x in range(57):
        day = day0 + timedelta(days=i)
        if day.isoweekday() not in workoutDays:
            splitSchedule += "|"+str(day)+":0"
        if day.isoweekday() in workoutDays:
            splitSchedule += "|"+str(day)+":" + str(subSplits[listIndex])
            listIndex += 1
            if listIndex == len(subSplits):
                listIndex = 1
        i +=1

        if x == 56:
            splitSchedule += "|"
    
    return(splitSchedule)

def grab_single_schedule_data(db:SessionLocal,user_id):

    s = select(settings.c).where(user_id==settings.c.user_id)
    sd = ScheduleData()
    for row in db.execute(s):
        
        row = dict(row)
        sd.user_id = row["user_id"]
        sd.cardio = row["cardio"]
        sd.preffered_days = row["preffered_days"]
        sd.sub_splits = [0]

        s = select(splits_sub_splits.c.sub_splits).where(row["split"] == splits_sub_splits.c.split_id)
        for row in db.execute(s):
            row = dict(row)
            sd.sub_splits.append(row["sub_splits"])
        
    return sd

def create_schedule(db:SessionLocal,user_id):
    scheduleData = grab_single_schedule_data(db,user_id)

    schedule = build_schedule(scheduleData)

    ins = user_schedule.insert().values(user_id = user_id, schedule = schedule)        
    result = db.execute(ins)     
        
    db.commit()

def update_schedule(db:SessionLocal,user_id):
    scheduleData = grab_single_schedule_data(db,user_id)

    schedule = build_schedule(scheduleData)
       
    ins = update(user_schedule).where(user_schedule.c.user_id == user_id).values(user_id = user_id, schedule = schedule)     
    result = db.execute(ins)     
        
    db.commit() 