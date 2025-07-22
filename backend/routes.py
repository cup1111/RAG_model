from __future__ import annotations

"""FastAPI routes for chat and health check endpoints."""

from fastapi import APIRouter, HTTPException
from langchain_openai import ChatOpenAI

from constants import CODE_ANALYSIS_PROMPT
from schemas import ChatRequest, ChatResponse
from chain_factory import get_chain

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Handle chat requests in two modes.

    1. Normal conversational retrieval (RAG) mode (isCodeMode=False)
    2. Code analysis mode (isCodeMode=True)
    """

    # --- Code Analysis Mode -------------------------------------------------
    if request.isCodeMode:
        system_prompt = CODE_ANALYSIS_PROMPT.strip()
        user_prompt = f"```python\n{request.message}\n```"
        import os
        for _v in ("HTTP_PROXY","HTTPS_PROXY","http_proxy","https_proxy"):
            os.environ.pop(_v, None)
        import openai  # local import
        llm = ChatOpenAI(client=openai.OpenAI(), temperature=0, model_name="gpt-3.5-turbo")
        try:
            result_msg = llm.invoke(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            )
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


@router.get("/health")
async def health_check():
    """Simple health check endpoint."""

    return {"status": "OK"} 