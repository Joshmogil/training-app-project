import json
from enum import Enum
from typing import Union

from typing_extensions import Annotated

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class FooBar(BaseModel):
    count: int
    size: Union[float, None] = None


class Gender(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'
    not_given = 'not_given'


class MainModel(BaseModel):
    """
    This is the description of the main model
    """

    model_config = ConfigDict(title='Main')

    foo_bar: FooBar
    gender: Annotated[Union[Gender, None], Field(alias='Gender')] = None
    snap: int = Field(
        42,
        title='The Snap',
        description='this is the value of snap',
        gt=30,
        lt=50,
    )


d0 ={
  "model_config": {"title": "Main"},
  "foo_bar": {"count": 10, "size": 5.5},
  "gender": "male",
  "snap": 35
}

d1 ={
  "model_config": {"title": "Main"},
  "foo_bar": {"count": 20},
  "gender": "female",
  "snap": 45
}

d2 = {
  "model_config": {"title": "Main"},
  "foo_bar": {"count": 15, "size": None},
  "Gender": "other",
  "snap": 40
}

d3 = {
  "model_config": {"title": "Main"},
  "foo_bar": {"count": 8, "size": 3.2},
  "Gender": "not_given",
  "snap": 32
}


res = [
    MainModel(**d0),
    MainModel(**d1),
    MainModel(**d2),
    MainModel(**d3)
]
print(res)
#print(json.dumps(MainModel.model_json_schema(), indent=2))