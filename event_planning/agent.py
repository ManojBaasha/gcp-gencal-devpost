from google.adk.agents import LlmAgent
from event_planning.planner import plan_event_with_friends

root_agent = LlmAgent(
    name="EventPlanning",
    model="gemini-2.0-flash",
    description="Finds mutual availability between friends and suggests time slots.",
    instruction="You will interact with the platform to manage calendar events.",
    tools=[
        plan_event_with_friends,
    ]
)
