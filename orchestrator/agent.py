from google.adk.agents import LlmAgent
from social_profiling.agent import root_agent as social_agent
from event_planning.agent import root_agent as planning_agent
from platform_interaction.agent import root_agent as platform_agent

root_agent = LlmAgent(
    name="Orchestrator",
    model="gemini-2.0-flash",
    instruction="You're the central coordinator. Use SocialProfiling for user insights, EventPlanning for finding shared time, and PlatformInteraction to manage events.",
    description="Top-level orchestrator for GCPCal system.",
    sub_agents=[social_agent, planning_agent, platform_agent]
)
