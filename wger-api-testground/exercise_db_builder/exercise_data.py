from dataclasses import dataclass
import json

@dataclass
class Exercise():

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




