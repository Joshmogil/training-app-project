from pydantic import BaseModel
from typing import List
from datetime import date, datetime
from calendar import monthrange 

class ScheduleData(BaseModel):

    user_id: int
    days_per_week: int
    preffered_days: str
    sub_splits: List[int]

def build_schedule(scheduleData : ScheduleData):

    now = datetime.now()
    daysInMonth =  monthrange(now.year, now.month)[1]
    
    currentDay = date.today().day
    currentWeekDay = date.today().isoweekday()
    
    prefferedDays = scheduleData.preffered_days

    periodBeginPd = prefferedDays[currentWeekDay:]
    fullPrefferedDays = periodBeginPd+prefferedDays*4
    fullPrefferedDays = fullPrefferedDays[:daysInMonth-currentDay+1]
    
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