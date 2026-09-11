from tavily import TavilyClient

from app.config import settings


tavily_client = TavilyClient(api_key=settings.tavily_api_key)


def web_search(query: str, max_results: int = 5) -> dict:
    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        include_answer=True,
        include_raw_content=False,
    )

    sources = []

    for result in response.get("results", []):
        sources.append({
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "content": result.get("content", ""),
        })

    return {
        "answer": response.get("answer", ""),
        "sources": sources,
    }


# Keep existing agent imports working
def search_exchange_rate(query: str, max_results: int = 5) -> str:
    result = web_search(query, max_results)

    snippets = []

    if result["answer"]:
        snippets.append(result["answer"])

    for source in result["sources"]:
        snippets.append(
            f"- {source['title']}: {source['content']}\n"
            f"Source: {source['url']}"
        )

    return "\n\n".join(snippets)