from langchain_core.messages import SystemMessage, HumanMessage

from app.llm import get_llm
from app.tools.vectorstore_tool import retrieve_relevant_chunks
from app.tools.search_tool import search_exchange_rate


llm = get_llm()

CHANNEL_AGENT_SYSTEM_PROMPT = """
You are the Channel Recommendation Agent for RemitGuard.

Your job is to help users choose safe and suitable channels for sending
remittances, especially when sending money to Bangladesh.

Use the provided retrieved knowledge and web search information.

Rules:
- Recommend authorized and regulated remittance channels.
- Prefer banks, licensed Money Transfer Operators (MTOs), authorized
  financial institutions, and officially supported mobile financial
  service channels.
- Do not recommend Hundi, Hawala, or other informal/illegal channels.
- Consider safety, regulation, transparency, fees, exchange rates,
  delivery speed, and recipient convenience.
- Do not claim a provider is licensed unless the provided evidence
  supports it.
- Do not invent fees, exchange rates, or regulatory information.
- Clearly distinguish facts from recommendations.
- Answer in the user's language when possible.

Provide:
1. Recommended channel options
2. Why each option is suitable
3. Important safety considerations
4. What the user should verify before sending money
"""


def run_channel_agent(user_query: str) -> str:
    retrieved_info = retrieve_relevant_chunks(user_query, k=4)

    search_results = search_exchange_rate(
        f"{user_query} safe legal remittance channels Bangladesh"
    )

    messages = [
        SystemMessage(content=CHANNEL_AGENT_SYSTEM_PROMPT),
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