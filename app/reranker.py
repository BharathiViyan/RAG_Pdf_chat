from typing import List, Dict, Any
from sentence_transformers import CrossEncoder
from .config import settings

_reranker = None

def get_reranker() -> CrossEncoder:
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(settings.reranker_model_name)
    return _reranker

def rerank(query: str, docs: List[Dict[str, Any]], top_k: int = 5):
    model = get_reranker()
    pairs = [(query, d["content"]) for d in docs]
    scores = model.predict(pairs)
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [d for d, _ in ranked[:top_k]]
