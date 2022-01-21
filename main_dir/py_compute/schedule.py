from pydantic import BaseModel
from typing import List
from datetime import date, datetime, timedelta
from calendar import monthrange 

class ScheduleData(BaseModel):

    user_id: int
    days_per_week: int
    preffered_days: str
    sub_splits: List[int]

def build_schedule(scheduleData : ScheduleData):#scheduleData : ScheduleData

    now = datetime.now()
    daysInMonth =  monthrange(now.year, now.month)[1]
    
    currentDay = date.today().day
    
    firstOfMonth = date.today() + timedelta(days = -(currentDay-1))
    firstWeekDay = firstOfMonth.isoweekday()
    prefferedDays = scheduleData.preffered_days

    scheduleObj = prefferedDays[firstWeekDay-1:]
    
    scheduleObj += prefferedDays*5
    
    fullPrefferedDays = scheduleObj[:daysInMonth]
    
    subSplits = scheduleData.sub_splits

    splitSchedule = ""
    listIndex = 1 
    for x in fullPrefferedDays:
        if x == "0":
            splitSchedule += "0"
        if x == "1":
            splitSchedule += str(subSplits[listIndex])
            listIndex += 1
            if listIndex == len(subSplits):
                listIndex = 1
    
    return(splitSchedule)