from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
import os

# Add API here
load_dotenv()
OPENAI_API_KEY = ''
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Create FastAPI application
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    message: str
    isCodeMode: bool = False  # Flag for code analysis mode

# Response model
class ChatResponse(BaseModel):
    response: str

# Predefined knowledge base content
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

# 在 KNOWLEDGE_BASE 后添加代码分析提示
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

# Document storage class
class DocumentStore:
    def __init__(self):
        try:
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-ada-002"
            )
            self.vector_store = None
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )
        except Exception as e:
            print(f"Error initializing DocumentStore: {str(e)}")
            raise

    def init_vector_store(self):
        if not self.vector_store:
            try:
                # Try to load existing vector store
                self.vector_store = Chroma(
                    embedding_function=self.embeddings,
                    persist_directory="./chroma_db"
                )
                
                # Add text only if store is empty
                if len(self.vector_store.get()) == 0:
                    print("Vector store is empty, adding initial text...")
                    # Split predefined knowledge base text
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200
                    )
                    texts = text_splitter.split_text(KNOWLEDGE_BASE)

                    # Add text to vector store
                    self.vector_store.add_texts(texts)
                    # Persist storage
                    self.vector_store.persist()
                    print("Text addition completed")
                else:
                    print("Using existing vector store")
                    
            except Exception as e:
                print(f"Error initializing vector store: {str(e)}")
                raise

    def get_relevant_documents(self, query: str, k: int = 3):
        if not self.vector_store:
            return []
        return self.vector_store.similarity_search(query, k=k)

# Create document store instance
doc_store = DocumentStore()

# Create RAG chain
def create_rag_chain():
    try:
        # Check API key
        if not os.getenv("OPENAI_API_KEY"):
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")
        
        print("Creating LLM...")
        # Create LLM
        llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo"
        )
        print("LLM created successfully")
        
        # Initialize vector store
        print("Initializing vector store...")
        doc_store.init_vector_store()
        print("Vector store initialized")

        # Create retrieval chain
        print("Creating retrieval chain...")
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=doc_store.vector_store.as_retriever(),
            memory=doc_store.memory,
            return_source_documents=True,
            verbose=True,
            return_generated_question=False,
            output_key="answer"
        )
        print("Retrieval chain created")
        
        return chain
    except Exception as e:
        print(f"Error creating RAG chain: {str(e)}")
        import traceback
        print(f"Error stack: {traceback.format_exc()}")
        raise

# Create RAG chain instance
rag_chain = create_rag_chain()

@app.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        if request.isCodeMode:
            # In code mode, add code analysis prompt
            analysis_request = f"{CODE_ANALYSIS_PROMPT}\n\nCode:\n{request.message}"
            result = rag_chain({"question": analysis_request})
        else:
            # Normal conversation mode
            result = rag_chain({"question": request.message})
        
        return ChatResponse(response=result["answer"])
    except Exception as e:
        print(f"Detailed error: {str(e)}")
        import traceback
        print(f"Error stack: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing request: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "OK"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)