import os

from fastapi import FastAPI
from pydantic import BaseModel

from app.config import settings

os.environ["LANGSMITH_TRACING"] = str(settings.langsmith_tracing).lower()
os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
os.environ["LANGSMITH_ENDPOINT"] = settings.langsmith_endpoint
os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project

from app.graph import app_graph
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="RemitGuard")


app = FastAPI(title="RemitGuard")


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "env": settings.app_env
    }


@app.post("/chat")
def chat(request: ChatRequest):


    result = app_graph.invoke({
        "user_query": request.message
    })

    return {
        "route": result["route"],
        "response": result["final_response"]
    }


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)