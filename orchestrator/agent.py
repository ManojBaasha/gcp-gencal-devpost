from google.adk.agents import LlmAgent
from platform_interaction.agent import root_agent as platform_agent

root_agent = LlmAgent(
    name="Orchestrator",
    model="gemini-2.0-flash",
    instruction="You're the central coordinator. You manage the platform agent and ensure all tasks are executed correctly.",
    description="Top-level orchestrator for GCPCal system.",
    sub_agents=[platform_agent]
)
