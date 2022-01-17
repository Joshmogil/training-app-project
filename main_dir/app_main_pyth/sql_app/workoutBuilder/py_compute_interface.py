import requests
from sql_app.crud import app_crud

def go_test():
    r = requests.get('http://127.0.0.1:10000/').content
    print(r)


def send_schedule_data():
    scheduleData = app_crud.read_user_settings()
    r = requests.post('http://127.0.0.1:5000/schedule', data=scheduleData)