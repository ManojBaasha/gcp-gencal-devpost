from shared.firestore import get_user_events

def analyze_user_calendar(user_id: str = "user") -> dict:
    events = get_user_events(user_id)
    # Placeholder logic
    preferences = {
        "preferred_study_time": "19:00-21:00",
        "avoid": ["Monday 8:00-10:00"],
    }
    return {"status": "success", "preferences": preferences} 