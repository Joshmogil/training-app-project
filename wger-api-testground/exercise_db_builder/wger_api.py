import json
import requests
import re

import exercise_data
from exercise_data import Exercise

import json

base_url = "https://wger.de/api/v2/"
#https://wger.de/api/v2/exerciseiinfo/<id>/
response = requests.get(
    "https://wger.de/api/v2/exerciseinfo/?language=2&limit=400&offset=20",
     headers={'Authorization': 'Token adcb0fdccbcb7a4dac294291bfc2b84e468d0cab'},

)

exercise_results = json.loads(response.text)["results"]

listOfExerciseDataObj = []
listOfAllMuscles= []

entryNum = 0 

for x in exercise_results:

    app_id = entryNum
    wg_id = x["id"]
    name = x["name"]
    category = x["category"]["name"]   
    desc= x["description"]
    cleanedDesc = re.sub(re.compile('\n'), '', re.sub(re.compile('<.*?>'), '', desc))
    muscles = []

    for z in x["muscles"]: 
        muscles.append(z["name"])
        if listOfAllMuscles.count(z["name"])==0:
            listOfAllMuscles.append(z["name"])
        
    for z in x["muscles_secondary"]:              
        muscles.append(z["name"])
        if listOfAllMuscles.count(z["name"])==0:
            listOfAllMuscles.append(z["name"])
        
    entryNum += 1
    print(entryNum)
    print(name)

    var_family_mems = x["variations"]
    
    exerciseToAdd = exercise_data.Exercise(app_id, 0, wg_id,name,category,cleanedDesc,muscles,var_family_mems)

    listOfExerciseDataObj.append(exerciseToAdd)


for x in listOfExerciseDataObj:
    with open("sample.json", "a") as outfile:
        outfile.write(x.toJSON())






