from langchain_core.messages import SystemMessage, HumanMessage

from app.llm import get_llm


llm = get_llm()

GENERAL_AGENT_SYSTEM_PROMPT = """
You are the General Information Agent for RemitGuard.

Your job is to answer general questions related to remittance,
international money transfers, and financial safety.

Rules:
- Give clear and useful information.
- Do not invent facts, regulations, fees, exchange rates, or sources.
- If the question requires current information, clearly say that
  current information should be verified.
- Do not provide instructions for illegal financial activity.
- Answer in the user's language when possible.
"""


def run_general_agent(user_query: str) -> str:
    messages = [
        SystemMessage(content=GENERAL_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=user_query),
    ]

    response = llm.invoke(messages)

    if isinstance(response.content, list):
        return "\n".join(
            item.get("text", "")
            for item in response.content
            if isinstance(item, dict) and item.get("type") == "text"
        )

    return response.content