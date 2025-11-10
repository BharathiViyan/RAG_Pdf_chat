from fastapi import APIRouter, HTTPException
from .schemas import QueryRequest, QueryResponse, IngestRequest, DocumentChunk
from .pdf_ingest import ingest_pdf, ingest_all_pdfs_from_dir
from .rag_service import answer_query

router = APIRouter()

@router.post("/ingest", summary="Ingest a single PDF from path")
def ingest_pdf_endpoint(req: IngestRequest):
    try:
        count = ingest_pdf(req.file_path)
        return {"status": "ok", "chunks_ingested": count}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")


@router.post("/ingest-all", summary="Ingest all PDFs from docs dir")
def ingest_all_endpoint():
    count = ingest_all_pdfs_from_dir()
    return {"status": "ok", "total_chunks_ingested": count}


@router.post("/query", response_model=QueryResponse)
def query_endpoint(req: QueryRequest):
    answer, ctx = answer_query(req.query, req.top_k)
    return QueryResponse(
        query=req.query,
        answer=answer,
        context=[DocumentChunk(content=c["content"], metadata=c["metadata"]) for c in ctx],
    )
