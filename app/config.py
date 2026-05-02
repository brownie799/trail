from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = Field(default="")
    openai_model: str = Field(default="gpt-4o-mini")
    use_openai: bool = Field(default=False)
    confidence_threshold: float = Field(default=0.78)
    kb_index_path: str = Field(default="data/kb/faiss.index")
    kb_meta_path: str = Field(default="data/kb/meta.json")

    class Config:
        env_file = ".env"


settings = Settings()
