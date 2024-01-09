import dataclasses
import os
from google.cloud import firestore
import pydantic


"""
    doc_ref = db.collection("users").document("alovelace")
    doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})

    doc_ref = db.collection("users").document("aturing")
    doc_ref.set({"first": "Alan", "middle": "Mathison", "last": "Turing", "born": 1912})

    users_ref = db.collection("users")
    docs = users_ref.stream()
"""


class FirestoreDocument:
    def __init__(
            self,
            firestore_client: firestore.Client,
            user_id: str,
            collection_key: str,
            pydantic_model: pydantic.BaseModel
            ):
        self.__db=firestore_client
        self.__collection=collection_key 
        self.__document_id=collection_key.lower() + "_" + user_id 
        self.__model=pydantic_model
        #self.__data: pydantic.BaseModel =None
        #self.__data= self.__load_document_into_model()
    
    def init_data_model(self, data_model: pydantic.BaseModel) -> bool:
        self.__commit_model_to_firestore(data_model)
        return True


    def commit_model(self, data_model: pydantic.BaseModel) -> bool:#, data_model: pydantic.BaseModel) -> bool:
        self.__commit_model_to_firestore(data_model)
        return True
        
    def get_data_model(self):
        data_model=self.__load_document_into_model()
        return data_model

    
    
    def __load_document_into_model(self) -> pydantic.BaseModel or None:
        """Loads json document from firestore into pydantic model."""
        try:
            doc_ref = self.__db.collection(self.__collection).document(self.__document_id).get()
            if doc_ref.exists:
                doc_data = doc_ref.to_dict()
                return self.__model(**doc_data)
            else:
                "Cannot load empty document."
        except:
            return None
        
    
    def __commit_model_to_firestore(self, data_model: pydantic.BaseModel):
        """Commits modified document to firestore db."""
        #print(data_model)
        doc_ref = self.__db.collection(self.__collection).document(self.__document_id)
        doc_ref.set(data_model.dict())
    



def use_local_firestore():
    FIRESTORE_EMULATOR_HOST='127.0.0.1:8083'
    os.environ['FIRESTORE_EMULATOR_HOST']=FIRESTORE_EMULATOR_HOST

