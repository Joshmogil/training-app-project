

import random

from readDb import getExerciseData, getExercisePoints, getIntensityPoints, getVolumePoints


def generateWorkout(userId:int):
    
    exerciseData = getExerciseData(userId)
    volumePoints = getVolumePoints(userId)
    exercisePoints = getExercisePoints(userId)
    intensityPoints = getIntensityPoints(userId)

    exercises = []
    catTrack = 0
    exercises = recursiveAddExercise(exercisePoints,exerciseData,catTrack,exercises)

    proofOfConcept = []
    for x in exercises:
        proofOfConcept.append([x['name'],int(volumePoints/len(exercises)),10])


    return proofOfConcept


def recursiveAddExercise(points, exerciseData, usedCategoryTracker, exercises):
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
    

    return sorted(exercises, key = lambda i: i['fatigue_factor'], reverse=True)