from dataclasses import dataclass

@dataclass
class Exercise():
    wg_id: int
    name: str
    category: str
    description: str

    muscles: list
    variation_fam_members: list


