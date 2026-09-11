from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from app.config import settings


# Primary LLM
primary_llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=settings.google_api_key,
    temperature=0,
)


# Fallback LLM
fallback_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    groq_api_key=settings.groq_api_key,
    temperature=0,
)


class FallbackLLM:
    """
    Try Gemini for every request.
    If Gemini fails, automatically use Groq.
    """

    def __init__(self, primary, fallback):
        self.primary = primary
        self.fallback = fallback

    def invoke(self, input, config=None, **kwargs):
        try:
            return self.primary.invoke(
                input,
                config=config,
                **kwargs
            )

        except Exception:
            print("Gemini unavailable. Switching to Groq...")

            return self.fallback.invoke(
                input,
                config=config,
                **kwargs
            )


def get_llm():
    return FallbackLLM(
        primary_llm,
        fallback_llm
    )