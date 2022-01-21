

import random

from readDb import getExerciseData, getVolumePoints


def generateWorkout(userId:int):
    
    exerciseData = getExerciseData(userId)
    volumePoints = getVolumePoints(userId)

    exerciseSetsReps = []
    catTrack = 0

    recursiveAddExercise(volumePoints,exerciseData,catTrack)


    return exerciseData


def recursiveAddExercise(points, exerciseData, usedCategoryTracker):
    if points >= 0:
        category  = list(exerciseData)[usedCategoryTracker]
        usedCategoryTracker += 1

        if usedCategoryTracker >= len(list(exerciseData)):
            usedCategoryTracker = 0

        print(category)

        exercise = exerciseData[category]
        print(type(exercise))

        points -= 10
        recursiveAddExercise(points,exerciseData, usedCategoryTracker)
    else:
        return