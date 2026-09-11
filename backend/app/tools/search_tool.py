from tavily import TavilyClient
from app.config import settings

tavily_client = TavilyClient(api_key=settings.tavily_api_key)

def search_exchange_rate(query: str, max_results: int = 5) -> str:
    """
    Tavily দিয়ে live exchange rate / remittance সংক্রান্ত তথ্য খুঁজে আনে।
    LLM-কে দেওয়ার জন্য একটা readable string হিসেবে ফেরত দেয়।
    """
    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
    )
    snippets = []
    for result in response.get("results", []):
        snippets.append(f"- {result['title']}: {result['content']}")
    return "\n".join(snippets)