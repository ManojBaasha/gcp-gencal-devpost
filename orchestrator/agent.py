# orchestrator/agent.py

from google.adk.agents import LlmAgent # type: ignore
from team_agent.agent import root_agent as team_agent
from task_agent.agent import root_agent as task_agent
from project_agent.agent import root_agent as project_agent
from calendar_agent.agent import root_agent as calendar_agent

root_agent = LlmAgent(
    name="Orchestrator",
    model="gemini-2.0-flash",
    instruction="You are the top-level orchestrator for the system. Your role is to manage and coordinate the interactions between various sub-agents responsible for team management, task handling, project oversight, and calendar scheduling.",
    description="Top-level orchestrator for GCPCal system.",
    sub_agents=[team_agent, task_agent, project_agent, calendar_agent]
)
