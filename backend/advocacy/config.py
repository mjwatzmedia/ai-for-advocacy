from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ADVOCACY_", env_file=".env", extra="ignore")
    cors_origins: str = "http://localhost:5173,http://localhost:8080,http://127.0.0.1:8080"
    api_token: str = ""
    llm_provider: str = "disabled"
    llm_api_key: str = ""
    llm_model: str = ""
    llm_timeout: float = Field(default=30, ge=1, le=90)
    llm_max_tokens: int = Field(default=1800, ge=128, le=4000)
    # Disabled until operator explicitly accepts estimated cost controls.
    llm_calls_per_hour: int = Field(default=0, ge=0, le=100)
    llm_budget_usd_per_hour: float = Field(default=0, ge=0, le=20)
    llm_input_usd_per_million: float = Field(default=0, ge=0)
    llm_output_usd_per_million: float = Field(default=0, ge=0)
    requests_per_minute: int = Field(default=12, ge=1, le=120)
    retrieval_timeout: float = Field(default=10, ge=1, le=30)
    max_source_bytes: int = Field(default=1500000, ge=10000, le=3000000)
    max_request_bytes: int = 240000
    max_parallel_research: int = Field(default=2, ge=1, le=4)

    def ai_ready(self):
        return (self.llm_provider in ("openai", "gemini") and bool(self.llm_api_key)
                and bool(self.llm_model) and self.llm_calls_per_hour > 0
                and self.llm_budget_usd_per_hour > 0
                and self.llm_input_usd_per_million > 0
                and self.llm_output_usd_per_million > 0)