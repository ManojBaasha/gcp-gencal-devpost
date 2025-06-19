from vertexai.preview import reasoning_engines
from orchestrator.agent import root_agent


app = reasoning_engines.AdkApp(agent=root_agent)

session = app.create_session(user_id="user")
print("Session ID:", session.id)
