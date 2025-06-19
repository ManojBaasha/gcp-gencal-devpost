# shared/firestore.py

import firebase_admin # type: ignore
from firebase_admin import credentials # type: ignore
from firebase_admin import firestore # type: ignore

from dotenv import load_dotenv
load_dotenv()

# Path to your service account key file
SERVICE_ACCOUNT_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Initialize Firestore DB
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()
    
def get_team_members():
    """Fetch all team members."""
    members_ref = db.collection('team_members')
    return {doc.id: doc.to_dict() for doc in members_ref.stream()}

def add_team_member(member_id: str, member_data: dict):
    """Add or update a team member."""
    members_ref = db.collection('team_members')
    members_ref.document(member_id).set(member_data)
    
def delete_team_member(member_id: str):
    """Delete a team member."""
    members_ref = db.collection('team_members')
    members_ref.document(member_id).delete()
    
def get_project_info():
    """Fetch project information."""
    project_ref = db.collection('project').document('info')
    doc = project_ref.get()
    return doc.to_dict() if doc.exists else None

def add_project_info(project_data: dict):
    project_ref = db.collection('project').document('info')
    project_ref.set(project_data)

def delete_project_info():
    project_ref = db.collection('project').document('info')
    project_ref.delete()

    
def get_tasks():
    """Fetch all task categories from their separate documents."""
    tasks_collection = db.collection('tasks')
    task_data = {}

    for status in ['active', 'completed', 'pending', 'blocked']:
        doc = tasks_collection.document(status).get()
        if doc.exists:
            task_data[status] = doc.to_dict().get("items", [])
        else:
            task_data[status] = []

    return task_data


def add_task(status: str, task: str):
    """Add task to the proper status document under `items` array."""
    doc_ref = db.collection('tasks').document(status)
    doc = doc_ref.get()
    current = doc.to_dict().get("items", []) if doc.exists else []
    current.append(task)
    doc_ref.set({"items": current})


    
def delete_task(status: str, index: int):
    """Delete a task from a specific list by index."""
    tasks_ref = db.collection('tasks').document('info')
    doc = tasks_ref.get()
    tasks_data = doc.to_dict() if doc.exists else {}

    if status not in tasks_data or not isinstance(tasks_data[status], list):
        return False
    
    if 0 <= index < len(tasks_data[status]):
        del tasks_data[status][index]
        tasks_ref.set(tasks_data)
        return True
    return False

        
def get_calendar_events(member_id: str):
    """Fetch calendar events for a specific team member."""
    calendar_ref = db.collection('calendar').document(member_id)
    return calendar_ref.get().to_dict() if calendar_ref.get().exists else None

def add_calendar_event(member_id: str, event_data: dict):
    """Add or update a calendar event for a specific team member."""
    calendar_ref = db.collection('calendar').document(member_id)
    calendar_ref.set(event_data, merge=True)
    
def delete_calendar_event(member_id: str, event_id: str):
    """Delete a specific calendar event for a team member."""
    calendar_ref = db.collection('calendar').document(member_id)
    calendar_data = calendar_ref.get().to_dict()
    if calendar_data and event_id in calendar_data:
        del calendar_data[event_id]
        calendar_ref.set(calendar_data)
        
def delete_all_data():
    """Delete all data in the Firestore database."""
    collections = db.collections()
    for collection in collections:
        docs = collection.stream()
        for doc in docs:
            doc.reference.delete()
    print("All data deleted successfully.")
    
def get_team_member(member_id: str):
    """Fetch a specific team member by ID."""
    members_ref = db.collection('team_members').document(member_id)
    return members_ref.get().to_dict() if members_ref.get().exists else None

def get_project():
    """Fetch the project information."""
    project_ref = db.collection('project_info').document('info')
    return project_ref.get().to_dict() if project_ref.get().exists else None

def get_task(task_id: str):
    """Fetch a specific task by ID."""
    tasks_ref = db.collection('tasks').document('info')
    tasks_data = tasks_ref.get().to_dict()
    if tasks_data and task_id in tasks_data['active']:
        return {task_id: tasks_data['active'][task_id]}
    return None

def get_calendar_event(member_id: str, event_id: str):
    """Fetch a specific calendar event for a team member."""
    calendar_ref = db.collection('calendar').document(member_id)
    calendar_data = calendar_ref.get().to_dict()
    if calendar_data and event_id in calendar_data:
        return {event_id: calendar_data[event_id]}
    return None




