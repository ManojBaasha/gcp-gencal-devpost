from shared.firestore import insert_event, update_event_entry, delete_event_entry

def create_event(data: dict) -> dict:
    insert_event(data)
    return {"status": "success", "message": "Event created."}

def update_event(data: dict) -> dict:
    update_event_entry(data)
    return {"status": "success", "message": "Event updated."}

def delete_event(event_id: str) -> dict:
    delete_event_entry(event_id)
    return {"status": "success", "message": "Event deleted."} 