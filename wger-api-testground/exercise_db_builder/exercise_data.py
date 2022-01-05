from dataclasses import dataclass
import json

@dataclass
class Exercise():


    name: str
    category: str
    description: str
    regularity_factor: int
    fatigue_factor: int
    parent_variation_id: int

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

""" @dataclass
class Exercise():

#this data class won't be used

    app_id: int    
    regularity: int

    wg_id: int
    name: str
    category: str
    description: str

    muscles: list
    variation_fam_members: list


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
 """



