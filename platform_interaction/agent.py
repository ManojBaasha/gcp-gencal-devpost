from google.adk.agents import LlmAgent
from platform_interaction.firestore_mcp import (
    create_event,
    update_event,
    delete_event,
)

root_agent = LlmAgent(
    name="PlatformInteraction",
    model="gemini-2.0-flash",
    description="Creates, updates, or deletes calendar events using Firestore.",
    instruction="You will interact with the platform to manage calendar events.",
    tools=[
        create_event,
        update_event,
        delete_event,
    ]
)
