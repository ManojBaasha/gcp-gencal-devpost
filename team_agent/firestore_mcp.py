# platform_interaction/firestore_mcp.py

from shared.firestore import get_team_members, add_team_member, delete_team_member

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
