from pydantic import BaseModel
from typing import List
from datetime import date, datetime, timedelta
from calendar import monthrange 

class ScheduleData(BaseModel):

    user_id: int
    cardio: bool
    preffered_days: str
    sub_splits: List[int]

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
    for x in range(28):
        day = day0 + timedelta(days=i)
        if day.isoweekday() not in workoutDays:
            splitSchedule += "|"+str(day)+":0"
        if day.isoweekday() in workoutDays:
            splitSchedule += "|"+str(day)+":" + str(subSplits[listIndex])
            listIndex += 1
            if listIndex == len(subSplits):
                listIndex = 1
        i +=1

        if x == 27:
            splitSchedule += "|"
    
    return(splitSchedule)