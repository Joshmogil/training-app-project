

import random

from readDb import getExerciseData, getExercisePoints, getVolume


def generateMonthOfWorkouts(userId:int):
    #getExercisesByDay(userId) -> returns list dates(workouts) with associated exercises
    #then
    #getExercisesIntensitySetsReps(ExercisesByDay) -> returns the same list but with sets reps and intensity for each exercise
    #then
    #mutateExercisesOnWeeklyBasis(ExercisesWithIntensitysetsreps) -> returns same list but mutates from week to week based on current period
    #then return final product: list of dates (workouts) with associated lists of: exercises, intensity, set,reps ; muatated on a weekly basis based on current period

    """ exerciseData = getExerciseData(userId)
    exercisePoints = getExercisePoints(userId)
    exercises = []
    catTrack = 0
    exercises = recursiveAddExercise(exercisePoints,exerciseData,catTrack,exercises)
    proofOfConcept = []
    for x in exercises:
        setsReps = getVolume(userId, x)
        proofOfConcept.append([x['name'],setsReps[0],setsReps[1]]) """
    
    return 0


""" def recursiveAddExercise(points, exerciseData, usedCategoryTracker, exercises):
    if points >= 0: #fatigue factors on a 30/25/20/15 scale
        category  = list(exerciseData)[usedCategoryTracker]
        usedCategoryTracker += 1
        if usedCategoryTracker >= len(list(exerciseData)):
            usedCategoryTracker = 0
        exercise = exerciseData[category][random.randrange(0,len(exerciseData[category])-1)]
        if exercise not in exercises:
            points -= exercise['fatigue_factor']
            exercises.append(exercise)  
        recursiveAddExercise(points,exerciseData, usedCategoryTracker, exercises)
    return sorted(exercises, key = lambda i: i['fatigue_factor'], reverse=True) """