import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("NEW_API_KEY")
FIREBASE_CREDENTIALS = "firebase-admin.json"
