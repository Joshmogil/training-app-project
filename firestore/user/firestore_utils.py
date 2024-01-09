import os
from google.cloud import firestore


class FirestoreDocument:
    def __init__(
            self,
            firestore_client: firestore.Client,
            user_id: str,
            collection_key: str
            ):
        self.db=firestore_client
        self.collection=collection_key 
        self.document_id = collection_key.to_lower() + "_" + user_id 
    
    def __load_document_into_model(self):
        """Loads json document from firestore into pydantic model."""
        pass


    def __dump_model_into_document(self):
        """Dumps pydantic model into json document."""
        pass

    
    def commit_document(self):
        """Commits modified document to firestore db."""
        pass



def use_local_firestore():
    FIRESTORE_EMULATOR_HOST='127.0.0.1:8083'
    os.environ['FIRESTORE_EMULATOR_HOST']=FIRESTORE_EMULATOR_HOST
