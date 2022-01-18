from msilib.schema import Class
from fastapi import FastAPI
import uvicorn
from typing import List
import requests

####USE BELOW COMMAND TO START####
#uvicorn main:app --port 5000 --reload

app = FastAPI()

class ScheduleData():

    user_id: int
    days_per_week: int
    preffered_days: str
    sub_splits: List[int]



@app.post("/schedule")
def send_user_exercise_preferences(scheduleData:List):

    print(scheduleData)
    return scheduleData

x = requests.get('http://127.0.0.1:8000/scheduledata')

print(x._content)