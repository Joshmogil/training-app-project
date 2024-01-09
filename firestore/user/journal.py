
from google.cloud import firestore
from firestore_utils import FirestoreDocument, use_local_firestore

COLLECTION_KEY: str ="user_journals"



from enum import Enum
from typing import Union
from typing_extensions import Annotated
import pydantic
from pydantic.config import ConfigDict
from pydantic import BaseModel, Field

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


class UserJournal(FirestoreDocument):
    def __init__(
            self,
            firestore_client: firestore.Client,
            user_id: str
            ):
        super().__init__(
            firestore_client=firestore_client,
            user_id=user_id,
            collection_key=COLLECTION_KEY,
            pydantic_model=MainModel
            )
        
    
    



if __name__ == "__main__":
    use_local_firestore()
    
    new_journal = UserJournal(
        firestore_client=firestore.Client(project="my-project-id"),
        user_id="jmogil123"
        )
    
    d0 ={
        "model_config": {"title": "Main"},
        "foo_bar": {"count": 10, "size": 5.5},
        "gender": "male",
        "snap": 35
    }

    

    new_journal.init_data_model(data_model=MainModel(**d0))
    journal_data: MainModel = new_journal.get_data_model()
    print(journal_data)

    journal_data.model_config["title"] ="Two Brothas"
    new_journal.commit_model(journal_data)
    journal_data: MainModel = new_journal.get_data_model()
    print(journal_data)


    

    #for doc in docs:
    #    print(f"{doc.id} => {doc.to_dict()}")