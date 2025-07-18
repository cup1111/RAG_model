# Rewrite the entire file to adapt to the latest langchain/openai ecosystem
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Latest LangChain related imports
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory

# ---------------------------------------------------------------------------
# Environment Setup
# ---------------------------------------------------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set. Please configure it in .env or export it directly!")

# ---------------------------------------------------------------------------
# FastAPI Application Initialization
# ---------------------------------------------------------------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Pydantic Data Models
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    isCodeMode: bool = False  # Flag for code analysis mode

class ChatResponse(BaseModel):
    response: str

# ---------------------------------------------------------------------------
# Built-in Knowledge Base (for demo, can be replaced with actual document vector store)
# ---------------------------------------------------------------------------
KNOWLEDGE_BASE = """
Basic knowledge about artificial intelligence:

1. AI Definition
Artificial Intelligence (AI) is a branch of computer science dedicated to creating machines capable of simulating human intelligence.

2. Machine Learning
Machine learning is a subset of AI that enables computers to learn from data without explicit programming.

3. Deep Learning
Deep learning is a branch of machine learning that uses multi-layer neural networks to learn data representations.

4. Natural Language Processing
NLP enables computers to understand, interpret, and generate human language.

5. Computer Vision
Computer vision enables machines to understand and process visual information.
"""

CODE_ANALYSIS_PROMPT = """
Please analyze the following code in terms of:

1. Code complexity analysis:
   - Time complexity
   - Space complexity
   - Code structure complexity

2. Completion assessment:
   - Functionality completeness
   - Error handling
   - Boundary case handling

3. Code quality analysis:
   - Code readability
   - Naming conventions
   - Comment completeness
   - Code reusability

4. Improvement suggestions:
   - Performance optimization suggestions
   - Code structure optimization suggestions
   - Security suggestions

Please provide a detailed analysis report.
"""

# ---------------------------------------------------------------------------
# Vector Store & Chain Route Encapsulation
# ---------------------------------------------------------------------------
class DocumentStore:
    """Encapsulates vector storage, memory and other components."""

    def __init__(self, persist_directory: str = "./chroma_db") -> None:
        try:
            # embeddings will automatically read OPENAI_API_KEY from environment variables
            self.embeddings = OpenAIEmbeddings()
            self.persist_directory = persist_directory
            # Initialize or load ChromaDB
            self.vector_store = Chroma(
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
            )

            # Add demo text if empty
            if len(self.vector_store.get()) == 0:
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                texts = splitter.split_text(KNOWLEDGE_BASE)
                self.vector_store.add_texts(texts)
                self.vector_store.persist()

            # Conversation memory
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer",
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to initialize DocumentStore: {exc}") from exc

    def get_chain(self) -> ConversationalRetrievalChain:
        """Build conversation chain with retrieval."""
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
        retriever = self.vector_store.as_retriever()
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=self.memory,
            return_source_documents=True,
            verbose=True,
            return_generated_question=False,
            output_key="answer",
        )
        return chain


# Singleton pattern to avoid repeated loading
_DOC_STORE: DocumentStore | None = None
_CHAIN: ConversationalRetrievalChain | None = None

def get_chain() -> ConversationalRetrievalChain:
    global _DOC_STORE, _CHAIN
    if _CHAIN is None:
        _DOC_STORE = DocumentStore()
        _CHAIN = _DOC_STORE.get_chain()
    return _CHAIN

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint supporting two modes:
    1. Normal Q&A via ConversationalRetrievalChain (with memory & vector store)
    2. Code analysis mode – directly call LLM with analysis prompt, without touching chain/memory.
    """

    # --- Code Analysis Mode -------------------------------------------------
    if request.isCodeMode:
        system_prompt = CODE_ANALYSIS_PROMPT.strip()
        user_prompt = f"```python\n{request.message}\n```"
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        try:
            result_msg = llm.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ])
            return ChatResponse(response=result_msg.content)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Error processing request: {exc}") from exc

    # --- Normal Chat Mode ---------------------------------------------------
    chain = get_chain()
    try:
        result = chain.invoke({"question": request.message})
        return ChatResponse(response=result["answer"])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error processing request: {exc}") from exc


@app.get("/health")
async def health_check():
    return {"status": "OK"}


# ---------------------------------------------------------------------------
# Debug Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)