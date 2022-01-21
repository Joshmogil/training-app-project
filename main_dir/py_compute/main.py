from msilib.schema import Class
from fastapi import FastAPI

import uvicorn
from typing import List
import requests

from schedule import ScheduleData, build_schedule

####USE BELOW COMMAND TO START####
#uvicorn main:app --port 5000 --reload

app = FastAPI()

@app.post("/schedule")
def schedule(scheduleData:ScheduleData):

    return build_schedule(scheduleData)

@app.post("/workout")
def workout():
    return
