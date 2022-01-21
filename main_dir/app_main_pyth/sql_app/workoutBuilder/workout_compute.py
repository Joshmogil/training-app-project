

import json
from typing import List, Optional
from pydantic import BaseModel


class WorkoutData(BaseModel):

    user_id: Optional[int]
    schedule: Optional[str]
    preffered_days: Optional[str]
    sub_splits: Optional[List[int]]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)