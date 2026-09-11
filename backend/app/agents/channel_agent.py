from langchain_core.messages import SystemMessage, HumanMessage

from app.llm import get_llm
from app.tools.vectorstore_tool import retrieve_relevant_chunks
from app.tools.search_tool import web_search


llm = get_llm()


CHANNEL_AGENT_SYSTEM_PROMPT = """
You are the Channel Recommendation Agent for RemitGuard.

Your job is to explain safe and legal ways to send money to Bangladesh.

IMPORTANT RULES:

1. Use the provided RAG knowledge and current web search results.
2. Prefer official or authoritative sources when available, especially
   Bangladesh Bank, BFIU, government/regulatory sources, and official
   provider pages.
3. Do not invent licensing, authorization, fees, exchange rates, limits,
   incentives, or delivery times.
4. Do not claim that a specific provider is authorized in Bangladesh unless
   the provided evidence explicitly supports it.
5. Do not mention IBAN unless the evidence specifically supports its use
   for the transaction being discussed.
6. Do not claim a provider is regulated by a particular regulator unless
   the evidence says so.
7. Clearly distinguish between:
   - information supported by sources
   - general safety advice
   - information that must be verified by the user
8. Recommend regulated/legal channels and warn users against informal
   Hundi/Hawala channels.
9. Always include the source title and URL when a web result provides one.
10. Answer in the user's language when possible.
11. Keep the answer practical and concise.

Structure the answer as:

### Safest options

### Why they are safer

### What to verify before sending

### Sources
"""


def run_channel_agent(user_query: str) -> str:

    retrieved_info = retrieve_relevant_chunks(
        user_query,
        k=4
    )

    search_data = web_search(
        f"{user_query} Bangladesh legal remittance official Bangladesh Bank BFIU"
    )

    web_answer = search_data.get("answer", "")

    web_sources = []

    for source in search_data.get("sources", []):
        web_sources.append(
            f"- {source.get('title', '')}\n"
            f"  {source.get('content', '')}\n"
            f"  Source: {source.get('url', '')}"
        )

    web_information = (
        f"Search answer:\n{web_answer}\n\n"
        f"Search sources:\n" +
        "\n\n".join(web_sources)
    )

    messages = [
        SystemMessage(content=CHANNEL_AGENT_SYSTEM_PROMPT),
        HumanMessage(
            content=(
                f"User question:\n{user_query}\n\n"
                f"Retrieved regulatory knowledge:\n{retrieved_info}\n\n"
                f"Current web information:\n{web_information}"
            )
        ),
    ]

    response = llm.invoke(messages)

    if isinstance(response.content, list):
        return "\n".join(
            item.get("text", "")
            for item in response.content
            if isinstance(item, dict)
            and item.get("type") == "text"
        )

    return response.content