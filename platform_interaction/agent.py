from google.adk.agents import LlmAgent
from platform_interaction.firestore_mcp import (
    get_all_team_members, add_or_update_team_member, remove_team_member,
    get_project, set_project, remove_project,
    get_all_tasks, insert_task, remove_task,
    get_events, add_event, delete_event_by_index,
    nuke_database
)

root_agent = LlmAgent(
    name="PlatformInteraction",
    model="gemini-2.0-flash",
    description="Handles team, project, calendar, and task data in Firestore.",
    instruction="""
You have access to project-related data stored in Firestore. This includes details about the team, tasks, project goals and progress, and calendars.

When a user asks a question, decide which part of the data is most relevant and call the appropriate tool. You can retrieve:
- Team member profiles (roles, preferences, notes, personalities)
- Project status, goals, summary, and milestones
- Task lists categorized by status
- Calendar events for each team member

Examples of valid user requests:
- "Who’s the PM?" → Look for a team member with a PM-related role
- "Tell me about Leo" → Match by name or partial name
- "Which devs prefer mornings?" → Search `meeting_preference` fields for relevant phrases
- "What’s blocking us right now?" → Check `project_info.status.blockers`
- "Show me all pending tasks" → Use `tasks.pending`
- "What events does Ava have on Tuesday?" → Look up Ava’s calendar

Always respond naturally and concisely. Provide only what’s needed based on the question. You may include short summaries, bullet points, or direct answers.

Only call tools if information is not already available to you. Use the retrieved data to interpret the user’s intent and answer appropriately.
""",
    tools=[
        get_all_team_members, add_or_update_team_member, remove_team_member,
        get_project, set_project, remove_project,
        get_all_tasks, insert_task, remove_task,
        get_events, add_event, delete_event_by_index,
        nuke_database
    ]
)
