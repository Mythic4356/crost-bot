import firebase
from firebase import firebase   
import json
import os
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("../crost-secret/db.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://crost-a9e0e-default-rtdb.europe-west1.firebasedatabase.app/'})

def save(path : str,value):
    try:
        ref=db.reference(path)
        ref.set(value)
        print(f"Data at '{path}' has been set to value: '{value}'")
        return True
    except:
        print(f"Unable to save data at '{path}' with value: '{value}'")
        return False

def load(path: str):
    try:
        ref=db.reference(path)
        return ref.get()
    except:
        print(f"Unable to load data at path '{path}'")

save('quaso/cat',"CROISSANTS")