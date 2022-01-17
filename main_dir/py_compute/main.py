from msilib.schema import Class
from fastapi import FastAPI
import uvicorn
from typing import List

####USE BELOW COMMAND TO START####
#uvicorn main:app--5000 --reload

app = FastAPI()

class ScheduleData():

    user_id: int
    days_per_week: int
    preffered_days: str
    sub_splits: List[int]



@app.post("/exercises")
def send_user_exercise_preferences(scheduleData:List):

    print(scheduleData)
    return scheduleData