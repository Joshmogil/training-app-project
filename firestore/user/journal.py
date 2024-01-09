
from google.cloud import firestore
from firestore_utils import FirestoreDocument, use_local_firestore

COLLECTION_KEY: str ="user_journals"

class UserJournal(FirestoreDocument):
    def __init__(
            self,
            firestore_client: firestore.Client,
            user_id: str
            ):
        super().__init__(firestore_client, user_id=user_id, collection_key=COLLECTION_KEY)
    
    



if __name__ == "__main__":
    use_local_firestore()
    
    new_journal = UserJournal(
                              firestore_client=firestore.Client(project="my-project-id"),
                              user_id="jmogil123"
                              )



    doc_ref = db.collection("users").document("alovelace")
    doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})

    doc_ref = db.collection("users").document("aturing")
    doc_ref.set({"first": "Alan", "middle": "Mathison", "last": "Turing", "born": 1912})

    users_ref = db.collection("users")
    docs = users_ref.stream()

    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")