# platform_interaction/firestore_mcp.py

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

# -- PROJECT TOOLS --

def get_project(data: dict) -> dict:
    project_data = get_project_info()
    if project_data:
        return {"status": "success", "data": project_data}
    else:
        return {"status": "error", "message": "Project info not found"}

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


