from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    file_path: str 

class QueryRequest(BaseModel):
    query: str
    top_k: int = 10

class DocumentChunk(BaseModel):
    content: str
    metadata: dict

class QueryResponse(BaseModel):
    query: str
    answer: str
    context: List[DocumentChunk]
