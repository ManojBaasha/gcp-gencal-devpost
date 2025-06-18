from google.adk.agents import LlmAgent
from social_profiling.profiler import analyze_user_calendar

root_agent = LlmAgent(
    name="SocialProfiling",
    model="gemini-2.0-flash",
    description="Understands the user's past calendar behavior and time preferences.",
    instruction="You will figure out all the user's preference's",
    tools = [analyze_user_calendar]
    )
