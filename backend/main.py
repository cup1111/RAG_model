from __future__ import annotations

"""Application entrypoint.

This module wires the FastAPI application together, adds CORS middleware
and includes the API routes defined in `routes.py`.
"""

import os

# ---------------------------------------------------------------------------
# Stub out onnxruntime BEFORE any chromadb import to avoid optional dependency
# issues. We never use the default ONNX embedding, so a dummy module is fine.
# ---------------------------------------------------------------------------
import sys, types  # noqa: E402

if 'onnxruntime' not in sys.modules:
    fake_ort = types.ModuleType('onnxruntime')
    # provide minimal attrs to satisfy chromadb import
    fake_ort.__dict__.update({
        'get_available_providers': lambda: [],
        '__version__': '0.0.0',
    })
    sys.modules['onnxruntime'] = fake_ort

# ---- 阻断 chromadb 默认嵌入器 -----------------------------------
import types, sys

dummy_ef_mod = types.ModuleType("chromadb.utils.embedding_functions")
class _NoopEF:
    def __init__(self, *_, **__): pass
    def __call__(self, texts):      # 返回占位向量，维度随便
        return [[0.0] * 3 for _ in texts]

dummy_ef_mod.DefaultEmbeddingFunction = _NoopEF
sys.modules["chromadb.utils.embedding_functions"] = dummy_ef_mod
# ----------------------------------------------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Ensure environment variables are loaded early in the process
import config  # noqa: F401  pylint: disable=unused-import

from routes import router

app = FastAPI()

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
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
# Add API routes first so they have higher priority than the catch-all StaticFiles
app.include_router(router, prefix="/api")

# ---------------------------------------------------------------------------
# Static Files (Frontend)
# ---------------------------------------------------------------------------
# Try to serve frontend static files if they exist (mounted after API routes)
try:
    app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")
except Exception:
    # If frontend is not built, just serve API
    pass

# ---------------------------------------------------------------------------
# Root endpoint (serve frontend)
# ---------------------------------------------------------------------------
@app.get("/")
async def read_index():
    """Serve the frontend index.html file."""
    try:
        return FileResponse("../frontend/dist/index.html")
    except Exception:
        return {"message": "Frontend not built. Please run 'npm run build' first."}

# ---------------------------------------------------------------------------
# Debug Entry Point (only used when `python main.py`)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    
    # Railway provides PORT environment variable
    port = int(os.getenv("PORT", 3000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)