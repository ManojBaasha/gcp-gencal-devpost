# platform_interaction/firestore_mcp.py

from shared.firestore import get_tasks, add_task, delete_task

from pydantic import ValidationError # type: ignore
from shared.schema import (
    TeamMember, ProjectInfo, Tasks, CalendarEvent,
    ProjectInfo as ProjectInfoSchema,
    TeamMember as TeamMemberSchema,
    Tasks as TasksSchema,
    CalendarEvent as CalendarEventSchema,
)
from typing import Dict, List

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

