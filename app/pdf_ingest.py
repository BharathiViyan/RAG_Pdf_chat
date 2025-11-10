from pathlib import Path
from typing import List, Dict, Any

from langchain_text_splitters import RecursiveCharacterTextSplitter
from docling.document import Document as DoclingDocument
from docling.readers import PdfReader

from .vectorstore import get_vectorstore
from .config import settings


def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader()
    doc: DoclingDocument = reader.read(pdf_path)
    # Docling doc has structured elements; for demo, flatten to text
    return doc.export_to_markdown()  # or .export_to_text()


def chunk_text(text: str) -> List[Dict[str, Any]]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " "],
    )
    chunks = splitter.split_text(text)
    return [
        {
            "content": chunk,
            "metadata": {},
        }
        for chunk in chunks
    ]


def ingest_pdf(pdf_path: str) -> int:
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    vs = get_vectorstore()
    docs = [c["content"] for c in chunks] # add to vectorstore with metadata
    metadatas = [{"source": pdf_path, **c["metadata"]} for c in chunks]
    vs.add_texts(docs, metadatas=metadatas)
    return len(chunks)


def ingest_all_pdfs_from_dir() -> int:
    docs_dir = Path(settings.docs_dir)
    total = 0
    for pdf_file in docs_dir.glob("*.pdf"):
        total += ingest_pdf(str(pdf_file))
    return total
