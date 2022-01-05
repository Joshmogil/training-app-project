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