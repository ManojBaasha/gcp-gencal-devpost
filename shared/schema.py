# shared/schema.py

from pydantic import BaseModel, Field # type: ignore
from typing import Dict, List, Any

class TeamMember(BaseModel):
    name: str
    role: str
    personality: str
    meeting_preference: str
    notes: str

class Status(BaseModel):
    sprint: str
    progress_percent: int
    blockers: str
    next_milestone: str

class ProjectInfo(BaseModel):
    name: str
    summary: str
    goals: List[str]
    timeline: str
    status: Status

class Tasks(BaseModel):
    completed: List[str]
    active: List[str]
    pending: List[str]
    blocked: List[str]

class CalendarEvent(BaseModel):
    day: str
    time: str
    event: str

class EventSchema(BaseModel):
    team_members: Dict[str, TeamMember]
    project_info: ProjectInfo
    tasks: Tasks
    calendar: Dict[str, List[CalendarEvent]]