# NOTE: This file has been rewritten to use FAISS instead of Chroma.
from __future__ import annotations

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from langchain_openai import ChatOpenAI

from schemas import ChatRequest, ChatResponse
from chain_factory import get_chain
from constants import CODE_ANALYSIS_PROMPT

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Handle chat requests (normal RAG or code analysis)."""

    # --- Code Analysis Mode -------------------------------------------------
    if request.isCodeMode:
        llm = ChatOpenAI(temperature=0)
        system_prompt = CODE_ANALYSIS_PROMPT.strip()
        user_prompt = f"```python\n{request.message}\n```"
        try:
            result_msg = llm.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ])
            return ChatResponse(response=result_msg.content)
        except Exception as exc:  # pragma: no cover
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    # --- Normal Chat Mode ---------------------------------------------------
    chain = get_chain()
    try:
        result = chain.invoke({"question": request.message})
        return ChatResponse(response=result["answer"])
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/health")
async def health_check():  # noqa: D401
    """Simple health check endpoint."""
    return {"status": "OK"}


# ---------------------------------------------------------------------------
# Root endpoint can optionally serve frontend files if you still bundle them
# ---------------------------------------------------------------------------


@app.get("/")
async def read_index():
    try:
        return FileResponse(str(FRONT_DIST / "index.html"))
    except Exception:  # pragma: no cover
        return {"message": "Frontend not built. Please run 'npm run build' first."}


# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
FRONT_DIST = BASE_DIR / "frontend" / "dist"
try:
    app.mount("/", StaticFiles(directory=str(FRONT_DIST), html=True), name="static")
except Exception:
    pass


# ---------------------------------------------------------------------------
# Debug entry point (python backend/main.py)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 3000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)