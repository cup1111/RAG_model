from __future__ import annotations

"""Singleton helper to build / load an in-memory FAISS vector store
using OpenAIEmbeddings. Keeps code isolated from FastAPI for easy reuse."""

from pathlib import Path
from typing import Optional

try:
    from langchain_community.vectorstores import FAISS
    _FAISS_AVAILABLE = True
except ImportError:  # pragma: no cover
    from langchain_community.vectorstores import DocArrayInMemorySearch as InMemVS
    _FAISS_AVAILABLE = False

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from constants import KNOWLEDGE_BASE

__all__ = ["get_db"]

# ---------------------------------------------------------------------------
# Private singletons
# ---------------------------------------------------------------------------

_EMBEDDINGS: Optional[OpenAIEmbeddings] = None
_DB: Optional[object] = None  # FAISS or InMemVS
_INDEX_PATH = Path("./faiss_index")


def _init_embeddings() -> OpenAIEmbeddings:  # noqa: D401 (simple function)
    """Return (and cache) the OpenAIEmbeddings instance."""
    global _EMBEDDINGS
    if _EMBEDDINGS is None:
        _EMBEDDINGS = OpenAIEmbeddings()
    return _EMBEDDINGS


def _build_db() -> object:  # noqa: D401
    """Create vector store (FAISS if available else in-memory)."""
    embed = _init_embeddings()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = splitter.split_text(KNOWLEDGE_BASE)

    if _FAISS_AVAILABLE:
        try:
            return FAISS.from_texts(texts, embedding=embed)
        except ImportError:
            # 动态库缺失，降级到纯 Python 内存向量库
            global _FAISS_AVAILABLE  # noqa: PLW0603
            _FAISS_AVAILABLE = False
            return InMemVS.from_texts(texts, embedding=embed)
    # Fallback: pure-python in-memory vector store (non-persistent)
    return InMemVS.from_texts(texts, embedding=embed)


def get_db() -> object:  # noqa: D401
    """Return a shared FAISS instance, building / loading on first call."""
    global _DB
    if _DB is None:
        if _FAISS_AVAILABLE and _INDEX_PATH.exists():
            _DB = FAISS.load_local(
                str(_INDEX_PATH), _init_embeddings(), allow_dangerous_deserialization=True
            )
        else:
            _DB = _build_db()
            if _FAISS_AVAILABLE:
                _DB.save_local(str(_INDEX_PATH))
    return _DB 