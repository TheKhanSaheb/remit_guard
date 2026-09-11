from langchain_core.messages import SystemMessage, HumanMessage

from app.llm import get_llm
from app.tools.search_tool import search_exchange_rate


llm = get_llm()

RATE_AGENT_SYSTEM_PROMPT = """তুমি RemitGuard-এর Rate Comparator Agent।
তোমার কাজ: user-কে সবচেয়ে ভালো ও সাম্প্রতিক remittance exchange rate সম্পর্কে জানানো।
তোমাকে search tool থেকে পাওয়া real-time তথ্য ব্যবহার করতে হবে, নিজের পুরনো জ্ঞান থেকে rate অনুমান করবে না।
উত্তর সংক্ষিপ্ত, স্পষ্ট এবং কোন source থেকে তথ্য নিয়েছ তা উল্লেখ করে দিতে হবে।
"""

def run_rate_agent(user_query: str) -> str:
    search_results = search_exchange_rate(
    f"{user_query} current exchange rate today 2026 Bangladesh remittance"
     )

    messages = [
        SystemMessage(content=RATE_AGENT_SYSTEM_PROMPT),
        HumanMessage(
            content=f"User question: {user_query}\n\nSearch results:\n{search_results}"
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