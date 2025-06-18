# calendar_agent/firestore_mcp.py

from shared.firestore import get_calendar_events, add_calendar_event, delete_calendar_event, get_team_members, delete_all_data

from pydantic import ValidationError # type: ignore
from shared.schema import (
    TeamMember, ProjectInfo, Tasks, CalendarEvent,
    ProjectInfo as ProjectInfoSchema,
    TeamMember as TeamMemberSchema,
    Tasks as TasksSchema,
    CalendarEvent as CalendarEventSchema,
)
from typing import Dict, List

# -- CALENDAR TOOLS --

def get_events(data: dict) -> dict:
    name = data.get("name")
    if not name:
        return {"status": "error", "message": "Missing name"}

    all_members = get_team_members()
    matched = [
        (member_id, info)
        for member_id, info in all_members.items()
        if name.lower() in info.get("name", "").lower()
    ]

    if not matched:
        return {"status": "error", "message": f"No user found with name matching '{name}'"}
    if len(matched) > 1:
        return {
            "status": "error",
            "message": f"Multiple matches for '{name}': {[info['name'] for _, info in matched]}"
        }

    member_id = matched[0][0]
    events = get_calendar_events(member_id)
    return {"status": "success", "data": events}

def get_whole_calendar() -> dict:
    all_members = get_team_members()
    calendar_data = {}
    
    for member_id, info in all_members.items():
        events = get_calendar_events(member_id)
        if events:
            calendar_data[member_id] = {
                "name": info.get("name", "Unknown"),
                "events": events
            }
    
    return {"status": "success", "data": calendar_data}


def add_event(data: dict) -> dict:
    member_id = data.get("member_id")
    event = data.get("event")
    if not member_id or not event:
        return {"status": "error", "message": "Missing member_id or event"}
    try:
        validated = CalendarEventSchema(**event)
        add_calendar_event(member_id, validated.dict())
        return {"status": "success", "message": "Event added"}
    except ValidationError as e:
        return {"status": "error", "message": f"Invalid event data: {e}"}

def delete_event_by_index(data: dict) -> dict:
    member_id = data.get("member_id")
    index = data.get("index")
    if member_id is None or index is None:
        return {"status": "error", "message": "Missing member_id or index"}
    result = delete_calendar_event(member_id, index)
    return {
        "status": "success" if result else "error",
        "message": "Deleted" if result else "Invalid index"
    }

