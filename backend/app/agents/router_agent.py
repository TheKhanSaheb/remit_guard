from langchain_core.messages import SystemMessage, HumanMessage

from app.llm import get_llm


llm = get_llm()

ROUTER_SYSTEM_PROMPT = """
You are the Router Agent for RemitGuard.

Read the user's query and classify it into exactly ONE category:

- rate -> exchange rate or remittance rate questions
- scam -> questions about whether a remittance channel, agent, website, or offer is trustworthy or fraudulent
- channel -> questions asking for the safest, best, or most suitable way to send money
- general -> anything else

Return ONLY one word:
rate
scam
channel
general
"""


def classify_intent(user_query: str) -> str:
    messages = [
        SystemMessage(content=ROUTER_SYSTEM_PROMPT),
        HumanMessage(content=user_query),
    ]

    response = llm.invoke(messages)

    content = response.content

    if isinstance(content, list):
        content = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict) and item.get("type") == "text"
        )

    route = str(content).strip().lower()

    if route not in ("rate", "scam", "channel", "general"):
        route = "rate"

    return route