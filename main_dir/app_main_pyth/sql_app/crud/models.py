from lib2to3.pgen2.token import BACKQUOTE
from typing import List
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
    days_per_week: int
    preffered_days: str