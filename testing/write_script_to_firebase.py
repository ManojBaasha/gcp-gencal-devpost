import json
import firebase_admin  # type: ignore
from firebase_admin import credentials, firestore  # type: ignore

# Paths
SERVICE_ACCOUNT_PATH = "./product-manager-devpost-firebase-adminsdk-fbsvc-6b860d1bfc.json"
JSON_DATA_PATH = "./firestore_agent_ai_project.json"

# Initialize Firestore
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

# === HELPER: Delete Collection ===
def delete_collection(coll_ref):
    docs = coll_ref.stream()
    for doc in docs:
        print(f"Deleting {coll_ref.id}/{doc.id}")
        doc.reference.delete()

# === DELETE EXISTING DATA ===
delete_collection(db.collection("team_members"))
delete_collection(db.collection("tasks"))
delete_collection(db.collection("calendar"))

project_ref = db.collection("project").document("info")
if project_ref.get().exists:
    print("Deleting project/info")
    project_ref.delete()

# === LOAD JSON DATA ===
with open(JSON_DATA_PATH, "r") as f:
    data = json.load(f)

# === ADD DATA BACK ===

# Team Members
for uid, member in data["team_members"].items():
    db.collection("team_members").document(uid).set(member)

# Project Info
if "project" in data and "info" in data["project"]:
   db.collection("project").document("info").set(data["project"]["info"])
else:
    print("⚠️ Project info missing in JSON")

# Tasks
for status, tasks in data["tasks"].items():
    db.collection("tasks").document(status).set({"items": tasks})

# Calendar
for member_id, events in data["calendar"].items():
    # Save events as a list under "events" key
    db.collection("calendar").document(member_id).set({"events": events})

print("✅ Firestore reset and repopulated successfully.")
