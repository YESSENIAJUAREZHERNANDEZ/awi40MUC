import pyrebase
import firebase_config as token
firebase = pyrebase.initialize_app(token.firebaseConfig)
db = firebase.database()

users = db.child("users").get()
print(users)

db.child("users").child("Morty").update({"name": "Mortiest Morty"})