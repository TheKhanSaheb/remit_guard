from google import genai

from app.config import settings


client = genai.Client(api_key=settings.google_api_key)


def google_search(query: str) -> str:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=query,
        config={
            "tools": [
                {"google_search": {}}
            ]
        },
    )

    return response.text