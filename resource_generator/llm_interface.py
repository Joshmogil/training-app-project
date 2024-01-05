

"""
Can you create a few json objects that fit the following pydantic schema: class FooBar(BaseModel):
    count: int
    size: Union[float, None] = None


class Gender(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'
    not_given = 'not_given'


class MainModel(BaseModel):
    
    This is the description of the main model
    

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
"""