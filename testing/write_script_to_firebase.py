import json
import firebase_admin
from firebase_admin import credentials, firestore

# Path to your service account key file
SERVICE_ACCOUNT_PATH = "./product-manager-devpost-firebase-adminsdk-fbsvc-6b860d1bfc.json"
JSON_DATA_PATH = "./firestore_agent_ai_project.json"

# Initialize Firestore DB
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

# === HELPER FUNCTION TO DELETE COLLECTIONS ===
def delete_collection(coll_ref):
    docs = coll_ref.stream()
    for doc in docs:
        print(f"Deleting {coll_ref.id}/{doc.id}")
        doc.reference.delete()

# === DELETE EXISTING DATA ===
delete_collection(db.collection("team_members"))
delete_collection(db.collection("tasks"))
delete_collection(db.collection("calendar"))

# Delete single document
project_info_ref = db.collection("project").document("info")
if project_info_ref.get().exists:
    print("Deleting project/info")
    project_info_ref.delete()

# === LOAD JSON DATA ===
with open(JSON_DATA_PATH, "r") as f:
    data = json.load(f)

# === RE-ADD DATA ===

# Add team members
for uid, member in data["team_members"].items():
    db.collection("team_members").document(uid).set(member)

# Add project info
db.collection("project").document("info").set(data["project_info"])

# Add tasks
for status, items in data["tasks"].items():
    db.collection("tasks").document(status).set({"items": items})

# Add calendar events
for user_id, events in data["calendar"].items():
    db.collection("calendar").document(user_id).set({"events": events})

print("Firestore reset and repopulated successfully.")