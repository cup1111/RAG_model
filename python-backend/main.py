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

# 在这里添加API
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 创建 FastAPI 应用
app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求模型
class ChatRequest(BaseModel):
    message: str

# 响应模型
class ChatResponse(BaseModel):
    response: str

# 预设的知识库内容
KNOWLEDGE_BASE = """
以下是关于人工智能的基础知识：

1. 人工智能定义
人工智能(AI)是计算机科学的一个分支，致力于创造能够模拟人类智能的机器。

2. 机器学习
机器学习是AI的一个子领域，让计算机能够从数据中学习，而无需显式编程。

3. 深度学习
深度学习是机器学习的一个分支，使用多层神经网络来学习数据的表示。

4. 自然语言处理
NLP让计算机能够理解、解释和生成人类语言。

5. 计算机视觉
计算机视觉使机器能够理解和处理视觉信息。
"""

# 文档存储
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
            print(f"初始化 DocumentStore 时出错: {str(e)}")
            raise

    def init_vector_store(self):
        if not self.vector_store:
            try:
                # 先尝试加载已存在的向量存储
                self.vector_store = Chroma(
                    embedding_function=self.embeddings,
                    persist_directory="./chroma_db"
                )
                
                # 如果是空的，才添加文本
                if len(self.vector_store.get()) == 0:
                    print("向量存储为空，添加初始文本...")
                    # 分割预设知识库文本
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200
                    )
                    texts = text_splitter.split_text(KNOWLEDGE_BASE)
                    
                    # 添加文本到向量存储
                    self.vector_store.add_texts(texts)
                    # 持久化存储
                    self.vector_store.persist()
                    print("文本添加完成")
                else:
                    print("使用已存在的向量存储")
                    
            except Exception as e:
                print(f"初始化向量存储时出错: {str(e)}")
                raise

    def get_relevant_documents(self, query: str, k: int = 3):
        if not self.vector_store:
            return []
        return self.vector_store.similarity_search(query, k=k)

# 创建文档存储实例
doc_store = DocumentStore()

# 创建 RAG 链
def create_rag_chain():
    try:
        # 检查 API 密钥
        if not os.getenv("OPENAI_API_KEY"):
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY 未设置")
        
        print("正在创建 LLM...")
        # 创建 LLM
        llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo"
        )
        print("LLM 创建成功")
        
        # 初始化向量存储
        print("正在初始化向量存储...")
        doc_store.init_vector_store()
        print("向量存储初始化成功")

        # 创建检索链
        print("正在创建检索链...")
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=doc_store.vector_store.as_retriever(),
            memory=doc_store.memory,
            return_source_documents=True,
            verbose=True,
            return_generated_question=False,
            output_key="answer"
        )
        print("检索链创建成功")
        
        return chain
    except Exception as e:
        print(f"创建 RAG 链时出错: {str(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")
        raise

# 创建 RAG 链实例
rag_chain = create_rag_chain()

@app.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        # 运行 RAG 链
        result = rag_chain({"question": request.message})
        return ChatResponse(response=result["answer"])
    except Exception as e:
        print(f"详细错误信息: {str(e)}")  # 添加详细错误日志
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")  # 打印完整错误堆栈
        raise HTTPException(
            status_code=500, 
            detail=f"处理请求时出错: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "OK"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)