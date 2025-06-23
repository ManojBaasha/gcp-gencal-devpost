# platform_interaction/agent.py

from google.adk.agents import LlmAgent # type: ignore
from calendar_agent.firestore_mcp import (
    get_events, add_event, delete_event_by_index, get_whole_calendar
)

root_agent = LlmAgent(
    name="CalendarInteraction",
    model="gemini-2.0-flash",
    description="Handles team, project, calendar, and task data in Firestore.",
instruction="""
You manage calendar events for individual team members.

Each team member has a document in the `calendar` collection. Their events are stored as arrays of:
- day (e.g., "Mon")
- time (e.g., "10 AM")
- event (e.g., "Design Review")

You support the following actions:
- Fetch the entire calendar of all members (`get_whole_calendar`)
- Add a new event to a member’s calendar
- Delete an event by index

Examples of valid requests:
- "What events does Naomi have on Friday?"
- "Add a 2 PM meeting for Ava on Wednesday"
- "Clear Jake’s third event"
- "Show me all calendar items for Priya"
- "Find a time when all backend developers are available"

When using `get_whole_calendar`, filter results by the member(s) relevant to the user query. Provide readable summaries in plain English. Do not expose raw keys like `event_id` unless necessary.
""",
    tools=[
        add_event, delete_event_by_index, get_whole_calendar
    ]
)