import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("antei-retail-project-demo-firebase-adminsdk-2x8oe-03a4dff15b.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://antei-retail-project-demo-default-rtdb.asia-southeast1.firebasedatabase.app"  # Замените на ваш URL
})
