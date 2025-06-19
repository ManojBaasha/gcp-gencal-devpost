# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from orchestrator.agent import root_agent as orchestrator_agent
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import traceback
import os


os.environ["GOOGLE_CLOUD_PROJECT"] = "gcp-gencal-devpost"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
os.environ["USE_VERTEX_AI"] = "true"
os.environ["GOOGLE_API_KEY"] = "AIzaSyCm0oKlz3lgrvTQzS1pi9vqXbuPuZAIhU0"


app = FastAPI(
    title="Orchestrator Agent API",
    description="API for interacting with the Orchestrator LLM agent and its sub-agents.",
    version="0.1.0"
)

origins = [
    "http://localhost",
    "http://localhost:3000", # Example for a React dev server
    "https://product-manager-devpost.web.app",
    "https://*.web.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/orchestrate")
async def run_orchestrator(request: dict):
    try:
        message = request.get("message")
        context = request.get("context", {})

        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        content = types.Content(role='user', parts=[types.Part(text=message)])

        session_service = InMemorySessionService()
        session_id = "56b47296-01e7-42a6-a25a-b2b34b3907c3"
        await session_service.create_session(app_name="OrchestratorApp", user_id="user123", session_id=session_id)

        runner = Runner(agent=orchestrator_agent, app_name="OrchestratorApp", session_service=session_service)

        responses = []
        async for event in runner.run_async(user_id="user123", session_id=session_id, new_message=content):
            if event.is_final_response():
                responses.append(event.content.parts[0].text)

        return {"responses": responses}

    except Exception as e:
        print("❌ Exception occurred:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interacting with orchestrator: {str(e)}")


# You could also expose specific sub-agents if needed, though the orchestrator
# is designed to handle routing. For example:
# from team_agent.agent import root_agent as team_agent
# @app.post("/team_agent_action")
# async def run_team_agent_action(request: UserRequest):
#     try:
#         response = await team_agent.ask(request.message, context=request.context)
#         return {"response": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error interacting with team agent: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    
    
'''
Example Snippet 
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

import yfinance as yf


APP_NAME = "stock_app"
USER_ID = "1234"
SESSION_ID = "session1234"

def get_stock_price(symbol: str):
    """
    Retrieves the current stock price for a given symbol.

    Args:
        symbol (str): The stock symbol (e.g., "AAPL", "GOOG").

    Returns:
        float: The current stock price, or None if an error occurs.
    """
    try:
        stock = yf.Ticker(symbol)
        historical_data = stock.history(period="1d")
        if not historical_data.empty:
            current_price = historical_data['Close'].iloc[-1]
            return current_price
        else:
            return None
    except Exception as e:
        print(f"Error retrieving stock price for {symbol}: {e}")
        return None


stock_price_agent = Agent(
    model='gemini-2.0-flash',
    name='stock_agent',
    instruction= 'You are an agent who retrieves stock prices. If a ticker symbol is provided, fetch the current price. If only a company name is given, first perform a Google search to find the correct ticker symbol before retrieving the stock price. If the provided ticker symbol is invalid or data cannot be retrieved, inform the user that the stock price could not be found.',
    description='This agent specializes in retrieving real-time stock prices. Given a stock ticker symbol (e.g., AAPL, GOOG, MSFT) or the stock name, use the tools and reliable data sources to provide the most up-to-date price.',
    tools=[get_stock_price], # You can add Python functions directly to the tools list; they will be automatically wrapped as FunctionTools.
)


# Session and Runner
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=stock_price_agent, app_name=APP_NAME, session_service=session_service)


# Agent Interaction
def call_agent(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)

call_agent("stock price of GOOG")
'''