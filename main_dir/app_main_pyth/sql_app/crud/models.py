import json
from lib2to3.pgen2.token import BACKQUOTE
from typing import List, Optional
from pydantic import BaseModel

class personalExercise(BaseModel):

    id: int
    max: int
    ranked_choice: int
    favorite: bool
    active: bool

class exerciseList(BaseModel):
    user_id: int
    exercise_list : List[personalExercise]

class settings(BaseModel):

    user_id: int
    goal: str
    split: int
    preffered_days: str
    cardio:bool

class goalsListSplitsList(BaseModel):
    goalsList : List[str]
    splitsList :List[str]

    