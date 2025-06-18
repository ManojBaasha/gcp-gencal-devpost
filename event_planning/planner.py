from shared.utils import intersect_time_ranges

def plan_event_with_friends(user_pref: dict = None) -> dict:
    # Dummy availability
    alex = [("18:00", "20:00")]
    claire = [("19:00", "21:00")]
    user = user_pref.get("preferred_study_time", ["18:00", "20:00"])
    mutual = intersect_time_ranges([alex, claire, [user]])
    return {"status": "success", "suggested_slots": mutual} 