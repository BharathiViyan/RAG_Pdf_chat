from typing import List, Dict, Any
from .vectorstore import get_vectorstore
from .reranker import rerank
from .generator import generate_answer

def retrieve(query: str, top_k: int = 10) -> List[Dict[str, Any]]:
    vs = get_vectorstore()
    docs = vs.similarity_search(query, k=top_k)
    return [
        {
            "content": d.page_content,
            "metadata": d.metadata,
        }
        for d in docs
    ]

def answer_query(query: str, top_k: int = 5) -> tuple[str, List[Dict[str, Any]]]:
    retrieved = retrieve(query, top_k)
    reranked = rerank(query, retrieved, top_k=min(3, len(retrieved)))
    answer = generate_answer(query, reranked)
    return answer, reranked
