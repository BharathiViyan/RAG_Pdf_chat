import uvicorn
from fastapi import FastAPI
from app.api import router as api_router
from app.config import settings

app = FastAPI(
    title="PDF RAG Chat",
    version="0.1.0",
    description="RAG over PDF with Docling, Chroma, reranking",
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )
