from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from .config import settings

_vectorstore = None
_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        model_kwargs = {}
        if settings.hf_token:
            model_kwargs["token"] = settings.hf_token

        _embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model_name,
            model_kwargs=model_kwargs,
        )
    return _embeddings

def get_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            collection_name="pdf_chunks",
            embedding_function=get_embeddings(),
            persist_directory=settings.vectorstore_dir,
        )
    return _vectorstore
