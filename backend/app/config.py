from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    google_api_key: str
    groq_api_key: str
    tavily_api_key: str

    langchain_tracing_v2: bool = True
    langchain_api_key: str
    langchain_project: str = "remitguard"

    # LangSmith
    langsmith_tracing: bool = True
    langsmith_api_key: str
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    langsmith_project: str = "remitguard"

    app_env: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()