from shared.firestore import get_team_members, add_team_member, delete_team_member, get_project_info, add_project_info, delete_project_info
from shared.firestore import get_tasks, add_task, delete_task, get_calendar_events, add_calendar_event, delete_calendar_event, delete_all_data
from shared.firestore import get_team_member, get_project, get_task, get_calendar_event

from pydantic import ValidationError # type: ignore
from shared.schema import (
    TeamMember, ProjectInfo, Tasks, CalendarEvent,
    ProjectInfo as ProjectInfoSchema,
    TeamMember as TeamMemberSchema,
    Tasks as TasksSchema,
    CalendarEvent as CalendarEventSchema,
)
from typing import Dict, List

# -- TEAM MEMBER TOOLS --

def get_all_team_members(data: dict) -> dict:
    return {"status": "success", "data": get_team_members()}

def add_or_update_team_member(data: dict) -> dict:
    member_id = data.get("member_id")
    member_data = data.get("member_data")
    if not member_id or not member_data:
        return {"status": "error", "message": "Missing member_id or member_data"}
    try:
        validated = TeamMemberSchema(**member_data)
        add_team_member(member_id, validated.dict())
        return {"status": "success", "message": "Team member added/updated"}
    except ValidationError as e:
        return {"status": "error", "message": f"Invalid member data: {e}"}

def remove_team_member(data: dict) -> dict:
    member_id = data.get("member_id")
    if not member_id:
        return {"status": "error", "message": "Missing member_id"}
    delete_team_member(member_id)
    return {"status": "success", "message": "Team member deleted"}


# -- PROJECT TOOLS --

def get_project(data: dict) -> dict:
    return {"status": "success", "data": get_project_info()}

def set_project(data: dict) -> dict:
    try:
        validated = ProjectInfoSchema(**data)
        add_project_info(validated.dict())
        return {"status": "success", "message": "Project info updated"}
    except ValidationError as e:
        return {"status": "error", "message": f"Invalid project data: {e}"}

def remove_project(data: dict) -> dict:
    delete_project_info()
    return {"status": "success", "message": "Project info deleted"}


# -- TASK TOOLS --

def get_all_tasks(data: dict) -> dict:
    return {"status": "success", "data": get_tasks()}

def insert_task(data: dict) -> dict:
    status = data.get("status")
    task = data.get("task")
    if not status or not task or not isinstance(task, str):
        return {"status": "error", "message": "Missing or invalid status/task"}
    
    add_task(status, task)
    return {"status": "success", "message": f"Task added to {status}"}


def remove_task(data: dict) -> dict:
    status = data.get("status")
    index = data.get("index")
    if status is None or index is None:
        return {"status": "error", "message": "Missing status or index"}
    result = delete_task(status, index)
    return {
        "status": "success" if result else "error",
        "message": "Task deleted" if result else "Invalid index or status"
    }


# -- CALENDAR TOOLS --

def get_events(data: dict) -> dict:
    member_id = data.get("member_id")
    if not member_id:
        return {"status": "error", "message": "Missing member_id"}
    return {"status": "success", "data": get_calendar_events(member_id)}

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


# -- GENERAL --

def nuke_database(data: dict) -> dict:
    delete_all_data()
    return {"status": "success", "message": "All data deleted"}
