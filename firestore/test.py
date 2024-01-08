import os
from google.cloud import firestore

FIRESTORE_EMULATOR_HOST='127.0.0.1:8083'
os.environ['FIRESTORE_EMULATOR_HOST']=FIRESTORE_EMULATOR_HOST

db = firestore.Client(project="my-project-id")
doc_ref = db.collection("users").document("alovelace")
doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})

doc_ref = db.collection("users").document("aturing")
doc_ref.set({"first": "Alan", "middle": "Mathison", "last": "Turing", "born": 1912})

users_ref = db.collection("users")
docs = users_ref.stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")