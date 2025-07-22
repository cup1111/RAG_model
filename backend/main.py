from __future__ import annotations

"""Application entrypoint.

This module wires the FastAPI application together, adds CORS middleware
and includes the API routes defined in `routes.py`.
"""

import os
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
# Static Files (Frontend)
# ---------------------------------------------------------------------------
# Try to serve frontend static files if they exist
try:
    app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")
except Exception:
    # If frontend is not built, just serve API
    pass

# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------
app.include_router(router, prefix="/api")

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