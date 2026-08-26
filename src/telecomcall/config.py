from typing import ClassVar

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# --- Groq Configuration ---
class GroqSettings(BaseModel):
    api_key: str = Field(default="", description="Groq API Key")
    base_url: str = Field(
        default="https://api.groq.com/openai/v1", description="Groq Base URL"
    )
    model: str = Field(default="openai/gpt-oss-20b", description="Groq Model to use")


# --- Twilio Configuration ---
class TwilioSettings(BaseModel):
    account_sid: str = Field(default="", description="Twilio Account SID")
    auth_token: str = Field(default="", description="Twilio Auth Token")
    phone_number: str = Field(default="", description="Twilio Phone Number")


# --- Qdrant Configuration ---
class QdrantSettings(BaseModel):
    host: str = Field(default="localhost", description="Qdrant Host")
    port: int = Field(default=6333, description="Qdrant Port")
    api_key: str = Field(default="", description="Qdrant API Key")
    cluster_url: str = Field(default="", description="Qdrant Cloud Cluster URL")
    use_qdrant_cloud: bool = Field(default=False, description="Use Qdrant Cloud")


# --- Opik Configuration ---
class OpikSettings(BaseModel):
    api_key: str = Field(default="", description="Opik API Key")
    workspace: str = Field(default="telecomcall", description="Opik Workspace")


# --- Settings Configuration ---
class Settings(BaseSettings):
    groq: GroqSettings = Field(default_factory=GroqSettings)
    twilio: TwilioSettings = Field(default_factory=TwilioSettings)
    qdrant: QdrantSettings = Field(default_factory=QdrantSettings)
    opik: OpikSettings = Field(default_factory=OpikSettings)
    stt_model: str = Field(default="groq-whisper", description="STT Model to use")
    tts_model: str = Field(default="edge-tts", description="TTS Model to use")

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=[".env"],
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
        case_sensitive=False,
        frozen=True,
    )


settings = Settings()
