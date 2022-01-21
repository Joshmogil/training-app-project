import json
from typing import List, Optional
from pydantic import BaseModel
import requests
from sqlalchemy import update
from sql_app.database import SessionLocal, user_schedule

from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from ..database import settings, splits_sub_splits

class ScheduleData(BaseModel):

    user_id: Optional[int]
    days_per_week: Optional[int]
    preffered_days: Optional[str]
    sub_splits: Optional[List[int]]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
            
def send_single_schedule_data(db:Session,user_id):

    s = select(settings.c).where(user_id==settings.c.user_id)
    sd = ScheduleData()
    for row in db.execute(s):
        
        row = dict(row)
        sd.user_id = row["user_id"]
        sd.days_per_week = row["days_per_week"]
        sd.preffered_days = row["preffered_days"]
        sd.sub_splits = [0]

        s = select(splits_sub_splits.c.sub_splits).where(row["split"] == splits_sub_splits.c.split_id)
        for row in db.execute(s):
            row = dict(row)
            sd.sub_splits.append(row["sub_splits"])
        
    return sd


def fetch_schedule(db:SessionLocal,user_id):
    scheduleData = send_single_schedule_data(db,user_id)

    r = requests.post('http://127.0.0.1:5000/schedule',data = scheduleData.toJSON())

    schedule = str(r.content)[3:][:-2]

    ins = user_schedule.insert().values(user_id = user_id, schedule = schedule)        
    result = db.execute(ins)     
        
    db.commit()

def update_schedule(db:SessionLocal,user_id):
    scheduleData = send_single_schedule_data(db,user_id)

    r = requests.post('http://127.0.0.1:5000/schedule',data = scheduleData.toJSON())

    schedule = str(r.content)[3:][:-2]
       
    ins = update(user_schedule).where(user_schedule.c.user_id == user_id).values(user_id = user_id, schedule = schedule)     
    result = db.execute(ins)     
        
    db.commit() 

