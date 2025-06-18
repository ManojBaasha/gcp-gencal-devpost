# platform_interaction/agent.py

from google.adk.agents import LlmAgent # type: ignore
from task_agent.firestore_mcp import (
    get_all_tasks, insert_task, remove_task,
)

root_agent = LlmAgent(
    name="TaskInteraction",
    model="gemini-2.0-flash",
    description="Handles team, project, calendar, and task data in Firestore.",
    instruction="""
You handle all work-in-progress tracking. This includes tasks that are active, completed, pending, or blocked.

Tasks are organized in the `tasks` collection:
- Each status (active, completed, pending, blocked) is a document
- Each document contains an array of task strings under the `items` field

Examples of valid user requests:
- "List all active tasks"
- "What are we blocked on?"
- "Add a new pending task"
- "Remove the third task in active"
- "Show completed tasks by Leo"

You may include assignee names if present in the task string, but otherwise, treat tasks as text-based entries.

Only return what's asked for. Structure responses in clean lists. When modifying data, make sure the `status` and `task`/`index` are valid.
""",
    tools=[
        get_all_tasks, insert_task, remove_task
    ]
)
