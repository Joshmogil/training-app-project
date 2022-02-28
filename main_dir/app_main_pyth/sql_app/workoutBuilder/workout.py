from decimal import Decimal
from email.mime import base
import math
import random
import sched
from typing import Optional
from webbrowser import get

from sqlalchemy import select, true
from sql_app.crud.user_crud import get_user_data, get_user_goals, get_user_misc, get_user_period_info
from sql_app.database import SessionLocal,sub_splits_exercises,user_exercises, exercises,goals_exercises, goals, splits_sub_splits, user_schedule, sub_splits_muscle_groups, muscle_groups, muscles_exercises

class ExerciseData():

    id: Optional[int]
    name: Optional[str]
    category: Optional[str]
    regularity_factor: Optional[int]
    fatigue_factor:Optional[int]
    description: Optional[str]
    max:Optional[int]
    ranked_choice:Optional[int]
    favorite:Optional[bool]
    active:Optional[bool]
    core: Optional[bool]

def generateMonthOfWorkouts(db:SessionLocal, userId:int):

    userData = get_user_data(db,userId)
    

    populateScheduleWithExercises(db,userData)

    #getSchedule    
    #scheduleExercises(userId) -> returns list dates(workouts) with associated exercises
        #getExercisesBySubsplit(sub split id) -Run for each sub split type in the user's schedule
            #
            #>sub_splits_exercises sort #1
            #>select from exercises off of that set
            #->user_exercises sort #2 -> add additional info from user_exercises to each exercise
            #-->goals_exercises sort #3 -> add additional info from goals_exercises to each exercise
            # List[[exercise information],] = list of exercises matching the day's sub_split, the user's exercise preferences, the user's goal (List of lists)
            # Case misc.variation_pref = low : core + 1 addit exercise, medium + 2, high + 4
            # return list of exercise info
        #divyVolumeUp
            #period is a month (28 days)
            #volume = ideal sets for each muscle group times 4 (28 days = 4 weeks)
            #count up sub splits occurences over period
            #count up muscle_groups (quantity) associated with sub splits
            #->divide monthly ideal sets (volume) by muscle_groups quantity = average sets per muscle group for each workout that month
            #if sub splits have multiple muscle_groups, they get a fractional distribution of the average sets per muscle group for each workout?
            
    #then
    #getExercisesIntensitySetsReps(ExercisesByDay) -> returns the same list but with sets reps and intensity for each exercise
    #then
    #mutateExercisesOnWeeklyBasis(ExercisesWithIntensitysetsreps) -> returns same list but mutates from week to week based on current period
    #then return final product: list of dates (workouts) with associated lists of: exercises, intensity, set,reps ; muatated on a weekly basis based on current period
    
    
    return 0


def populateScheduleWithExercises(db:SessionLocal,userData):

    
    fullySortedExercises = exerciseSortBeforePopulate(db,userData)
    setsPerMuscleGroup = averageVolumePerMuscleGroup(db,userData)
    scheduleAsList = getScheduleAsList(db,userData)

    
    """ print(fullySortedExercises)
    print()
    print(setsPerMuscleGroup)
    print()
    print(scheduleAsList) """

    #workout is a dict with (date, sub_day) as key, list of tuples (exercise id, sets, reps) as value
    monthOfWorkouts = {}

    goals = get_user_goals(db, userData["goal"])
    period_info = get_user_period_info(db,userData["user_id"])
    user_misc = get_user_misc(db, userData["user_id"])

    dayToDayVarCounterDict = dict()
    dayToDayVar = 0
    for x in scheduleAsList:

        print("Begin new day")

        if len(x)<12:
            break
        date = x[1:11]
        day = int(x[12])
        monthOfWorkouts[(date,day)] = "None yet"
        

        ## HACKY
        setsAlot = 2
        
        s = select(sub_splits_muscle_groups.c.muscle_groups).where(sub_splits_muscle_groups.c.sub_splits ==day)

        for row in db.execute(s):
            
            row = dict(row)
            muscleGroup = row["muscle_groups"]
        #get exercises
        #get sets
            sets = setsPerMuscleGroup[muscleGroup]
            #print("sets:",sets,"sub_split",day,"muscle group:",muscleGroup)

            exercisesInDax = list(fullySortedExercises[(day,muscleGroup)]) 
            exercises = []
            
            exercisesRange = 0

            
            if user_misc["str_level"] == "Novice" or user_misc["str_level"] == "Intermediate":
                setsAlot = 3

                setsIndex = sets

                while setsIndex > 1:
                    setsIndex -= setsAlot
                    exercisesRange += 1

            if user_misc["str_level"] == "Advanced":
                setsAlot = 4

                setsIndex = sets

                while setsIndex > 1:
                    setsIndex -= setsAlot
                    exercisesRange += 1

            if user_misc["variation_pref"] == "High":
                if muscleGroup not in dayToDayVarCounterDict:
                    dayToDayVarCounterDict[muscleGroup] = 0
                else:
                    if dayToDayVarCounterDict[muscleGroup] + exercisesRange>= len(exercisesInDax):
                        dayToDayVarCounterDict[muscleGroup] = 0                       
                    else:
                        dayToDayVarCounterDict[muscleGroup] +=1
                dayToDayVar = dayToDayVarCounterDict[muscleGroup]
                #print(dayToDayVar)
                for j in range(dayToDayVar,exercisesRange+dayToDayVar):
                    try:
                        exercises.append(fullySortedExercises[(day,muscleGroup)][exercisesInDax[j]])
                    except:
                        print("Indexing error hit")
                        dayToDayVarCounterDict[day] = 0

            if user_misc["variation_pref"] == "Medium":
                
                #print(dayToDayVar)
                for j in range(exercisesRange):
                    try:
                        exercises.append(fullySortedExercises[(day,muscleGroup)][exercisesInDax[j]])
                    except:
                        print("Indexing error hit")
                        dayToDayVarCounterDict[day] = 0

            if user_misc["variation_pref"] == "Low":
                
                #print(dayToDayVar)
                for j in range(math.ceil(exercisesRange/2)):
                    try:
                        exercises.append(fullySortedExercises[(day,muscleGroup)][exercisesInDax[j]])
                    except:
                        print("Indexing error hit")
                        dayToDayVarCounterDict[day] = 0



            baseReps = goals["base_reps"]
            repsMutation = period_info["reps_mutation"]
            newBaseReps = baseReps + repsMutation
            
            #print(newBaseReps)
            baseIntensity = goals["base_intensity"]
            intensityMutation = period_info["intensity_mutation"]
            newIntensity = baseIntensity+intensityMutation
            #print(newIntensity)

            for jk in exercises:
                print(f"{jk.name} | Sets x {probabilistic_round(sets/exercisesRange)} | Reps x {newBaseReps + ff(jk.fatigue_factor)[0]} | Weight x {myround(jk.max * (Decimal(newIntensity)+Decimal(ff(jk.fatigue_factor)[1])))} |")


        print()


        print("End workout day")
        print()
    print(dayToDayVarCounterDict)

    print(monthOfWorkouts)


def getPeriodMutations(db:SessionLocal,userData):

    return 0

def averageVolumePerMuscleGroup(db:SessionLocal,userData):
    
    schedule = getScheduleAsList(db,userData)
    muscleGroupCounter = getMuscleGroupCounter(schedule,db)

    misc = get_user_misc(db,userData["user_id"])


    s = select(muscle_groups.c)
    idealSetsByMuscle = {}
    for row in db.execute(s):
        row = dict(row)
        idealSetsByMuscle[row["id"]] = row[misc["str_level"]]*4
        

    averageVolumePerMuscle = {}

    for x in muscleGroupCounter:
        averageVolumePerMuscle[x] = idealSetsByMuscle[x]/muscleGroupCounter[x]

    return averageVolumePerMuscle
def getMuscleGroupCounter(schedule,db:SessionLocal):

    subDayCounter = {}

    for x in schedule:
        subDay = x[12:]
        if subDay == "":
            continue
        if int(subDay) not in subDayCounter:
            subDayCounter[int(subDay)] = 1
        else:
            subDayCounter[int(subDay)] += 1    

    s = select(sub_splits_muscle_groups.c)

    mGwithSdCount = []
    for row in db.execute(s):
        row = dict(row)
        mGwithSdCount.append((row["sub_splits"],row["muscle_groups"]))
   
    muscleGroupCounter = []
    for x in mGwithSdCount:
        if x[0] in subDayCounter:            
            muscleGroupCounter.append(x)

    muscleGroupDict = {}

    for x in subDayCounter:
        for i in muscleGroupCounter:
            if x == i[0]:
                if i[1] not in muscleGroupDict:
                    muscleGroupDict[i[1]] = subDayCounter[x]
                else:
                    muscleGroupDict[i[1]] += subDayCounter[x]

    return dict(sorted(muscleGroupDict.items()))
def getScheduleAsList(db:SessionLocal, userData):

    s = select(user_schedule.c.schedule).where(user_schedule.c.user_id==userData["user_id"])
    schedule = ""
    for row in db.execute(s):
        row = dict(row)
        schedule = row["schedule"]

    newSchedule = []
    while len(schedule)>0:
        
        begin = schedule.find("|")
        newSchedule.append(schedule[begin:13])
        schedule = schedule[13:]

    return newSchedule
def getExercisesBySubsplit(db:SessionLocal,subSplit:int,userData):

    exerciseDatas = {}

    set1 = set({})
    s = select(sub_splits_exercises.c).where(subSplit==sub_splits_exercises.c.sub_splits)
    for row in db.execute(s):
        row = dict(row)
        set1.add(int(row["exercises"]))

    s = select(exercises.c).where(exercises.c.id.in_(set1))
    for row in db.execute(s):
        row = dict(row)
        exercise = ExerciseData()
        exercise.id = row["id"]
        exercise.name =row["name"]
        exercise.category=row["category"]
        exercise.regularity_factor=row["regularity_factor"]
        exercise.fatigue_factor=row["fatigue_factor"]
        exercise.description=row["description"]
        exerciseDatas[exercise.id] = exercise

    set2 = set({})
    h = select(user_exercises.c).where(userData["user_id"] == user_exercises.c.user_id)
    
    for row in db.execute(h):
        row = dict(row)
        exerciseId = int(row["exercises_id"])
        
        if exerciseId in set1:
            set2.add(exerciseId)
            exercise = exerciseDatas[row["exercises_id"]]
            exercise.max = row["max"]
            exercise.ranked_choice = row["ranked_choice"]
            exercise.favorite = row["favorite"]
            exercise.active = row["active"]
            exerciseDatas[exerciseId] = exercise
            
    commonDict = {}
    for x in exerciseDatas:
        if x in set2:
            commonDict[x] = exerciseDatas[x]
    exerciseDatas = commonDict

    finalSet = set({})

    goalIndex = 1 # bad
    g = select(goals.c.id).where(userData["goal"] == goals.c.name)
    for row in db.execute(g):
        row = dict(row)
        goalIndex = row["id"]

    h = select(goals_exercises.c).where(goals_exercises.c.goals == goalIndex)
    
    for row in db.execute(h):
        row = dict(row)
        exerciseId = int(row["exercises"])
        
        if exerciseId in set2:
            finalSet.add(exerciseId)
            exercise = exerciseDatas[row["exercises"]]
            exercise.core = row["core"]
            exerciseDatas[exerciseId] = exercise

    commonDict = {}
    for x in exerciseDatas:
        if x in finalSet:
            commonDict[x] = exerciseDatas[x]
    exerciseDatas = commonDict

    

    return exerciseDatas
def exerciseDataBySubSplit(db:SessionLocal,userData):
    
    s = select(splits_sub_splits.c.sub_splits).where(splits_sub_splits.c.split_id == userData["split"])

    exerciseDataBySubSplit = {} #<Important
    for row in db.execute(s):
        row = dict(row)
        exerciseDataBySubSplit[row["sub_splits"]]= getExercisesBySubsplit(db,row["sub_splits"],userData)
    
    return exerciseDataBySubSplit

def globalFuncGrabExercises(db:SessionLocal,userData):

    #exercises sorted by sub split (have this)
    #-> sort by muscle group = dictionary with tuple (sub_split,muscle_group) as key and list of exercises as value
    #--> Sort those dictionary entries by 1. ranked_choice 2.core 3.favorite 4.active = same dictionary of lists but sorted
    # return

    exerciseDatas = exerciseDataBySubSplit(db,userData)

    s = select(muscles_exercises.c)
    musclesExercises = []
    for row in db.execute(s):
        row = dict(row)
        musclesExercises.append((row["muscles"],row["exercises"]))

    """ listOfExerciseData = []
    for x in exerciseDatas:
        for y in exerciseDatas[x]:
            listOfExerciseData.append(exerciseDatas[x][y])
    print(listOfExerciseData[0:1]) """

    musclesSplitsExercises = {}
    for y in exerciseDatas: #Crazy sort
        for x in exerciseDatas[y]:
            for z in musclesExercises:
                if (y,z[0]) not in musclesSplitsExercises and x==z[1]:
                    musclesSplitsExercises[y,z[0]] = [exerciseDatas[y][x]]
                elif x==z[1]:
                    musclesSplitsExercises[y,z[0]].append(exerciseDatas[y][x])
    

    return musclesSplitsExercises

def exerciseSortBeforePopulate(db:SessionLocal,userData):

    #--> Sort those dictionary entries by 1. ranked_choice 2.core 3.favorite 4.active = same dictionary of lists but sorted
    exercisesToSort = globalFuncGrabExercises(db,userData)

    
    finalSortDict = {}
    for x in exercisesToSort:
        sortThis = []
        unSortedDict = {}
        for y in exercisesToSort[x]:
            sortThis.append((y.id,y.ranked_choice,y.favorite,y.core,y.active))
            unSortedDict[y.id] = y
        sortThis = Sort_Tuple(sortThis,1)
        sortThis = Sort_Tuple(sortThis,2)
        sortThis = Sort_Tuple(sortThis,3)
        sortThis = Sort_Tuple(sortThis,4)
        sortThis.reverse()     
        matchList = []
        for j in sortThis:            
            matchList.append(j[0])
        sortedDict = {}
        for k in matchList:
            sortedDict[k] = unSortedDict[k]
        finalSortDict[x] =sortedDict
        
    return finalSortDict

def finalSelectExercises():
    return "hi"

def Sort_Tuple(tup,pos): 
  
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of 
    # sublist lambda has been used 
    tup.sort(key = lambda x: x[pos]) 
    return tup 

def probabilistic_round(x):
    return int(math.floor(x + random.random()))

def ff(x):
    ff = {1:(5,-0.10),2:(3,-0.05),3:(0,0),4:(-1,.025)}
    return ff[x]

def myround(x, base=5):
    return base * round(x/base)