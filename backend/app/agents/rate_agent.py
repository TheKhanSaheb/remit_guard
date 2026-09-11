from langchain_core.messages import SystemMessage, HumanMessage

from app.llm import get_llm
from app.tools.search_tool import search_exchange_rate


llm = get_llm()

RATE_AGENT_SYSTEM_PROMPT = """তুমি RemitGuard-এর Rate Comparator Agent।

তোমার কাজ হলো user-এর remittance exchange-rate প্রশ্নের উত্তর দেওয়া।

নিয়ম:
1. Search tool থেকে পাওয়া সর্বশেষ web তথ্য ব্যবহার করবে।
2. নিজের পুরনো জ্ঞান থেকে exchange rate অনুমান করবে না।
3. Search result-এ যে rate পাওয়া যায় সেটি স্পষ্টভাবে উল্লেখ করবে।
4. এটি mid-market/reference rate হতে পারে—remittance provider-এর actual payout rate একই নাও হতে পারে।
5. User-কে provider-এর final receive amount, fees এবং exchange-rate markup transaction করার আগে যাচাই করতে বলবে।
6. Search result-এর source title এবং URL উল্লেখ করবে।
7. কোনো তথ্য search result-এ না থাকলে সেটা বানিয়ে বলবে না।
8. উত্তর সংক্ষিপ্ত, পরিষ্কার এবং নিরাপদ রাখবে।
"""


def run_rate_agent(user_query: str) -> str:
    search_results = search_exchange_rate(
        f"{user_query} current exchange rate today 2026 Bangladesh remittance"
    )

    messages = [
        SystemMessage(content=RATE_AGENT_SYSTEM_PROMPT),
        HumanMessage(
            content=(
                f"User question: {user_query}\n\n"
                f"Current web search results:\n{search_results}"
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