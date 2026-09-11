from langchain_core.messages import SystemMessage, HumanMessage

from app.llm import get_llm
from app.tools.vectorstore_tool import retrieve_relevant_chunks
from app.tools.search_tool import search_exchange_rate


llm = get_llm()

SCAM_AGENT_SYSTEM_PROMPT = """
You are the Scam Detection Agent for RemitGuard.

Your job is to help users identify potentially risky or fraudulent
remittance channels, agents, websites, offers, and payment requests.

Use the provided retrieved knowledge and web search information.

Rules:
- Do not claim something is definitely a scam unless the evidence clearly
  supports that conclusion.
- Clearly distinguish between confirmed facts, warning signs, and uncertainty.
- Look for common scam indicators such as unrealistic exchange rates,
  requests for advance payment, unofficial channels, suspicious links,
  identity/document requests, and pressure to act quickly.
- For Bangladesh-related remittance questions, prioritize the provided
  Bangladesh AML/CFT and regulatory information.
- Give practical safety advice.
- Never invent evidence or sources.
- Answer in the user's language when possible.

Provide:
1. Risk assessment
2. Warning signs found
3. Why the signs are concerning
4. Recommended safe action
"""


def run_scam_agent(user_query: str) -> str:
    retrieved_info = retrieve_relevant_chunks(user_query, k=4)

    search_results = search_exchange_rate(
    f"{user_query} Bangladesh Bank BFIU official hundi hawala remittance fraud AML CFT"
    )

    messages = [
        SystemMessage(content=SCAM_AGENT_SYSTEM_PROMPT),
        HumanMessage(
            content=(
                f"User question:\n{user_query}\n\n"
                f"Retrieved knowledge:\n{retrieved_info}\n\n"
                f"Web search information:\n{search_results}"
            )
        ),
    ]

    response = llm.invoke(messages)

    if isinstance(response.content, list):
        return "\n".join(
            item.get("text", "")
            for item in response.content
            if isinstance(item, dict) and item.get("type") == "text"
        )

    return response.content