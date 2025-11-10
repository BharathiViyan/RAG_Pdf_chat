import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings(BaseModel):
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))

    hf_token: str | None = os.getenv("HF_TOKEN")

    embedding_model_name: str = os.getenv(
        "EMBEDDING_MODEL_NAME",
        "google/flan-t5-base",
    )
    reranker_model_name: str = os.getenv(
        "RERANKER_MODEL_NAME",
        "cross-encoder/ms-marco-MiniLM-L-6-v2",
    )
    vectorstore_dir: str = os.getenv("VECTORSTORE_DIR", "./data/chroma")
    docs_dir: str = os.getenv("DOCS_DIR", "./data/docs")


settings = Settings()
