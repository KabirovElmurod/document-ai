from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://document_ai:document_ai_password@localhost:5432/document_ai"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    UPLOAD_DIR: Path = Path("../uploads")
    MAX_UPLOAD_MB: int = 50
    
    GROQ_API_KEY: str = ""
    
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()
