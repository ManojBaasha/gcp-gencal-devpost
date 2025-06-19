# setup.py
from fastapi.middleware.cors import CORSMiddleware
from adk.adapters.fast_api import AdkFastAPI



def setup_middlewares(app: AdkFastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # 👈 frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
