from __future__ import annotations

"""Vector store, embeddings and memory encapsulated in a single class.

This module depends on `config` for environment validation and uses the
constants defined in `constants`.
"""

# Trigger .env loading and API-key validation on import
import config  # noqa: F401  pylint: disable=unused-import

# Use modern OpenAI client explicitly and pass it to LangChain wrappers
import openai  # type: ignore

# langchain_openai 0.1.x supports `client` kwarg for OpenAI SDK ≥1.24
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from constants import KNOWLEDGE_BASE


class DocumentStore:
    """Encapsulate Chroma vector storage and conversation memory."""

    def __init__(self, persist_directory: str = "./chroma_db") -> None:
        # Ensure proxy env vars don't break openai client on httpx
        import os
        for _var in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
            os.environ.pop(_var, None)

        # Create client
        self._client = openai.OpenAI()

        # Initialise embeddings with explicit client to avoid deprecated params
        self.embeddings = OpenAIEmbeddings(client=self._client)
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
        llm = ChatOpenAI(client=self._client, temperature=0.7, model_name="gpt-3.5-turbo")
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