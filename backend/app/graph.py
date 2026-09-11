from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END

from app.agents.router_agent import classify_intent
from app.agents.rate_agent import run_rate_agent
from app.agents.scam_agent import run_scam_agent
from app.agents.channel_agent import run_channel_agent
from app.agents.general_agent import run_general_agent
from app.agents.aggregator import aggregate_response


class RemitGuardState(TypedDict):
    user_query: str
    route: str
    rate_result: Optional[str]
    scam_result: Optional[str]
    channel_result: Optional[str]
    general_result: Optional[str]
    final_response: Optional[dict]


def router_node(state: RemitGuardState) -> RemitGuardState:
    state["route"] = classify_intent(state["user_query"])
    return state


def rate_node(state: RemitGuardState) -> RemitGuardState:
    state["rate_result"] = run_rate_agent(state["user_query"])
    return state


def scam_node(state: RemitGuardState) -> RemitGuardState:
    state["scam_result"] = run_scam_agent(state["user_query"])
    return state


def channel_node(state: RemitGuardState) -> RemitGuardState:
    state["channel_result"] = run_channel_agent(state["user_query"])
    return state


def general_node(state: RemitGuardState) -> RemitGuardState:
    state["general_result"] = run_general_agent(state["user_query"])
    return state


def aggregator_node(state: RemitGuardState) -> RemitGuardState:
    state["final_response"] = aggregate_response(state)
    return state


def route_decision(state: RemitGuardState) -> str:
    if state["route"] == "scam":
        return "scam"

    if state["route"] == "channel":
        return "channel"

    if state["route"] == "general":
        return "general"

    return "rate"


graph = StateGraph(RemitGuardState)

graph.add_node("router", router_node)
graph.add_node("rate", rate_node)
graph.add_node("scam", scam_node)
graph.add_node("channel", channel_node)
graph.add_node("general", general_node)
graph.add_node("aggregator", aggregator_node)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    route_decision,
    {
        "rate": "rate",
        "scam": "scam",
        "channel": "channel",
        "general": "general",
    },
)

graph.add_edge("rate", "aggregator")
graph.add_edge("scam", "aggregator")
graph.add_edge("channel", "aggregator")
graph.add_edge("general", "aggregator")

graph.add_edge("aggregator", END)

app_graph = graph.compile()