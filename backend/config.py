import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    TMDB_API_KEY: str = Field(..., env="TMDB_API_KEY")
    VOYAGE_API_KEY: str = Field(..., env="VOYAGE_API_KEY")
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    QDRANT_URL: Optional[str] = Field(None, env="QDRANT_URL")
    QDRANT_API_KEY: Optional[str] = Field(None, env="QDRANT_API_KEY")
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    VOYAGE_BASE_URL: str = "https://api.voyageai.com/v1/embeddings"
    MAX_RECOMMENDATIONS: int = 10

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()


