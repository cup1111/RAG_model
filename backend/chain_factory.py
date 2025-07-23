from __future__ import annotations

"""Provides a module-level singleton ConversationalRetrievalChain.
Replaces previous Chroma-based implementation with FAISS for minimal
external dependencies."""

from typing import Optional

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

from vectordb import get_db

__all__ = ["get_chain"]

_CHAIN: Optional[ConversationalRetrievalChain] = None


def get_chain() -> ConversationalRetrievalChain:  # noqa: D401 (simple function)
    """Return a shared ConversationalRetrievalChain instance."""
    global _CHAIN

    if _CHAIN is None:
        llm = ChatOpenAI(temperature=0.7)
        retriever = get_db().as_retriever()
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer",
        )
        _CHAIN = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            verbose=True,
            output_key="answer",
        )
    return _CHAIN 