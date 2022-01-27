from fastapi import FastAPI

from schedule import ScheduleData, build_schedule
from workout import generateMonthOfWorkouts, generateMonthOfWorkouts

####USE BELOW COMMAND TO START####
#uvicorn appmain:app --port 5000 --reload

app = FastAPI()

@app.post("/schedule")
def schedule(scheduleData:ScheduleData):

    return build_schedule(scheduleData)

@app.get("/workout")
def workout(userId:int):
    workout = generateMonthOfWorkouts(userId)
    return workout


