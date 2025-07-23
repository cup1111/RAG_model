from __future__ import annotations

"""Singleton helper to build / load an in-memory FAISS vector store
using OpenAIEmbeddings. Keeps code isolated from FastAPI for easy reuse."""

from pathlib import Path
from typing import Optional

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from constants import KNOWLEDGE_BASE

__all__ = ["get_db"]

# ---------------------------------------------------------------------------
# Private singletons
# ---------------------------------------------------------------------------

_EMBEDDINGS: Optional[OpenAIEmbeddings] = None
_DB: Optional[FAISS] = None
_INDEX_PATH = Path("./faiss_index")


def _init_embeddings() -> OpenAIEmbeddings:  # noqa: D401 (simple function)
    """Return (and cache) the OpenAIEmbeddings instance."""
    global _EMBEDDINGS
    if _EMBEDDINGS is None:
        _EMBEDDINGS = OpenAIEmbeddings()
    return _EMBEDDINGS


def _build_db() -> FAISS:  # noqa: D401
    """Create a FAISS store seeded with demo knowledge base data."""
    embed = _init_embeddings()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = splitter.split_text(KNOWLEDGE_BASE)
    db = FAISS.from_texts(texts, embedding=embed)
    return db


def get_db() -> FAISS:  # noqa: D401
    """Return a shared FAISS instance, building / loading on first call."""
    global _DB
    if _DB is None:
        if _INDEX_PATH.exists():
            _DB = FAISS.load_local(str(_INDEX_PATH), _init_embeddings(), allow_dangerous_deserialization=True)
        else:
            _DB = _build_db()
            _DB.save_local(str(_INDEX_PATH))
    return _DB 