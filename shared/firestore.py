# Simulated Firestore stub
_firestore_db = {}

def get_user_events(user_id: str):
    return _firestore_db.get(user_id, [])

def insert_event(data):
    user = data.get("user", "user")
    _firestore_db.setdefault(user, []).append(data)

def update_event_entry(data):
    delete_event_entry(data.get("id"))
    insert_event(data)

def delete_event_entry(event_id):
    for user in _firestore_db:
        _firestore_db[user] = [e for e in _firestore_db[user] if e.get("id") != event_id] 