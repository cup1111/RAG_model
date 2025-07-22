from __future__ import annotations

"""Vector store, embeddings and memory encapsulated in a single class.

This module depends on `config` for environment validation and uses the
constants defined in `constants`.
"""

# Trigger .env loading and API-key validation on import
import config  # noqa: F401  pylint: disable=unused-import

# ---------------------------------------------------------------------------
# Compatibility Patch: allow langchain_openai to pass `proxies` even though
# openai>=1.24 removed this parameter. We monkey-patch openai.OpenAI.__init__
# to accept and ignore a `proxies` kwarg.
# ---------------------------------------------------------------------------
import openai  # type: ignore


_orig_openai_init = openai.OpenAI.__init__  # type: ignore[attr-defined]


def _patched_init(self, *args, proxies=None, **kwargs):  # noqa: D401, ANN001
    """Patched __init__ that silently drops obsolete `proxies` kwarg."""

    # Discard the deprecated argument, then delegate to the original init
    _orig_openai_init(self, *args, **kwargs)


# Only patch once
if "proxies" not in _orig_openai_init.__code__.co_varnames:
    openai.OpenAI.__init__ = _patched_init  # type: ignore[method-assign]

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from constants import KNOWLEDGE_BASE


class DocumentStore:
    """Encapsulate Chroma vector storage and conversation memory."""

    def __init__(self, persist_directory: str = "./chroma_db") -> None:
        # Initialise embeddings (reads OPENAI_API_KEY from env)
        self.embeddings = OpenAIEmbeddings()
        self.persist_directory = persist_directory

        # Create or load the Chroma vector store
        self.vector_store = Chroma(
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
        )

        # Populate with demo knowledge if empty
        if len(self.vector_store.get()) == 0:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
            )
            texts = splitter.split_text(KNOWLEDGE_BASE)
            self.vector_store.add_texts(texts)
            self.vector_store.persist()

        # Conversation memory buffer keeps chat history
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer",
        )

    def get_chain(self) -> ConversationalRetrievalChain:
        """Create a ConversationalRetrievalChain wired to this store."""
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
        retriever = self.vector_store.as_retriever()
        return ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=self.memory,
            return_source_documents=True,
            verbose=True,
            return_generated_question=False,
            output_key="answer",
        ) 