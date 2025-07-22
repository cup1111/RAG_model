from __future__ import annotations

"""Singleton factory for returning a shared ConversationalRetrievalChain.

The chain is expensive to build (vector store, embeddings, etc.) so we
construct it once and reuse it for all incoming requests.
"""

from typing import Optional

from langchain.chains import ConversationalRetrievalChain

from document_store import DocumentStore

__all__ = ["get_chain"]

# Module-level singletons (initialized lazily)
_DOC_STORE: Optional[DocumentStore] = None
_CHAIN: Optional[ConversationalRetrievalChain] = None


def get_chain() -> ConversationalRetrievalChain:  # noqa: D401  (simple function)
    """Return a shared ConversationalRetrievalChain instance.

    The first call creates the underlying `DocumentStore` and chain; all
    subsequent calls return the same objects.
    """
    global _DOC_STORE, _CHAIN

    if _CHAIN is None:
        _DOC_STORE = DocumentStore()
        _CHAIN = _DOC_STORE.get_chain()
    return _CHAIN 