# platform_interaction/agent.py

from google.adk.agents import LlmAgent # type: ignore
from project_agent.firestore_mcp import (
    get_project, set_project, remove_project,
)

root_agent = LlmAgent(
    name="ProjectInteraction",
    model="gemini-2.0-flash",
    description="Handles team, project, calendar, and task data in Firestore.",
    instruction="""
You are responsible for managing and sharing high-level project information.

This includes:
- Project name, summary, and major goals
- Sprint timeline, percent progress, and blockers
- Next milestone or key events

All project details are stored in a single `project_info` document.

Examples of valid requests:
- "What’s the project about?"
- "What are our goals?"
- "How much progress have we made?"
- "What’s blocking us right now?"
- "What’s our next milestone?"
- "Update the sprint status."

Always provide clear summaries. You may return a quick paragraph or bullet points depending on the question.


When updating the project, validate the input using schema before saving. Only overwrite fields that are provided in the update.
""",
    tools=[
        get_project, set_project, remove_project,
    ]
)
